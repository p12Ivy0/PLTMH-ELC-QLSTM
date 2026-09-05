
from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class PlantParams:
    """
    Parameter dasar reduced-order model PLTMH.

    Parameter dinamik pada tahap awal merupakan nilai awal
    simulasi dan selanjutnya harus divalidasi terhadap
    spesifikasi sistem atau literatur yang digunakan.
    """

    # Rating sistem
    rated_power_kw: float = 100.0
    nominal_frequency_hz: float = 50.0

    # Parameter hidraulik
    rho_water_kg_m3: float = 1000.0
    gravity_m_s2: float = 9.80665
    net_head_m: float = 30.0
    turbine_efficiency: float = 0.80

    # Parameter dinamik
    turbine_time_constant_s: float = 0.40
    inertia_constant_s: float = 2.50
    load_damping_pu: float = 2.0

    # Batas daya mekanik turbin
    pm_min_pu: float = 0.0
    pm_max_pu: float = 1.10


def hydraulic_power_w(
    flow_m3_s: float,
    params: PlantParams
) -> float:
    """
    Menghitung daya hidraulik:

        Ph = rho * g * Q * H
    """

    return (
        params.rho_water_kg_m3
        * params.gravity_m_s2
        * flow_m3_s
        * params.net_head_m
    )


def mechanical_power_w(
    flow_m3_s: float,
    params: PlantParams
) -> float:
    """
    Menghitung daya mekanik turbin:

        Pm = eta_t * Ph
    """

    return (
        params.turbine_efficiency
        * hydraulic_power_w(flow_m3_s, params)
    )


def nominal_flow_m3_s(
    params: PlantParams
) -> float:
    """
    Menghitung debit nominal agar daya mekanik turbin
    sama dengan daya nominal PLTMH.
    """

    rated_power_w = (
        params.rated_power_kw * 1000.0
    )

    return rated_power_w / (
        params.rho_water_kg_m3
        * params.gravity_m_s2
        * params.net_head_m
        * params.turbine_efficiency
    )


def constant_profile(
    value: float
) -> Callable[[float], float]:
    """
    Membentuk profil input konstan terhadap waktu.
    """

    return lambda t: float(value)


def step_profile(
    before: float,
    after: float,
    t_step: float
) -> Callable[[float], float]:
    """
    Membentuk profil perubahan step.

    before : nilai sebelum gangguan
    after  : nilai setelah gangguan
    t_step : waktu terjadinya gangguan
    """

    def profile(t: float) -> float:

        if t < t_step:
            return float(before)

        return float(after)

    return profile


def plant_rhs(
    t: float,
    x: np.ndarray,
    params: PlantParams,
    pm_cmd_profile: Callable[[float], float],
    pe_profile: Callable[[float], float],
) -> np.ndarray:
    """
    Persamaan diferensial reduced-order PLTMH.

    State:

        x[0] = Pm_pu
        x[1] = omega_pu

    Model dinamika turbin:

        Tt * dPm/dt = Pm_cmd - Pm

    Model dinamika rotor:

                    Pm - Pe - D(omega - 1)
        domega/dt = -----------------------
                              2H
    """

    pm_pu = x[0]
    omega_pu = x[1]

    # Perintah daya mekanik
    pm_cmd_pu = np.clip(
        pm_cmd_profile(t),
        params.pm_min_pu,
        params.pm_max_pu
    )

    # Daya elektrik / beban ekuivalen
    pe_pu = max(
        float(pe_profile(t)),
        0.0
    )

    # Dinamika daya mekanik turbin
    dpm_dt = (
        pm_cmd_pu - pm_pu
    ) / params.turbine_time_constant_s

    # Dinamika kecepatan rotor
    domega_dt = (
        pm_pu
        - pe_pu
        - params.load_damping_pu
        * (omega_pu - 1.0)
    ) / (
        2.0
        * params.inertia_constant_s
    )

    return np.array([
        dpm_dt,
        domega_dt
    ])


def simulate_plant(
    params: PlantParams,
    pm_cmd_profile: Callable[[float], float],
    pe_profile: Callable[[float], float],
    t_end_s: float = 20.0,
    dt_s: float = 0.01,
    initial_pm_pu: float | None = None,
    initial_omega_pu: float = 1.0,
) -> pd.DataFrame:
    """
    Menjalankan simulasi reduced-order PLTMH
    menggunakan scipy.integrate.solve_ivp.
    """

    # Jika tidak diberikan,
    # kondisi awal Pm mengikuti command awal.
    if initial_pm_pu is None:
        initial_pm_pu = float(
            pm_cmd_profile(0.0)
        )

    # State awal
    x0 = np.array([
        initial_pm_pu,
        initial_omega_pu
    ])

    # Titik waktu keluaran
    t_eval = np.arange(
        0.0,
        t_end_s + 0.5 * dt_s,
        dt_s
    )

    # Penyelesaian persamaan diferensial
    solution = solve_ivp(
        fun=lambda t, x: plant_rhs(
            t,
            x,
            params,
            pm_cmd_profile,
            pe_profile,
        ),
        t_span=(
            0.0,
            t_end_s
        ),
        y0=x0,
        t_eval=t_eval,
        method="DOP853",
        rtol=1e-9,
        atol=1e-11,
        max_step=dt_s,
    )

    if not solution.success:
        raise RuntimeError(
            solution.message
        )

    # Hasil state
    t = solution.t
    pm_pu = solution.y[0]
    omega_pu = solution.y[1]

    # Rekonstruksi input
    pm_cmd_pu = np.array([
        pm_cmd_profile(time)
        for time in t
    ])

    pe_pu = np.array([
        pe_profile(time)
        for time in t
    ])

    # Konversi omega per-unit menjadi frekuensi
    frequency_hz = (
        params.nominal_frequency_hz
        * omega_pu
    )

    # Deviasi frekuensi
    delta_f_hz = (
        frequency_hz
        - params.nominal_frequency_hz
    )

    # Ketidakseimbangan daya
    power_mismatch_pu = (
        pm_pu - pe_pu
    )

    power_mismatch_kw = (
        power_mismatch_pu
        * params.rated_power_kw
    )

    # Rate of Change of Frequency
    rocof_hz_s = np.gradient(
        frequency_hz,
        t
    )

    # Simpan hasil dalam DataFrame
    return pd.DataFrame({
        "time_s": t,
        "pm_cmd_pu": pm_cmd_pu,
        "pm_pu": pm_pu,
        "pe_pu": pe_pu,
        "omega_pu": omega_pu,
        "frequency_hz": frequency_hz,
        "delta_f_hz": delta_f_hz,
        "power_mismatch_pu": power_mismatch_pu,
        "power_mismatch_kw": power_mismatch_kw,
        "rocof_hz_s": rocof_hz_s,
    })
