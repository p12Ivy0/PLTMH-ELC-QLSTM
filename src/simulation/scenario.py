
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class DatasetScenario:
    """
    Satu skenario operasi untuk pembentukan
    dataset supervised gain scheduling PI.
    """

    scenario_id: str
    mechanical_power_pu: float
    initial_dump_power_kw: float
    load_step_kw: float
    disturbance_time_s: float

    duration_s: float = 10.0
    dt_s: float = 0.01
    rated_power_kw: float = 100.0

    def __post_init__(self):

        if not (0.0 < self.mechanical_power_pu <= 1.0):
            raise ValueError(
                "mechanical_power_pu must be in (0, 1]."
            )

        if self.initial_dump_power_kw < 0.0:
            raise ValueError(
                "initial_dump_power_kw must be >= 0."
            )

        if not (
            0.0
            < self.disturbance_time_s
            < self.duration_s
        ):
            raise ValueError(
                "disturbance_time_s must lie "
                "inside simulation horizon."
            )

        if self.dt_s <= 0.0:
            raise ValueError(
                "dt_s must be positive."
            )

        if self.initial_consumer_power_kw < 0.0:
            raise ValueError(
                "Initial consumer power is negative."
            )

        if self.final_consumer_power_kw < 0.0:
            raise ValueError(
                "Final consumer power is negative."
            )

        if (
            self.final_consumer_power_kw
            >
            self.mechanical_power_kw + 1e-9
        ):
            raise ValueError(
                "Final consumer load exceeds "
                "mechanical power. ELC cannot "
                "supply missing power."
            )

    @property
    def mechanical_power_kw(self) -> float:

        return (
            self.mechanical_power_pu
            * self.rated_power_kw
        )

    @property
    def initial_consumer_power_kw(self) -> float:

        return (
            self.mechanical_power_kw
            - self.initial_dump_power_kw
        )

    @property
    def final_consumer_power_kw(self) -> float:

        return (
            self.initial_consumer_power_kw
            + self.load_step_kw
        )

    @property
    def initial_duty(self) -> float:

        return (
            self.initial_dump_power_kw
            / self.rated_power_kw
        )

    def mechanical_power_profile(
        self
    ) -> Callable[[float], float]:

        return lambda t: float(
            self.mechanical_power_pu
        )

    def consumer_power_profile(
        self
    ) -> Callable[[float], float]:

        def profile(t: float) -> float:

            if t < self.disturbance_time_s:

                return float(
                    self.initial_consumer_power_kw
                )

            return float(
                self.final_consumer_power_kw
            )

        return profile


def build_default_scenario_catalog():
    """
    Membangun 120 skenario deterministik.
    """

    mechanical_values = (
        0.80,
        0.85,
        0.90,
        0.95,
        1.00,
    )

    initial_dump_values = (
        20.0,
        30.0,
        40.0,
    )

    load_steps = (
        -20.0,
        -10.0,
        10.0,
        20.0,
    )

    disturbance_times = (
        1.5,
        2.5,
    )

    scenarios = []
    index = 0

    for pm_pu in mechanical_values:

        for dump_kw in initial_dump_values:

            for load_step_kw in load_steps:

                for disturbance_time_s in disturbance_times:

                    scenario = DatasetScenario(
                        scenario_id=f"S{index:03d}",
                        mechanical_power_pu=pm_pu,
                        initial_dump_power_kw=dump_kw,
                        load_step_kw=load_step_kw,
                        disturbance_time_s=disturbance_time_s,
                    )

                    scenarios.append(
                        scenario
                    )

                    index += 1

    return scenarios
