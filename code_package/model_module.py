


def model(system_response, inputs, timesteps_inputs, initial_state):
    #print('inside model')
    t, y, calculated_outputs = system_response(timesteps_inputs, inputs, initial_state)
    #print('calc succesful')
    return calculated_outputs