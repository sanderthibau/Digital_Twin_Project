


def model(system_response, inputs, timesteps_inputs, initial_state):
    calculated_outputs = system_response(inputs, timesteps_inputs, initial_state)
    return calculated_outputs