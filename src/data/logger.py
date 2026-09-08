from typing import Iterable

import numpy as np
import pandas as pd

from ..control import (
    PIControllerParams,
    simulate_pi_elc_closed_loop,
)

from ..plant import (
    GeneratorParams,
    ELCParams,
)

from ..simulation import DatasetScenario


DEFAULT_KP_VALUES = (
    0.04,
    0.07,
    0.10,
    0.13,
    0.16,
)

DEFAULT_KI_VALUES = (
    0.20,
    0.35,
    0.50,
    0.65,
    0.80,
)


def performance_metrics(
    result: pd.DataFrame,
    disturbance_time_s: float,
    reference_frequency_hz: float = 50.0,
    settling_band_hz: float = 0.05,
    required_final_duty: float | None = None,
    boundary_threshold: float = 1e-4,
):
    """
    Closed-loop performance metrics after disturbance.

    saturation_fraction:
        Total fraction of samples located at either
        physical actuator boundary. This is retained
        as a diagnostic quantity.

    avoidable_saturation_fraction:
        Boundary occupancy that is not required by
        the final physical operating point.

        - required final duty at lower boundary:
          only upper-bound occupancy is penalized.

        - required final duty at upper boundary:
          only lower-bound occupancy is penalized.

        - interior final operating point:
          both boundaries are penalized.

    If required_final_duty is not supplied, the
    legacy interpretation is retained and all
    boundary occupancy is treated as avoidable.
    """

    post = result[
        result["time_s"]
        >= disturbance_time_s
    ].copy()

    deviation = (
        post["frequency_hz"]
        - reference_frequency_hz
    )

    deviation_array = (
        deviation.to_numpy()
    )

    rmse_hz = float(
        np.sqrt(
            np.mean(
                deviation_array ** 2
            )
        )
    )

    peak_hz = float(
        np.max(
            np.abs(
                deviation_array
            )
        )
    )

    final_abs_error_hz = float(
        abs(
            deviation_array[-1]
        )
    )

    max_rocof_hz_s = float(
        np.max(
            np.abs(
                post[
                    "rocof_hz_s"
                ].to_numpy()
            )
        )
    )

    outside = post[
        np.abs(deviation)
        > settling_band_hz
    ]

    available_horizon_s = float(
        post["time_s"].iloc[-1]
        - disturbance_time_s
    )

    if len(outside) == 0:

        settling_time_s = 0.0

    elif (
        outside["time_s"].iloc[-1]
        >= post["time_s"].iloc[-1]
        - 1e-9
    ):

        settling_time_s = (
            available_horizon_s
        )

    else:

        settling_time_s = float(
            outside["time_s"].iloc[-1]
            - disturbance_time_s
        )


    # --------------------------------------------------------
    # Actuator-boundary diagnostics
    # --------------------------------------------------------

    duty = (
        post["duty"]
        .to_numpy(dtype=float)
    )

    lower_boundary = (
        duty
        <= boundary_threshold
    )

    upper_boundary = (
        duty
        >= 1.0 - boundary_threshold
    )


    lower_boundary_fraction = float(
        np.mean(
            lower_boundary
        )
    )

    upper_boundary_fraction = float(
        np.mean(
            upper_boundary
        )
    )

    saturation_fraction = float(
        np.mean(
            lower_boundary
            | upper_boundary
        )
    )


    # --------------------------------------------------------
    # Boundary-aware saturation penalty
    # --------------------------------------------------------

    if required_final_duty is None:

        avoidable_saturation_fraction = (
            saturation_fraction
        )

        required_boundary = (
            "UNKNOWN"
        )

    else:

        required_final_duty = float(
            required_final_duty
        )

        if (
            required_final_duty
            <= boundary_threshold
        ):

            # Lower boundary is physically required.
            # Only upper-bound occupancy is avoidable.
            avoidable_saturation_fraction = (
                upper_boundary_fraction
            )

            required_boundary = (
                "LOWER"
            )

        elif (
            required_final_duty
            >= 1.0 - boundary_threshold
        ):

            # Upper boundary is physically required.
            # Only lower-bound occupancy is avoidable.
            avoidable_saturation_fraction = (
                lower_boundary_fraction
            )

            required_boundary = (
                "UPPER"
            )

        else:

            # Final operating point is interior.
            # Any actuator-boundary occupancy
            # remains penalized.
            avoidable_saturation_fraction = (
                saturation_fraction
            )

            required_boundary = (
                "INTERIOR"
            )


    duty_total_variation = float(
        np.sum(
            np.abs(
                np.diff(duty)
            )
        )
    )

    frequency = (
        post["frequency_hz"]
        .to_numpy()
    )

    stable = bool(
        np.all(
            np.isfinite(
                frequency
            )
        )
        and
        np.min(frequency) > 45.0
        and
        np.max(frequency) < 55.0
    )


    return {
        "rmse_hz":
            rmse_hz,

        "peak_abs_deviation_hz":
            peak_hz,

        "final_abs_error_hz":
            final_abs_error_hz,

        "max_rocof_hz_s":
            max_rocof_hz_s,

        "settling_time_s":
            settling_time_s,

        "available_horizon_s":
            available_horizon_s,

        # Diagnostic actuator-boundary metrics
        "lower_boundary_fraction":
            lower_boundary_fraction,

        "upper_boundary_fraction":
            upper_boundary_fraction,

        "saturation_fraction":
            saturation_fraction,

        # Quantity used by gain objective
        "avoidable_saturation_fraction":
            avoidable_saturation_fraction,

        "required_boundary":
            required_boundary,

        "duty_total_variation":
            duty_total_variation,

        "stable":
            stable,
    }
def deterministic_gain_score(
    metrics: dict
) -> float:
    """
    Deterministic objective for gain labeling.

    All physical quantities are normalized before
    weighted aggregation.

    Actuator-boundary penalty uses
    avoidable_saturation_fraction whenever available.
    saturation_fraction is retained only as a
    backward-compatible fallback.
    """

    if not metrics["stable"]:

        return 1e6

    horizon = max(
        metrics[
            "available_horizon_s"
        ],
        1e-9,
    )

    saturation_penalty_metric = (
        metrics.get(
            "avoidable_saturation_fraction",
            metrics["saturation_fraction"],
        )
    )

    score = (
        0.25
        * metrics["rmse_hz"]
        / 0.50

        + 0.20
        * metrics[
            "peak_abs_deviation_hz"
        ]
        / 1.00

        + 0.15
        * metrics[
            "final_abs_error_hz"
        ]
        / 0.05

        + 0.10
        * metrics[
            "max_rocof_hz_s"
        ]
        / 1.00

        + 0.10
        * metrics[
            "settling_time_s"
        ]
        / horizon

        + 0.10
        * saturation_penalty_metric

        + 0.10
        * metrics[
            "duty_total_variation"
        ]
    )

    return float(
        score
    )
def build_controller(
    scenario: DatasetScenario,
    generator_params: GeneratorParams,
    kp: float,
    ki: float,
):
    """
    PI kandidat dengan bias sesuai titik
    operasi awal skenario.
    """

    return PIControllerParams(
        kp=float(kp),
        ki=float(ki),

        reference_frequency_hz=(
            generator_params
            .nominal_frequency_hz
        ),

        output_bias=(
            scenario.initial_dump_power_kw
            / scenario.rated_power_kw
        ),

        output_min=0.0,
        output_max=1.0,
        control_direction=-1.0,
    )


def select_best_gain(
    scenario: DatasetScenario,
    generator_params: GeneratorParams,
    elc_params: ELCParams,
    kp_values: Iterable[float] = DEFAULT_KP_VALUES,
    ki_values: Iterable[float] = DEFAULT_KI_VALUES,
    scoring_dt_s: float = 0.01,
):
    """
    Exhaustive deterministic grid evaluation.

    Uses the validated deterministic fixed-step RK4
    solver for candidate-gain evaluation.

    Tidak menggunakan algoritma metaheuristik.
    """

    from src.control.pi_controller import (
        simulate_pi_elc_closed_loop_rk4,
    )

    rows = []

    for kp in kp_values:

        for ki in ki_values:

            controller = build_controller(
                scenario,
                generator_params,
                kp,
                ki,
            )

            result = (
                simulate_pi_elc_closed_loop_rk4(
                    controller_params=controller,
                    generator_params=generator_params,
                    elc_params=elc_params,

                    mechanical_power_profile=(
                        scenario
                        .mechanical_power_profile()
                    ),

                    consumer_power_profile=(
                        scenario
                        .consumer_power_profile()
                    ),

                    t_end_s=(
                        scenario.duration_s
                    ),

                    dt_s=scoring_dt_s,

                    initial_dump_power_kw=(
                        scenario
                        .initial_dump_power_kw
                    ),
                )
            )

            required_final_dump_kw = (
                scenario.mechanical_power_kw
                - scenario.final_consumer_power_kw
            )

            required_final_duty = (
                required_final_dump_kw
                / scenario.rated_power_kw
            )

            metrics = performance_metrics(
                result=result,

                disturbance_time_s=(
                    scenario
                    .disturbance_time_s
                ),

                reference_frequency_hz=(
                    generator_params
                    .nominal_frequency_hz
                ),

                required_final_duty=(
                    required_final_duty
                ),
            )

            score = (
                deterministic_gain_score(
                    metrics
                )
            )

            row = {
                "scenario_id":
                    scenario.scenario_id,

                "kp": float(kp),
                "ki": float(ki),
                "score": score,

                **metrics,
            }

            rows.append(row)

    candidate_table = (
        pd.DataFrame(rows)
        .sort_values(
            by=[
                "score",
                "kp",
                "ki",
            ],
            ascending=[
                True,
                True,
                True,
            ],
        )
        .reset_index(drop=True)
    )

    best = (
        candidate_table.iloc[0]
    )

    return (
        best,
        candidate_table,
    )

def generate_labeled_trajectory(
    scenario: DatasetScenario,
    generator_params: GeneratorParams,
    elc_params: ELCParams,
    target_kp: float,
    target_ki: float,
    label_score: float,
):
    """
    Simulasi final dengan gain label terpilih.

    Dataset mentah belum dinormalisasi dan
    belum dibuat sliding window.
    """

    controller = build_controller(
        scenario,
        generator_params,
        target_kp,
        target_ki,
    )

    result = (
        simulate_pi_elc_closed_loop(
            controller_params=controller,
            generator_params=generator_params,
            elc_params=elc_params,

            mechanical_power_profile=(
                scenario
                .mechanical_power_profile()
            ),

            consumer_power_profile=(
                scenario
                .consumer_power_profile()
            ),

            t_end_s=(
                scenario.duration_s
            ),

            dt_s=(
                scenario.dt_s
            ),

            initial_dump_power_kw=(
                scenario
                .initial_dump_power_kw
            ),
        )
    )

    result = result.copy()

    result["sample_id"] = (
        np.arange(
            len(result)
        )
    )

    result["scenario_id"] = (
        scenario.scenario_id
    )

    result["delta_f_hz"] = (
        result["frequency_hz"]
        -
        generator_params
        .nominal_frequency_hz
    )

    result["pm_kw"] = (
        result["pm_pu"]
        * generator_params
        .rated_power_kw
    )

    result["pe_kw"] = (
        result[
            "electrical_power_kw"
        ]
    )

    result["p_dump_kw"] = (
        result["dump_power_kw"]
    )

    result["target_kp"] = (
        float(target_kp)
    )

    result["target_ki"] = (
        float(target_ki)
    )

    result["label_score"] = (
        float(label_score)
    )

    result[
        "disturbance_time_s"
    ] = (
        scenario
        .disturbance_time_s
    )

    result[
        "time_since_disturbance_s"
    ] = (
        result["time_s"]
        -
        scenario
        .disturbance_time_s
    )

    # Baris sebelum gangguan tetap disimpan
    # sebagai konteks temporal, tetapi tidak
    # digunakan sebagai target supervised utama.
    result["label_valid"] = (
        result["time_since_disturbance_s"]
        >= 0.05
    )

    # Fokus transien utama untuk tahap windowing.
    result["transient_focus"] = (
        (
            result[
                "time_since_disturbance_s"
            ]
            >= 0.05
        )
        &
        (
            result[
                "time_since_disturbance_s"
            ]
            <= 3.0
        )
    )

    result[
        "mechanical_power_scenario_pu"
    ] = (
        scenario
        .mechanical_power_pu
    )

    result[
        "initial_dump_power_kw"
    ] = (
        scenario
        .initial_dump_power_kw
    )

    result[
        "load_step_kw"
    ] = (
        scenario
        .load_step_kw
    )

    return result


def generate_dataset(
    scenarios,
    generator_params: GeneratorParams,
    elc_params: ELCParams,
    kp_values=DEFAULT_KP_VALUES,
    ki_values=DEFAULT_KI_VALUES,
    scoring_dt_s: float = 0.04,
    verbose: bool = True,
):
    """
    Generate raw temporal dataset dan
    tabel label per skenario.
    """

    trajectories = []
    label_rows = []

    total = len(scenarios)

    for i, scenario in enumerate(
        scenarios,
        start=1,
    ):

        best, _ = select_best_gain(
            scenario=scenario,
            generator_params=generator_params,
            elc_params=elc_params,
            kp_values=kp_values,
            ki_values=ki_values,
            scoring_dt_s=scoring_dt_s,
        )

        target_kp = float(
            best["kp"]
        )

        target_ki = float(
            best["ki"]
        )

        score = float(
            best["score"]
        )

        trajectory = (
            generate_labeled_trajectory(
                scenario=scenario,
                generator_params=generator_params,
                elc_params=elc_params,
                target_kp=target_kp,
                target_ki=target_ki,
                label_score=score,
            )
        )

        trajectories.append(
            trajectory
        )

        label_rows.append({
            "scenario_id":
                scenario.scenario_id,

            "mechanical_power_pu":
                scenario.mechanical_power_pu,

            "mechanical_power_kw":
                scenario.mechanical_power_kw,

            "initial_consumer_power_kw":
                scenario.initial_consumer_power_kw,

            "final_consumer_power_kw":
                scenario.final_consumer_power_kw,

            "initial_dump_power_kw":
                scenario.initial_dump_power_kw,

            "load_step_kw":
                scenario.load_step_kw,

            "disturbance_time_s":
                scenario.disturbance_time_s,

            "target_kp":
                target_kp,

            "target_ki":
                target_ki,

            "label_score":
                score,

            "rmse_hz":
                float(best["rmse_hz"]),

            "peak_abs_deviation_hz":
                float(
                    best[
                        "peak_abs_deviation_hz"
                    ]
                ),

            "settling_time_s":
                float(
                    best[
                        "settling_time_s"
                    ]
                ),

            "saturation_fraction":
                float(
                    best[
                        "saturation_fraction"
                    ]
                ),
        })

        if verbose and (
            i == 1
            or i % 10 == 0
            or i == total
        ):

            print(
                f"[{i:03d}/{total:03d}] "
                f"{scenario.scenario_id} "
                f"-> Kp={target_kp:.3f}, "
                f"Ki={target_ki:.3f}"
            )

    raw_dataset = pd.concat(
        trajectories,
        ignore_index=True,
    )

    label_table = pd.DataFrame(
        label_rows
    )

    return (
        raw_dataset,
        label_table,
    )


# === FIXED_POST_DISTURBANCE_EVALUATION_WINDOW ===

DEFAULT_POST_DISTURBANCE_EVALUATION_HORIZON_S = 7.5


_performance_metrics_unwindowed = performance_metrics


def performance_metrics(
    result,
    disturbance_time_s,
    reference_frequency_hz=50.0,
    settling_band_hz=0.05,
    required_final_duty=None,
    boundary_threshold=1e-4,
    evaluation_horizon_s=(
        DEFAULT_POST_DISTURBANCE_EVALUATION_HORIZON_S
    ),
):
    """
    Compute deterministic controller-performance metrics over
    a fixed post-disturbance evaluation horizon.

    A common horizon prevents gain-selection bias when otherwise
    identical scenarios use different disturbance times.

    Parameters
    ----------
    evaluation_horizon_s : float or None
        Duration after disturbance used for metric evaluation.
        Default = 7.5 s, the maximum common post-disturbance
        horizon of the current scenario catalog.

        If None, the supplied result is evaluated without
        additional truncation.
    """

    if evaluation_horizon_s is None:

        evaluation_result = (
            result.copy()
        )

    else:

        evaluation_horizon_s = float(
            evaluation_horizon_s
        )


        if evaluation_horizon_s <= 0.0:

            raise ValueError(
                "evaluation_horizon_s must be > 0 "
                "or None."
            )


        evaluation_end_s = (
            float(
                disturbance_time_s
            )
            + evaluation_horizon_s
        )


        available_end_s = float(
            result[
                "time_s"
            ].iloc[-1]
        )


        if (
            available_end_s
            <
            evaluation_end_s - 1e-9
        ):

            raise ValueError(
                "Simulation result does not contain the "
                "requested fixed post-disturbance horizon: "
                f"required end={evaluation_end_s:.6f} s, "
                f"available end={available_end_s:.6f} s."
            )


        evaluation_result = (
            result[
                result[
                    "time_s"
                ]
                <= evaluation_end_s + 1e-12
            ]
            .copy()
            .reset_index(
                drop=True
            )
        )


    return (
        _performance_metrics_unwindowed(
            result=(
                evaluation_result
            ),

            disturbance_time_s=(
                disturbance_time_s
            ),

            reference_frequency_hz=(
                reference_frequency_hz
            ),

            settling_band_hz=(
                settling_band_hz
            ),

            required_final_duty=(
                required_final_duty
            ),

            boundary_threshold=(
                boundary_threshold
            ),
        )
    )


