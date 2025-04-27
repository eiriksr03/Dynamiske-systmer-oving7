from pythonfmu import Fmi2Slave, Real, Fmi2Causality

class cart(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.initial_position = 0
        self.initial_velocity = 0
        self.mass = 1
        self.position = 0
        self.velocity = 0
        self.acceleration = 0
        self.force = [0.0, 0.0]

        self.register_variable(Real("mass", causality=Fmi2Causality.parameter))
        self.register_variable(Real("initial_position", causality=Fmi2Causality.parameter))
        self.register_variable(Real("initial_velocity", causality=Fmi2Causality.parameter))
        self.register_variable(Real("position", causality=Fmi2Causality.output))
        self.register_variable(Real("velocity", causality=Fmi2Causality.output))
        self.register_variable(Real("acceleration", causality=Fmi2Causality.output))
        self.register_variable(Real("force[0]",
                                    setter=lambda x: self.set_force(0, x),
                                    getter=lambda: self.force[0],
                                    causality=Fmi2Causality.input))

        self.register_variable(Real("force[1]",
                                    setter=lambda x: self.set_force(1, x),
                                    getter=lambda: self.force[1],
                                    causality=Fmi2Causality.input))

    def set_force(self, index, value):
        self.force[index] = value

    def exit_initialization_mode(self):
        self.position = self.initial_position
        self.velocity = self.initial_velocity
        self.acceleration = 0
        self.force = [0.0, 0.0]

    def do_step(self, t, dt):
        try:
            self.acceleration = sum(self.force) / (self.mass + 0.1)
            self.velocity += self.acceleration * dt
            self.position += self.velocity * dt
        except Exception as e:
            print(f"error in cart do_step: {e}")
        return True