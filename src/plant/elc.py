
from dataclasses import dataclass, field
from typing import Callable, Optional

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

from .dump_load import (
    DumpLoadParams,
    average_dump_power_kw,
    clamp_duty,
)


@dataclass(frozen=True)
class ELCParams:
    """
    Parameter averaged Electronic Load Controller.
    """

    dump_load: DumpLoadParams = field(
        default_factory=DumpLoadParams
    )

    actuator_time_constant_s: float = 0.05

    def __post_init__(self):

        if self.actuator_time_constant_s <= 0.0:
            raise ValueError(
                "actuator_time_constant_s "
                "must be positive."
            )


def required_dump_power_kw(
    generator_power_kw: float,
    consumer_power_kw: float,
    params: ELCParams,
) -> float:
    """
    Ideal dump power agar:

        P_gen = P_consumer + P_dump

    Dengan batas fisik dump load.
    """

    required = (
        float(generator_power_kw)
        - float(consumer_power_kw)
    )

    required = np.clip(
        required,
        0.0,
        params.dump_load.rated_power_kw,
    )

    return float(required)


def ideal_balance_duty(
    generator_power_kw: float,
    consumer_power_kw: float,
    params: ELCParams,
) -> float:
    """
    Duty-cycle ideal untuk menjaga keseimbangan daya.
    """

    dump_power = required_dump_power_kw(
        generator_power_kw,
        consumer_power_kw,
        params,
    )

    duty = (
        dump_power
        / params.dump_load.rated_power_kw
    )

    return clamp_duty(
        duty,
        params.dump_load,
    )


def elc_actuator_rhs(
    t: float,
    x: np.ndarray,
    params: ELCParams,
    duty_profile: Callable[[float], float],
) -> np.ndarray:
    """
    First-order averaged ELC actuator.

    State:
        x[0] = actual dump-load power [kW]
    """

    actual_dump_kw = float(x[0])

    duty = clamp_duty(
        duty_profile(t),
        params.dump_load,
    )

    commanded_dump_kw = average_dump_power_kw(
        duty,
        params.dump_load,
    )

    d_dump_dt = (
        commanded_dump_kw
        - actual_dump_kw
    ) / params.actuator_time_constant_s

    return np.array([
        d_dump_dt
    ])


def simulate_elc_actuator(
    params: ELCParams,
    duty_profile: Callable[[float], float],
    t_end_s: float = 5.0,
    dt_s: float = 0.005,
    initial_dump_power_kw: float = 0.0,
) -> pd.DataFrame:
    """
    Simulasi averaged ELC actuator.
    """

    n_steps = int(
        round(t_end_s / dt_s)
    )

    t_eval = np.linspace(
        0.0,
        t_end_s,
        n_steps + 1,
    )

    solution = solve_ivp(
        fun=lambda t, x: elc_actuator_rhs(
            t,
            x,
            params,
            duty_profile,
        ),
        t_span=(0.0, t_end_s),
        y0=np.array([
            float(initial_dump_power_kw)
        ]),
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

    duty = np.array([
        clamp_duty(
            duty_profile(t),
            params.dump_load,
        )
        for t in time_s
    ])

    command_kw = average_dump_power_kw(
        duty,
        params.dump_load,
    )

    actual_kw = solution.y[0]

    return pd.DataFrame({
        "time_s": time_s,
        "duty": duty,
        "dump_command_kw": command_kw,
        "dump_power_kw": actual_kw,
    })


def simulate_elc_balance(
    params: ELCParams,
    generator_power_profile: Callable[[float], float],
    consumer_power_profile: Callable[[float], float],
    t_end_s: float = 5.0,
    dt_s: float = 0.005,
    initial_dump_power_kw: Optional[float] = None,
) -> pd.DataFrame:
    """
    Validasi ideal ELC balancing.

    CATATAN:
    Fungsi ini belum menggunakan PI.

    Duty dihitung dari keseimbangan daya ideal
    hanya untuk memvalidasi arah dan kemampuan
    actuator ELC.
    """

    def duty_profile(t: float) -> float:

        return ideal_balance_duty(
            generator_power_profile(t),
            consumer_power_profile(t),
            params,
        )

    if initial_dump_power_kw is None:

        initial_dump_power_kw = (
            average_dump_power_kw(
                duty_profile(0.0),
                params.dump_load,
            )
        )

    result = simulate_elc_actuator(
        params=params,
        duty_profile=duty_profile,
        t_end_s=t_end_s,
        dt_s=dt_s,
        initial_dump_power_kw=initial_dump_power_kw,
    )

    t = result["time_s"].to_numpy()

    generator_kw = np.array([
        generator_power_profile(time)
        for time in t
    ])

    consumer_kw = np.array([
        consumer_power_profile(time)
        for time in t
    ])

    total_electrical_kw = (
        consumer_kw
        + result["dump_power_kw"].to_numpy()
    )

    power_balance_error_kw = (
        generator_kw
        - total_electrical_kw
    )

    result["generator_power_kw"] = generator_kw
    result["consumer_power_kw"] = consumer_kw
    result["total_electrical_load_kw"] = (
        total_electrical_kw
    )

    result["power_balance_error_kw"] = (
        power_balance_error_kw
    )

    return result
