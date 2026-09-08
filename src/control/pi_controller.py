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
    Numerically robust conditional-integration
    anti-windup.

    Integrator dihentikan ketika PI telah mencapai
    batas aktuator dan arah integrasi akan mendorong
    output semakin jauh ke daerah saturasi.

    Toleransi kecil digunakan di sekitar batas
    untuk mencegah numerical chattering.
    """

    output_rate_sign = (
        params.control_direction
        * params.ki
        * error_hz
    )

    eps = 1e-6

    at_lower_limit = (
        raw_output
        <= params.output_min + eps
    )

    at_upper_limit = (
        raw_output
        >= params.output_max - eps
    )

    if (
        at_lower_limit
        and output_rate_sign < 0.0
    ):
        return 0.0

    if (
        at_upper_limit
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
        rtol=1e-6,
        atol=1e-8,
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


# ============================================================
# DETERMINISTIC FIXED-STEP RK4 SOLVER
# ============================================================

def simulate_pi_elc_closed_loop_rk4(
    controller_params,
    generator_params,
    elc_params,
    mechanical_power_profile,
    consumer_power_profile,
    t_end_s=10.0,
    dt_s=0.01,
    initial_omega_pu=1.0,
    initial_delta_rad=0.0,
    initial_integral_error_hz_s=0.0,
    initial_dump_power_kw=None,
):
    """
    Deterministic fixed-step fourth-order Runge-Kutta
    solver for the PLTMH-ELC-PI closed-loop model.

    This solver is intended for deterministic dataset
    generation, including operating points at the ELC
    actuator boundary where adaptive solve_ivp may suffer
    excessive step rejection.

    Default integration step:
        dt_s = 0.01 s
    """

    import numpy as np
    import pandas as pd

    from src.plant.dump_load import (
        average_dump_power_kw,
    )

    if dt_s <= 0.0:
        raise ValueError(
            "dt_s must be positive."
        )

    n_steps_float = (
        t_end_s / dt_s
    )

    n_steps = int(
        round(
            n_steps_float
        )
    )

    if not np.isclose(
        n_steps * dt_s,
        t_end_s,
        atol=1e-12,
    ):
        raise ValueError(
            "t_end_s must be an integer "
            "multiple of dt_s."
        )


    # --------------------------------------------------------
    # Initial condition
    # --------------------------------------------------------

    initial_frequency_hz = (
        generator_params.nominal_frequency_hz
        * initial_omega_pu
    )

    initial_error_hz = (
        controller_params.reference_frequency_hz
        - initial_frequency_hz
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


    x = np.array(
        [
            initial_omega_pu,
            initial_delta_rad,
            initial_dump_power_kw,
            initial_integral_error_hz_s,
        ],
        dtype=float,
    )


    # --------------------------------------------------------
    # Time/state arrays
    # --------------------------------------------------------

    time_s = np.linspace(
        0.0,
        t_end_s,
        n_steps + 1,
    )

    states = np.zeros(
        (
            n_steps + 1,
            4,
        ),
        dtype=float,
    )

    states[0] = x


    # --------------------------------------------------------
    # Fixed-step RK4 integration
    # --------------------------------------------------------

    for i in range(
        n_steps
    ):

        t = time_s[i]

        h = (
            time_s[i + 1]
            - time_s[i]
        )

        k1 = closed_loop_rhs(
            t,
            x,
            controller_params,
            generator_params,
            elc_params,
            mechanical_power_profile,
            consumer_power_profile,
        )

        k2 = closed_loop_rhs(
            t + 0.5 * h,
            x + 0.5 * h * k1,
            controller_params,
            generator_params,
            elc_params,
            mechanical_power_profile,
            consumer_power_profile,
        )

        k3 = closed_loop_rhs(
            t + 0.5 * h,
            x + 0.5 * h * k2,
            controller_params,
            generator_params,
            elc_params,
            mechanical_power_profile,
            consumer_power_profile,
        )

        k4 = closed_loop_rhs(
            np.nextafter(t + h, t),
            x + h * k3,
            controller_params,
            generator_params,
            elc_params,
            mechanical_power_profile,
            consumer_power_profile,
        )

        x = (
            x
            + (h / 6.0)
            * (
                k1
                + 2.0 * k2
                + 2.0 * k3
                + k4
            )
        )

        if not np.isfinite(
            x
        ).all():

            raise FloatingPointError(
                "Non-finite state encountered "
                f"at t={time_s[i + 1]:.6f} s."
            )

        states[
            i + 1
        ] = x


    # --------------------------------------------------------
    # State extraction
    # --------------------------------------------------------

    omega_pu = (
        states[:, 0]
    )

    delta_rad = (
        states[:, 1]
    )

    dump_power_kw = (
        states[:, 2]
    )

    integral_error_hz_s = (
        states[:, 3]
    )


    frequency_hz = (
        generator_params.nominal_frequency_hz
        * omega_pu
    )

    error_hz = (
        controller_params.reference_frequency_hz
        - frequency_hz
    )


    # --------------------------------------------------------
    # PI output reconstruction
    # --------------------------------------------------------

    raw_duty = np.zeros_like(
        time_s
    )

    duty = np.zeros_like(
        time_s
    )


    for i in range(
        len(time_s)
    ):

        (
            raw_duty[i],
            duty[i],
        ) = pi_output(
            error_hz[i],
            integral_error_hz_s[i],
            controller_params,
        )


    dump_command_kw = (
        average_dump_power_kw(
            duty,
            elc_params.dump_load,
        )
    )


    # --------------------------------------------------------
    # Power trajectories
    # --------------------------------------------------------

    consumer_power_kw = np.array(
        [
            consumer_power_profile(t)
            for t in time_s
        ],
        dtype=float,
    )

    pm_pu = np.array(
        [
            mechanical_power_profile(t)
            for t in time_s
        ],
        dtype=float,
    )

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


    # --------------------------------------------------------
    # Physics-based RoCoF
    #
    # frequency_hz = f_nom * omega_pu
    #
    # Therefore:
    #
    # df/dt = f_nom * d(omega_pu)/dt
    #
    # The state derivative is evaluated directly from
    # the closed-loop dynamic model instead of applying
    # numerical differentiation to sampled frequency.
    # --------------------------------------------------------

    rocof_hz_s = np.zeros_like(
        time_s,
        dtype=float,
    )

    for i, t in enumerate(
        time_s
    ):

        dxdt = closed_loop_rhs(
            t,
            states[i],

            controller_params,
            generator_params,
            elc_params,

            mechanical_power_profile,
            consumer_power_profile,
        )

        rocof_hz_s[i] = (
            generator_params
            .nominal_frequency_hz
            * float(
                dxdt[0]
            )
        )


    # --------------------------------------------------------
    # Return same data structure as solve_ivp implementation
    # --------------------------------------------------------

    return pd.DataFrame({
        "time_s":
            time_s,

        "frequency_hz":
            frequency_hz,

        "error_hz":
            error_hz,

        "omega_pu":
            omega_pu,

        "delta_rad":
            delta_rad,

        "integral_error_hz_s":
            integral_error_hz_s,

        "raw_duty":
            raw_duty,

        "duty":
            duty,

        "dump_command_kw":
            dump_command_kw,

        "dump_power_kw":
            dump_power_kw,

        "consumer_power_kw":
            consumer_power_kw,

        "electrical_power_kw":
            electrical_power_kw,

        "pm_pu":
            pm_pu,

        "pe_pu":
            pe_pu,

        "power_mismatch_pu":
            power_mismatch_pu,

        "rocof_hz_s":
            rocof_hz_s,
    })

