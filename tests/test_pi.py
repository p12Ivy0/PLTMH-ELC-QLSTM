
import numpy as np

from src.control import (
    PIControllerParams,
    frequency_error_hz,
    pi_output,
    pi_raw_output,
    saturate_pi_output,
    conditional_integrator_derivative,
    simulate_pi_elc_closed_loop,
)

from src.plant import (
    GeneratorParams,
    DumpLoadParams,
    ELCParams,
)


def make_system():

    controller = PIControllerParams(
        kp=0.10,
        ki=0.50,
        output_bias=0.20,
        control_direction=-1.0,
    )

    generator = GeneratorParams()

    elc = ELCParams(
        dump_load=DumpLoadParams(
            rated_power_kw=100.0
        ),
        actuator_time_constant_s=0.05,
    )

    return (
        controller,
        generator,
        elc,
    )


def test_frequency_error_sign():

    assert (
        frequency_error_hz(
            50.0,
            49.5
        )
        > 0.0
    )

    assert (
        frequency_error_hz(
            50.0,
            50.5
        )
        < 0.0
    )


def test_elc_control_direction():

    controller, _, _ = make_system()

    _, low_frequency_duty = pi_output(
        0.5,
        0.0,
        controller,
    )

    _, high_frequency_duty = pi_output(
        -0.5,
        0.0,
        controller,
    )

    assert low_frequency_duty < 0.20
    assert high_frequency_duty > 0.20


def test_pi_saturation():

    controller, _, _ = make_system()

    assert (
        saturate_pi_output(
            -10.0,
            controller
        )
        == 0.0
    )

    assert (
        saturate_pi_output(
            10.0,
            controller
        )
        == 1.0
    )


def test_anti_windup_lower_limit():

    controller, _, _ = make_system()

    raw = pi_raw_output(
        error_hz=5.0,
        integral_error_hz_s=10.0,
        params=controller,
    )

    derivative = (
        conditional_integrator_derivative(
            error_hz=5.0,
            raw_output=raw,
            params=controller,
        )
    )

    assert raw < 0.0
    assert derivative == 0.0


def test_closed_loop_equilibrium():

    controller, generator, elc = (
        make_system()
    )

    result = (
        simulate_pi_elc_closed_loop(
            controller_params=controller,
            generator_params=generator,
            elc_params=elc,
            mechanical_power_profile=lambda t: 1.0,
            consumer_power_profile=lambda t: 80.0,
            t_end_s=3.0,
            dt_s=0.005,
        )
    )

    assert np.isclose(
        result[
            "frequency_hz"
        ].iloc[-1],
        50.0,
        atol=1e-6,
    )


def test_pi_recovers_load_increase():

    controller, generator, elc = (
        make_system()
    )

    result = (
        simulate_pi_elc_closed_loop(
            controller_params=controller,
            generator_params=generator,
            elc_params=elc,
            mechanical_power_profile=lambda t: 1.0,
            consumer_power_profile=lambda t: (
                80.0
                if t < 2.0
                else 90.0
            ),
            t_end_s=10.0,
            dt_s=0.005,
        )
    )

    assert abs(
        result[
            "frequency_hz"
        ].iloc[-1]
        - 50.0
    ) < 0.05

    assert np.isclose(
        result[
            "dump_power_kw"
        ].iloc[-1],
        10.0,
        atol=0.5,
    )


def test_pi_recovers_load_decrease():

    controller, generator, elc = (
        make_system()
    )

    result = (
        simulate_pi_elc_closed_loop(
            controller_params=controller,
            generator_params=generator,
            elc_params=elc,
            mechanical_power_profile=lambda t: 1.0,
            consumer_power_profile=lambda t: (
                80.0
                if t < 2.0
                else 60.0
            ),
            t_end_s=10.0,
            dt_s=0.005,
        )
    )

    assert abs(
        result[
            "frequency_hz"
        ].iloc[-1]
        - 50.0
    ) < 0.05

    assert np.isclose(
        result[
            "dump_power_kw"
        ].iloc[-1],
        40.0,
        atol=0.5,
    )
