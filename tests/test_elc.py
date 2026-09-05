
import numpy as np

from src.plant import (
    DumpLoadParams,
    ELCParams,
    clamp_duty,
    average_dump_power_kw,
    required_dump_power_kw,
    ideal_balance_duty,
    simulate_elc_balance,
)


def make_params():

    return ELCParams(
        dump_load=DumpLoadParams(
            rated_power_kw=100.0
        ),
        actuator_time_constant_s=0.05,
    )


def test_duty_clipping():

    params = DumpLoadParams()

    assert clamp_duty(-0.2, params) == 0.0
    assert clamp_duty(1.2, params) == 1.0


def test_dump_power_mapping():

    params = DumpLoadParams(
        rated_power_kw=100.0
    )

    assert np.isclose(
        average_dump_power_kw(
            0.0,
            params
        ),
        0.0
    )

    assert np.isclose(
        average_dump_power_kw(
            0.5,
            params
        ),
        50.0
    )

    assert np.isclose(
        average_dump_power_kw(
            1.0,
            params
        ),
        100.0
    )


def test_required_dump_power():

    params = make_params()

    power = required_dump_power_kw(
        generator_power_kw=100.0,
        consumer_power_kw=80.0,
        params=params,
    )

    assert np.isclose(
        power,
        20.0
    )


def test_ideal_balance_duty():

    params = make_params()

    duty = ideal_balance_duty(
        generator_power_kw=100.0,
        consumer_power_kw=80.0,
        params=params,
    )

    assert np.isclose(
        duty,
        0.20
    )


def test_load_reduction_increases_dump_load():

    params = make_params()

    result = simulate_elc_balance(
        params=params,
        generator_power_profile=lambda t: 100.0,
        consumer_power_profile=lambda t: (
            80.0 if t < 1.0 else 60.0
        ),
        t_end_s=3.0,
        dt_s=0.005,
    )

    pre = result.loc[
        result["time_s"] < 0.9,
        "dump_power_kw"
    ].iloc[-1]

    post = result[
        "dump_power_kw"
    ].iloc[-1]

    assert post > pre

    assert np.isclose(
        post,
        40.0,
        atol=0.01
    )


def test_load_increase_decreases_dump_load():

    params = make_params()

    result = simulate_elc_balance(
        params=params,
        generator_power_profile=lambda t: 100.0,
        consumer_power_profile=lambda t: (
            60.0 if t < 1.0 else 90.0
        ),
        t_end_s=3.0,
        dt_s=0.005,
    )

    pre = result.loc[
        result["time_s"] < 0.9,
        "dump_power_kw"
    ].iloc[-1]

    post = result[
        "dump_power_kw"
    ].iloc[-1]

    assert post < pre

    assert np.isclose(
        post,
        10.0,
        atol=0.01
    )


def test_power_balance_settles():

    params = make_params()

    result = simulate_elc_balance(
        params=params,
        generator_power_profile=lambda t: 100.0,
        consumer_power_profile=lambda t: (
            80.0 if t < 1.0 else 60.0
        ),
        t_end_s=3.0,
        dt_s=0.005,
    )

    final_error = (
        result[
            "power_balance_error_kw"
        ].iloc[-1]
    )

    assert abs(
        final_error
    ) < 0.01


def test_elc_saturation():

    params = make_params()

    high = ideal_balance_duty(
        generator_power_kw=120.0,
        consumer_power_kw=0.0,
        params=params,
    )

    low = ideal_balance_duty(
        generator_power_kw=100.0,
        consumer_power_kw=120.0,
        params=params,
    )

    assert high == 1.0
    assert low == 0.0
