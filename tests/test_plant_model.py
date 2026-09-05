
import numpy as np

from src.plant import (
    PlantParams,
    nominal_flow_m3_s,
    mechanical_power_w,
    constant_profile,
    step_profile,
    simulate_plant,
)


def test_nominal_hydraulic_power():

    params = PlantParams()

    q_nom = nominal_flow_m3_s(
        params
    )

    pm_kw = (
        mechanical_power_w(
            q_nom,
            params
        )
        / 1000.0
    )

    assert np.isclose(
        pm_kw,
        params.rated_power_kw,
        rtol=1e-6
    )


def test_equilibrium_frequency():

    params = PlantParams()

    result = simulate_plant(
        params=params,
        pm_cmd_profile=constant_profile(
            0.80
        ),
        pe_profile=constant_profile(
            0.80
        ),
        t_end_s=5.0,
        dt_s=0.01,
        initial_pm_pu=0.80,
    )

    max_error = np.max(
        np.abs(
            result["frequency_hz"]
            - params.nominal_frequency_hz
        )
    )

    assert max_error < 1e-6


def test_load_drop_increases_frequency():

    params = PlantParams()

    result = simulate_plant(
        params=params,
        pm_cmd_profile=constant_profile(
            0.80
        ),
        pe_profile=step_profile(
            0.80,
            0.75,
            2.0
        ),
        t_end_s=5.0,
        dt_s=0.01,
        initial_pm_pu=0.80,
    )

    assert (
        result[
            "frequency_hz"
        ].iloc[-1]
        >
        params.nominal_frequency_hz
    )


def test_load_increase_decreases_frequency():

    params = PlantParams()

    result = simulate_plant(
        params=params,
        pm_cmd_profile=constant_profile(
            0.80
        ),
        pe_profile=step_profile(
            0.80,
            0.85,
            2.0
        ),
        t_end_s=5.0,
        dt_s=0.01,
        initial_pm_pu=0.80,
    )

    assert (
        result[
            "frequency_hz"
        ].iloc[-1]
        <
        params.nominal_frequency_hz
    )
