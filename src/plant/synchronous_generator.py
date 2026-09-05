
from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp


@dataclass(frozen=True)
class GeneratorParams:
    """
    Parameter reduced-order synchronous generator
    untuk studi dinamika frekuensi PLTMH terisolasi.

    Nilai parameter pada tahap awal merupakan parameter
    simulasi dan harus divalidasi terhadap spesifikasi
    generator/literatur yang dipilih untuk tesis.
    """

    # Rating sistem
    rated_power_kw: float = 100.0
    nominal_frequency_hz: float = 50.0

    # Konfigurasi generator
    poles: int = 4

    # Parameter elektromekanik
    inertia_constant_s: float = 2.50
    damping_pu: float = 2.0


def electrical_base_speed_rad_s(
    params: GeneratorParams
) -> float:
    """
    Kecepatan sudut elektrik basis:

        omega_b = 2*pi*f0
    """
    return (
        2.0
        * np.pi
        * params.nominal_frequency_hz
    )


def synchronous_speed_rpm(
    params: GeneratorParams
) -> float:
    """
    Kecepatan sinkron mekanik:

        ns = 120*f0/p
    """
    return (
        120.0
        * params.nominal_frequency_hz
        / params.poles
    )


def frequency_hz(
    omega_pu,
    params: GeneratorParams
):
    """
    Konversi kecepatan rotor per-unit ke frekuensi:

        f = f0 * omega_pu
    """
    return (
        params.nominal_frequency_hz
        * np.asarray(omega_pu)
    )


def rotor_speed_rpm(
    omega_pu,
    params: GeneratorParams
):
    """
    Kecepatan mekanik rotor dalam rpm.
    """
    return (
        synchronous_speed_rpm(params)
        * np.asarray(omega_pu)
    )


def constant_profile(
    value: float
) -> Callable[[float], float]:
    """
    Membentuk profil daya konstan.
    """
    return lambda t: float(value)


def step_profile(
    before: float,
    after: float,
    t_step: float
) -> Callable[[float], float]:
    """
    Membentuk profil perubahan step.
    """

    def profile(t: float) -> float:

        if t < t_step:
            return float(before)

        return float(after)

    return profile


def generator_rhs(
    t: float,
    x: np.ndarray,
    params: GeneratorParams,
    pm_profile: Callable[[float], float],
    pe_profile: Callable[[float], float],
) -> np.ndarray:
    """
    Reduced-order electromechanical model.

    States:
        x[0] = omega_pu
        x[1] = delta_rad

    Swing equation:

        domega/dt =
        [Pm - Pe - D(omega - 1)] / (2H)

    Rotor angle relative to synchronous reference:

        ddelta/dt =
        omega_b * (omega - 1)
    """

    omega_pu = x[0]

    pm_pu = float(
        pm_profile(t)
    )

    pe_pu = float(
        pe_profile(t)
    )

    domega_dt = (
        pm_pu
        - pe_pu
        - params.damping_pu
        * (omega_pu - 1.0)
    ) / (
        2.0
        * params.inertia_constant_s
    )

    ddelta_dt = (
        electrical_base_speed_rad_s(params)
        * (omega_pu - 1.0)
    )

    return np.array([
        domega_dt,
        ddelta_dt
    ])


def simulate_generator(
    params: GeneratorParams,
    pm_profile: Callable[[float], float],
    pe_profile: Callable[[float], float],
    t_end_s: float = 10.0,
    dt_s: float = 0.01,
    initial_omega_pu: float = 1.0,
    initial_delta_rad: float = 0.0,
) -> pd.DataFrame:
    """
    Simulasi reduced-order synchronous generator.
    """

    x0 = np.array([
        initial_omega_pu,
        initial_delta_rad
    ])

    t_eval = np.arange(
        0.0,
        t_end_s + 0.5 * dt_s,
        dt_s
    )

    solution = solve_ivp(
        fun=lambda t, x: generator_rhs(
            t,
            x,
            params,
            pm_profile,
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

    t = solution.t
    omega_pu = solution.y[0]
    delta_rad = solution.y[1]

    pm_pu = np.array([
        pm_profile(time)
        for time in t
    ])

    pe_pu = np.array([
        pe_profile(time)
        for time in t
    ])

    f_hz = frequency_hz(
        omega_pu,
        params
    )

    speed_rpm = rotor_speed_rpm(
        omega_pu,
        params
    )

    delta_f_hz = (
        f_hz
        - params.nominal_frequency_hz
    )

    power_mismatch_pu = (
        pm_pu
        - pe_pu
    )

    power_mismatch_kw = (
        power_mismatch_pu
        * params.rated_power_kw
    )

    rocof_hz_s = np.gradient(
        f_hz,
        t
    )

    return pd.DataFrame({
        "time_s": t,
        "pm_pu": pm_pu,
        "pe_pu": pe_pu,
        "power_mismatch_pu": power_mismatch_pu,
        "power_mismatch_kw": power_mismatch_kw,
        "omega_pu": omega_pu,
        "frequency_hz": f_hz,
        "delta_f_hz": delta_f_hz,
        "rotor_speed_rpm": speed_rpm,
        "delta_rad": delta_rad,
        "delta_deg": np.rad2deg(delta_rad),
        "rocof_hz_s": rocof_hz_s,
    })
