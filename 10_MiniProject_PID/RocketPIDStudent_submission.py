# Optimize your PID parameters here:
pressure_tau_p = 0.729
pressure_tau_d = 1.458

rocket_tau_p = 4.
rocket_tau_i = 0.5
rocket_tau_d = 1.


def pressure_pd_solution(delta_t, current_pressure, data, n = 300):
    """Student solution to maintain LOX pressure to the turbopump at a level of 100.

    Args:
        delta_t (float): Time step length.
        current_pressure (float): Current pressure level of the turbopump.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0
    """
    if (data['ErrorP'] == 0 and data['ErrorD']== 0):
        diff = 0
        adjust_pressure = - pressure_tau_p * (current_pressure - 100) - pressure_tau_d * diff
        data['ErrorP'] = current_pressure
        data['ErrorD'] = diff
    else:
        diff = current_pressure - data['ErrorP']
        adjust_pressure = -pressure_tau_p * (current_pressure - 100) - pressure_tau_d * diff
        data['ErrorP'] = current_pressure
        data['ErrorD'] = diff

    return adjust_pressure, data

def rocket_pid_solution(delta_t, current_velocity, optimal_velocity, data):
    """Student solution for maintaining rocket throttle through out the launch based on an optimal flight path

    Args:
        delta_t (float): Time step length.
        current_velocity (float): Current velocity of rocket.
        optimal_velocity (float): Optimal velocity of rocket.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorI': Integral error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0

    Returns:
        Throttle to set, data dictionary to be passed through run.
    """
    a = data
    if data['ErrorP'] == 0 and data['ErrorI'] == 0 and data['ErrorD'] == 0:
        diff = 0
        data['ErrorP'] = current_velocity - optimal_velocity 
        throttle = -rocket_tau_p * data['ErrorP'] - rocket_tau_d * diff - rocket_tau_i * data['ErrorI']
        data['ErrorI'] += data['ErrorP']
        data['ErrorD'] = current_velocity
        data['ExOpt'] = optimal_velocity
    else:
        diff = current_velocity - data['ErrorD']
        data['ErrorP'] = current_velocity - optimal_velocity
        data['ErrorI'] += data['ErrorP']
        throttle = -rocket_tau_p * data['ErrorP'] - rocket_tau_d * diff - rocket_tau_i * data['ErrorI']
        data['ErrorD'] = current_velocity
        if optimal_velocity != data['ExOpt']:
            data['ErrorI'] = 0
            data['ErrorD'] = current_velocity
        data['ExOpt'] = optimal_velocity
    

    return throttle, data
