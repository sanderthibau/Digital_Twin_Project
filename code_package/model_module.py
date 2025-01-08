


def model(system_response, inputs, timesteps_inputs, initial_state):
    """
    This higher order function is meant to act as a general wrapper to contain a specific model and work properly within this package.
    The model of the desired Digital Twin should be given as the system_response input. The idea is that in this way existing models can be
    implemented with a minimal amount of adjustment from functions, state space models, FMU's, machine learning algorithms, other input/output mechanisms.
    """
    #print('inside model')
    t, y, calculated_outputs = system_response(timesteps_inputs, inputs, initial_state)
    #print('calc succesful')
    return calculated_outputs