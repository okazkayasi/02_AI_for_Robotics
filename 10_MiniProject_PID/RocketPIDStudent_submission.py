# Optimize your PID parameters here:
pressure_tau_p = 0.1
pressure_tau_d = 0.5

rocket_tau_p = 0.
rocket_tau_i = 0.
rocket_tau_d = 0.


def pressure_pd_solution(delta_t, current_pressure, data, n = 300):
    """Student solution to maintain LOX pressure to the turbopump at a level of 100.

    Args:
        delta_t (float): Time step length.
        current_pressure (float): Current pressure level of the turbopump.
        data (dict): Data passed through out run.  Additional data can be added and existing values modified.
            'ErrorP': Proportional error.  Initialized to 0.0
            'ErrorD': Derivative error.  Initialized to 0.0
    def run(robot, tau_p, tau_d, n=100, speed=1.0):
        x_trajectory = []
        y_trajectory = []
        last = robot.y
        for i in range(n):
            diff = robot.y - last
            steering = -tau_p * robot.y - tau_d * diff
            last = robot.y
            robot.move(steering, speed)
            x_trajectory.append(robot.x)
            y_trajectory.append(robot.y)
            print robot, steering
        return x_trajectory, y_trajectory
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

    # TODO: remove naive solution
    throttle = optimal_velocity - current_velocity

    # TODO: implement PID Solution here

    return throttle, data
