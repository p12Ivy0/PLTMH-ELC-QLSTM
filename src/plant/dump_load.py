
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DumpLoadParams:
    """
    Parameter resistive dump load untuk ELC PLTMH.
    """

    rated_power_kw: float = 100.0
    duty_min: float = 0.0
    duty_max: float = 1.0

    def __post_init__(self):

        if self.rated_power_kw <= 0.0:
            raise ValueError(
                "rated_power_kw must be positive."
            )

        if not (
            0.0 <= self.duty_min
            < self.duty_max
            <= 1.0
        ):
            raise ValueError(
                "Duty limits must satisfy "
                "0 <= duty_min < duty_max <= 1."
            )


def clamp_duty(
    duty,
    params: DumpLoadParams
):
    """
    Membatasi duty cycle pada rentang fisik ELC.
    """

    value = np.clip(
        np.asarray(duty, dtype=float),
        params.duty_min,
        params.duty_max,
    )

    if value.ndim == 0:
        return float(value)

    return value


def average_dump_power_kw(
    duty,
    params: DumpLoadParams
):
    """
    Averaged PWM/IGBT dump-load model:

        P_dump = D * P_dump,rated
    """

    duty_clamped = clamp_duty(
        duty,
        params
    )

    power = (
        np.asarray(duty_clamped)
        * params.rated_power_kw
    )

    if power.ndim == 0:
        return float(power)

    return power


def required_duty_for_dump_power(
    power_kw,
    params: DumpLoadParams
):
    """
    Duty cycle yang diperlukan untuk menghasilkan
    daya dump-load tertentu.
    """

    duty = (
        np.asarray(power_kw, dtype=float)
        / params.rated_power_kw
    )

    return clamp_duty(
        duty,
        params
    )
