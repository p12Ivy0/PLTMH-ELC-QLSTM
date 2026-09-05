
from .microhydro_plant import (
    PlantParams,
    hydraulic_power_w,
    mechanical_power_w,
    nominal_flow_m3_s,
    constant_profile,
    step_profile,
    plant_rhs,
    simulate_plant,
)


from .synchronous_generator import (
    GeneratorParams,
    electrical_base_speed_rad_s,
    synchronous_speed_rpm,
    frequency_hz,
    rotor_speed_rpm,
    generator_rhs,
    simulate_generator,
)


from .dump_load import (
    DumpLoadParams,
    clamp_duty,
    average_dump_power_kw,
    required_duty_for_dump_power,
)


from .elc import (
    ELCParams,
    required_dump_power_kw,
    ideal_balance_duty,
    elc_actuator_rhs,
    simulate_elc_actuator,
    simulate_elc_balance,
)
