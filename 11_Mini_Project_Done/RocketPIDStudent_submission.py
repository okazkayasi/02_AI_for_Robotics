# Optimize your PID parameters here:
pressure_tau_p = 0.729
pressure_tau_d = 1.458

# rocket_tau_p = 4.641000000000004
# rocket_tau_d = -4.640999999999998
# rocket_tau_i = 0.7865973524173118
#last chosen:  [4.6, -5.100000000000007, 0.7034826038769836]
#last chosen:  [10.599999999999998, 0.09999999999999996, 0.3999999999999996]
#98
# last chosen:  [3.4999999999999964, -7.000000000000006, 0.7348503304740923]
# 98
# last chosen:  [19.62977246966649, 0.7999999999999995, 0.4208382099999968]
# 105
# [2.3, -8.6, 2.4]
# 98
rocket_tau_p = 19.62977246966649
rocket_tau_d = 0.7999999999999995
rocket_tau_i = 0.4208382099999968

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
#            data['ErrorD'] = current_velocity
        data['ExOpt'] = optimal_velocity


    return throttle, data
