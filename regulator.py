from pythonfmu import Fmi2Slave, Real, Fmi2Causality


class regulator(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.k1 = -1
        self.k2 = -2
        self.k3 = -30
        self.k4 = -10

        self.cart_position = 0
        self.cart_velocity = 0
        self.pendulum_angle = 0
        self.angle_velocity = 0
        self.control_force = 0

        self.register_variable(Real("k1", causality=Fmi2Causality.parameter))
        self.register_variable(Real("k2", causality=Fmi2Causality.parameter))
        self.register_variable(Real("k3", causality=Fmi2Causality.parameter))
        self.register_variable(Real("k4", causality=Fmi2Causality.parameter))
        self.register_variable(Real("cart_position", setter=lambda x: setattr(self, "cart_position", x),
                                    getter=lambda: self.cart_position,
                                    causality=Fmi2Causality.input))
        self.register_variable(Real("cart_velocity", setter=lambda x: setattr(self, "cart_velocity", x),
                                    getter=lambda: self.cart_velocity,
                                    causality=Fmi2Causality.input))
        self.register_variable(Real("pendulum_angle", setter=lambda x: setattr(self, "pendulum_angle", x),
                                    getter=lambda: self.pendulum_angle,
                                    causality=Fmi2Causality.input))
        self.register_variable(Real("angle_velocity", setter=lambda x: setattr(self, "angle_velocity", x),
                                    getter=lambda: self.angle_velocity,
                                    causality=Fmi2Causality.input))
        self.register_variable(Real("control_force", causality=Fmi2Causality.output))

    def do_step(self, t, dt):
        k1 = self.k1
        k2 = self.k2
        k3 = self.k3
        k4 = self.k4
        position = self.cart_position
        angle_velocity = self.angle_velocity
        angle = self.pendulum_angle
        cart_velocity = self.cart_velocity

        self.control_force = -k1 * angle - k2 * angle_velocity - k3 * position - k4 * cart_velocity

        return True
