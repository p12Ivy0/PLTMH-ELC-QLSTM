
import numpy as np

from src.plant import (
    GeneratorParams,
    synchronous_speed_rpm,
    simulate_generator,
)


def test_synchronous_speed():

    params = GeneratorParams(
        nominal_frequency_hz=50.0,
        poles=4
    )

    assert np.isclose(
        synchronous_speed_rpm(params),
        1500.0
    )


def test_generator_equilibrium():

    params = GeneratorParams()

    result = simulate_generator(
        params=params,
        pm_profile=lambda t: 0.80,
        pe_profile=lambda t: 0.80,
        t_end_s=3.0,
        dt_s=0.01,
    )

    max_error = np.max(
        np.abs(
            result["frequency_hz"]
            - params.nominal_frequency_hz
        )
    )

    assert max_error < 1e-6


def test_load_increase_decreases_frequency():

    params = GeneratorParams()

    result = simulate_generator(
        params=params,
        pm_profile=lambda t: 0.80,
        pe_profile=lambda t: (
            0.80 if t < 1.0 else 0.85
        ),
        t_end_s=4.0,
        dt_s=0.01,
    )

    assert (
        result["frequency_hz"].iloc[-1]
        <
        params.nominal_frequency_hz
    )


def test_load_drop_increases_frequency():

    params = GeneratorParams()

    result = simulate_generator(
        params=params,
        pm_profile=lambda t: 0.80,
        pe_profile=lambda t: (
            0.80 if t < 1.0 else 0.75
        ),
        t_end_s=4.0,
        dt_s=0.01,
    )

    assert (
        result["frequency_hz"].iloc[-1]
        >
        params.nominal_frequency_hz
    )


def test_higher_inertia_reduces_rocof():

    params_low = GeneratorParams(
        inertia_constant_s=1.5
    )

    params_high = GeneratorParams(
        inertia_constant_s=4.0
    )

    pe_profile = lambda t: (
        0.80 if t < 1.0 else 0.85
    )

    result_low = simulate_generator(
        params=params_low,
        pm_profile=lambda t: 0.80,
        pe_profile=pe_profile,
        t_end_s=2.0,
        dt_s=0.01,
    )

    result_high = simulate_generator(
        params=params_high,
        pm_profile=lambda t: 0.80,
        pe_profile=pe_profile,
        t_end_s=2.0,
        dt_s=0.01,
    )

    mask_low = (
        result_low["time_s"] >= 1.0
    )

    mask_high = (
        result_high["time_s"] >= 1.0
    )

    rocof_low = np.max(
        np.abs(
            result_low.loc[
                mask_low,
                "rocof_hz_s"
            ]
        )
    )

    rocof_high = np.max(
        np.abs(
            result_high.loc[
                mask_high,
                "rocof_hz_s"
            ]
        )
    )

    assert rocof_high < rocof_low
