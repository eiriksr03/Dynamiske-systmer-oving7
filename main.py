from ecospy import EcosSimulation, EcosSimulationStructure
from ecospy.plotter import Plotter, TimeSeriesConfig
import math

if __name__ == '__main__':

    ss = EcosSimulationStructure()
    ss.add_model("cart", "cart.fmu" )
    ss.add_model("pendulum", "pendulum.fmu")
    ss.add_model("regulator", "regulator.fmu")

    ss.make_real_connection("cart::acceleration", "pendulum::cart_acceleration")
    ss.make_real_connection("regulator::control_force", "cart::force[0]")
    ss.make_real_connection("pendulum::force_on_cart", "cart::force[1]")
    ss.make_real_connection("cart::position", "regulator::cart_position")
    ss.make_real_connection("cart::velocity", "regulator::cart_velocity")
    ss.make_real_connection("pendulum::angle", "regulator::pendulum_angle")
    ss.make_real_connection("pendulum::angle_velocity", "regulator::angle_velocity")

    parameters = {
    "cart::initial_position" : 0,
    "cart::initial_velocity": 0,
    "pendulum::angle_velocity": 0,
    "pendulum::initial_angle": 20*math.pi/180,
    "pendulum::pendulum_length": 1,
    "pendulum::pendulum_mass": 0.1,
    "pendulum::gravity": 9.81,
    "cart::mass": 1,
    "regulator::k1": -1,
    "regulator::k2": -2,
    "regulator::k3": -30,
    "regulator::k4": -10,
    }

    ss.add_parameter_set("initialValues", parameters)
    result_file = "results.csv"

    with EcosSimulation(structure = ss, step_size = 1/100) as sim:
        sim.add_csv_writer(result_file)
        sim.init(parameter_set = "initialValues")
        sim.step_until(1.1)
        sim.terminate()

    config = TimeSeriesConfig(
            title = "cart pendulum",
            y_label = "position[m] / angle (rad)",
            identifiers = ["cart::position", "pendulum::angle"])
    plotter = Plotter(result_file, config)
    plotter.show()