
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

from ..plant.synchronous_generator import (
    GeneratorParams,
    electrical_base_speed_rad_s,
)

from ..plant.elc import ELCParams

from ..plant.dump_load import (
    average_dump_power_kw,
)


@dataclass(frozen=True)
class PIControllerParams:
    """
    Fixed-gain PI controller untuk ELC PLTMH.

    control_direction = -1:
        f < f_ref -> e > 0 -> duty ELC turun

    Unit:
        kp : duty / Hz
        ki : duty / (Hz s)
    """

    kp: float = 0.10
    ki: float = 0.50

    reference_frequency_hz: float = 50.0

    output_bias: float = 0.20

    output_min: float = 0.0
    output_max: float = 1.0

    control_direction: float = -1.0

    def __post_init__(self):

        if self.kp < 0.0:
            raise ValueError(
                "kp must be non-negative."
            )

        if self.ki < 0.0:
            raise ValueError(
                "ki must be non-negative."
            )

        if not (
            self.output_min
            < self.output_max
        ):
            raise ValueError(
                "output_min must be smaller "
                "than output_max."
            )

        if not (
            self.output_min
            <= self.output_bias
            <= self.output_max
        ):
            raise ValueError(
                "output_bias must lie within "
                "output limits."
            )

        if self.control_direction not in (
            -1.0,
            1.0,
        ):
            raise ValueError(
                "control_direction must be "
                "-1 or +1."
            )


def frequency_error_hz(
    reference_frequency_hz: float,
    measured_frequency_hz: float,
) -> float:
    """
    e = f_ref - f
    """

    return float(
        reference_frequency_hz
        - measured_frequency_hz
    )


def pi_raw_output(
    error_hz: float,
    integral_error_hz_s: float,
    params: PIControllerParams,
) -> float:
    """
    Unsaturated duty-cycle command.
    """

    correction = (
        params.kp
        * error_hz
        +
        params.ki
        * integral_error_hz_s
    )

    output = (
        params.output_bias
        +
        params.control_direction
        * correction
    )

    return float(output)


def saturate_pi_output(
    raw_output: float,
    params: PIControllerParams,
) -> float:
    """
    Saturasi duty cycle.
    """

    return float(
        np.clip(
            raw_output,
            params.output_min,
            params.output_max,
        )
    )


def pi_output(
    error_hz: float,
    integral_error_hz_s: float,
    params: PIControllerParams,
):
    """
    Mengembalikan:
        raw duty,
        saturated duty.
    """

    raw = pi_raw_output(
        error_hz,
        integral_error_hz_s,
        params,
    )

    saturated = saturate_pi_output(
        raw,
        params,
    )

    return raw, saturated


def conditional_integrator_derivative(
    error_hz: float,
    raw_output: float,
    params: PIControllerParams,
) -> float:
    """
    Conditional-integration anti-windup.

    Integrator dihentikan bila error akan
    mendorong PI semakin jauh ke daerah saturasi.
    """

    output_rate_sign = (
        params.control_direction
        * params.ki
        * error_hz
    )

    if (
        raw_output < params.output_min
        and output_rate_sign < 0.0
    ):
        return 0.0

    if (
        raw_output > params.output_max
        and output_rate_sign > 0.0
    ):
        return 0.0

    return float(error_hz)


def closed_loop_rhs(
    t: float,
    x: np.ndarray,
    controller_params: PIControllerParams,
    generator_params: GeneratorParams,
    elc_params: ELCParams,
    mechanical_power_profile: Callable[[float], float],
    consumer_power_profile: Callable[[float], float],
):
    """
    Closed-loop states:

        x[0] = omega_pu
        x[1] = delta_rad
        x[2] = P_dump actual [kW]
        x[3] = integral error [Hz s]
    """

    omega_pu = float(x[0])
    dump_power_kw = float(x[2])
    integral_error = float(x[3])

    frequency_hz = (
        generator_params.nominal_frequency_hz
        * omega_pu
    )

    error_hz = frequency_error_hz(
        controller_params.reference_frequency_hz,
        frequency_hz,
    )

    raw_duty, duty = pi_output(
        error_hz,
        integral_error,
        controller_params,
    )

    d_integral_dt = (
        conditional_integrator_derivative(
            error_hz,
            raw_duty,
            controller_params,
        )
    )

    dump_command_kw = (
        average_dump_power_kw(
            duty,
            elc_params.dump_load,
        )
    )

    d_dump_dt = (
        dump_command_kw
        - dump_power_kw
    ) / (
        elc_params.actuator_time_constant_s
    )

    consumer_power_kw = float(
        consumer_power_profile(t)
    )

    electrical_power_kw = (
        consumer_power_kw
        + dump_power_kw
    )

    pe_pu = (
        electrical_power_kw
        / generator_params.rated_power_kw
    )

    pm_pu = float(
        mechanical_power_profile(t)
    )

    d_omega_dt = (
        pm_pu
        - pe_pu
        - generator_params.damping_pu
        * (omega_pu - 1.0)
    ) / (
        2.0
        * generator_params.inertia_constant_s
    )

    d_delta_dt = (
        electrical_base_speed_rad_s(
            generator_params
        )
        * (omega_pu - 1.0)
    )

    return np.array([
        d_omega_dt,
        d_delta_dt,
        d_dump_dt,
        d_integral_dt,
    ])


def simulate_pi_elc_closed_loop(
    controller_params: PIControllerParams,
    generator_params: GeneratorParams,
    elc_params: ELCParams,
    mechanical_power_profile: Callable[[float], float],
    consumer_power_profile: Callable[[float], float],
    t_end_s: float = 10.0,
    dt_s: float = 0.005,
    initial_omega_pu: float = 1.0,
    initial_delta_rad: float = 0.0,
    initial_integral_error_hz_s: float = 0.0,
    initial_dump_power_kw: Optional[float] = None,
) -> pd.DataFrame:
    """
    Simulasi closed-loop:
    generator + ELC + fixed-gain PI.
    """

    initial_frequency_hz = (
        generator_params.nominal_frequency_hz
        * initial_omega_pu
    )

    initial_error_hz = frequency_error_hz(
        controller_params.reference_frequency_hz,
        initial_frequency_hz,
    )

    _, initial_duty = pi_output(
        initial_error_hz,
        initial_integral_error_hz_s,
        controller_params,
    )

    if initial_dump_power_kw is None:

        initial_dump_power_kw = (
            average_dump_power_kw(
                initial_duty,
                elc_params.dump_load,
            )
        )

    x0 = np.array([
        initial_omega_pu,
        initial_delta_rad,
        initial_dump_power_kw,
        initial_integral_error_hz_s,
    ])

    n_steps = int(
        round(t_end_s / dt_s)
    )

    t_eval = np.linspace(
        0.0,
        t_end_s,
        n_steps + 1,
    )

    solution = solve_ivp(
        fun=lambda t, x: closed_loop_rhs(
            t,
            x,
            controller_params,
            generator_params,
            elc_params,
            mechanical_power_profile,
            consumer_power_profile,
        ),
        t_span=(
            0.0,
            t_end_s,
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

    time_s = solution.t

    omega_pu = solution.y[0]
    delta_rad = solution.y[1]
    dump_power_kw = solution.y[2]
    integral_error = solution.y[3]

    frequency_hz = (
        generator_params.nominal_frequency_hz
        * omega_pu
    )

    error_hz = (
        controller_params.reference_frequency_hz
        - frequency_hz
    )

    raw_duty = np.zeros_like(
        time_s
    )

    duty = np.zeros_like(
        time_s
    )

    for i in range(len(time_s)):

        raw_duty[i], duty[i] = (
            pi_output(
                error_hz[i],
                integral_error[i],
                controller_params,
            )
        )

    dump_command_kw = (
        average_dump_power_kw(
            duty,
            elc_params.dump_load,
        )
    )

    consumer_power_kw = np.array([
        consumer_power_profile(t)
        for t in time_s
    ])

    pm_pu = np.array([
        mechanical_power_profile(t)
        for t in time_s
    ])

    electrical_power_kw = (
        consumer_power_kw
        + dump_power_kw
    )

    pe_pu = (
        electrical_power_kw
        / generator_params.rated_power_kw
    )

    power_mismatch_pu = (
        pm_pu
        - pe_pu
    )

    rocof_hz_s = np.gradient(
        frequency_hz,
        time_s,
    )

    return pd.DataFrame({
        "time_s": time_s,
        "frequency_hz": frequency_hz,
        "error_hz": error_hz,
        "omega_pu": omega_pu,
        "delta_rad": delta_rad,
        "integral_error_hz_s": integral_error,
        "raw_duty": raw_duty,
        "duty": duty,
        "dump_command_kw": dump_command_kw,
        "dump_power_kw": dump_power_kw,
        "consumer_power_kw": consumer_power_kw,
        "electrical_power_kw": electrical_power_kw,
        "pm_pu": pm_pu,
        "pe_pu": pe_pu,
        "power_mismatch_pu": power_mismatch_pu,
        "rocof_hz_s": rocof_hz_s,
    })
