GRAVITY = 9.81
RHO = 1.225


class Rocket:
    def __init__(self):
        self.altitude = 0.0
        self.velocity = 0.0
        self.acceleration = 0.0

        self.mass_empty = 42.0
        self.fuel = 110.0
        self.max_fuel = 110.0
        self.burn_rate = 7.0
        self.max_thrust = 3200.0

        self.drag_cd = 0.34
        self.area = 0.30

        self.time = 0.0
        self.phase = "READY"
        self.engine_on = False
        self.cooling = False

    @property
    def mass(self):
        return self.mass_empty + self.fuel

    def launch(self):
        if self.phase == "READY":
            self.phase = "ASCENT"
            self.engine_on = True

    def update(self, dt):
        self.time += dt
        self.cooling = False
        thrust = 0.0

        if self.phase == "ASCENT":
            self.engine_on = True
            thrust = self.max_thrust

            if self.altitude > 135 or self.fuel <= 45:
                self.phase = "COAST"
                self.engine_on = False

        elif self.phase == "COAST":
            self.engine_on = False

            if self.velocity < -10 and self.altitude < 75:
                self.phase = "LANDING_BURN"
                self.engine_on = True

        elif self.phase == "LANDING_BURN":
            self.engine_on = True

            target_descent = -4.0
            too_fast = abs(self.velocity) - abs(target_descent)
            throttle = 0.52 + too_fast * 0.035

            if self.altitude < 14:
                throttle += 0.15
                self.cooling = True

            throttle = max(0.35, min(1.0, throttle))
            thrust = self.max_thrust * throttle

            if self.altitude <= 0.18 and abs(self.velocity) < 9:
                self.altitude = 0
                self.velocity = 0
                self.acceleration = 0
                self.phase = "COOLDOWN"
                self.engine_on = False
                self.cooling = True
                return self.acceleration

        elif self.phase == "COOLDOWN":
            self.engine_on = False
            self.cooling = True
            return self.acceleration

        if self.engine_on and self.fuel > 0:
            used = min(self.fuel, self.burn_rate * dt)
            self.fuel -= used
        else:
            thrust = 0.0

        gravity = self.mass * GRAVITY
        drag = 0.5 * RHO * self.velocity * abs(self.velocity) * self.drag_cd * self.area
        net_force = thrust - gravity - drag

        self.acceleration = net_force / self.mass
        self.velocity += self.acceleration * dt
        self.altitude += self.velocity * dt

        if self.altitude < 0:
            self.altitude = 0
            self.velocity = 0

        return self.acceleration
