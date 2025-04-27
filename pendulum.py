from pythonfmu import Fmi2Slave, Real, Fmi2Causality
import math


class pendulum(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pendulum_mass = 0.1
        self.pendulum_length = 1
        self.gravity = 9.81
        self.initial_angle = 20 * math.pi / 180
        self.angle = 20 * math.pi / 180
        self.angle_velocity = 0
        self.cart_acceleration = 0
        self.force_on_cart = 0

        self.register_variable(Real("initial_angle", causality=Fmi2Causality.parameter))
        self.register_variable(Real("angle", causality=Fmi2Causality.output))
        self.register_variable(Real("pendulum_mass", causality=Fmi2Causality.parameter))
        self.register_variable(Real("pendulum_length", causality=Fmi2Causality.parameter))
        self.register_variable(Real("gravity", causality=Fmi2Causality.parameter))
        self.register_variable(Real("angle_velocity", causality=Fmi2Causality.output))
        self.register_variable(Real("force_on_cart", causality=Fmi2Causality.output))
        self.register_variable(Real("cart_acceleration", setter=lambda x: setattr(self, "cart_acceleration", x),
                                    getter=lambda: self.cart_acceleration,
                                    causality=Fmi2Causality.input))

    def exit_initialization_mode(self):
        self.angle = self.initial_angle
        self.angle_velocity = 0
        self.force_on_cart = 0

    def do_step(self, t, dt):
        m = self.pendulum_mass
        g = self.gravity
        l = self.pendulum_length

        angle_acceleration = (g * math.sin(self.angle) - self.cart_acceleration * math.cos(self.angle)) / l
        self.angle_velocity += angle_acceleration * dt
        self.angle += self.angle_velocity * dt
        self.force_on_cart = m * l * (
                    math.sin(self.angle) * self.angle_velocity ** 2 - math.cos(self.angle) * angle_acceleration)
        return True