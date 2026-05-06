import math

GRAVITY = 9.81


def clamp(x, a, b):
    return a if x < a else b if x > b else x


class Rocket:
    def __init__(self):
        self.altitude = 0.0
        self.velocity = 0.0
        self.acceleration = 0.0

        # Massa & propellant (nggak super-akurat, tapi “feels” lebih roket)
        self.mass_empty = 58.0
        self.fuel = 160.0
        self.max_fuel = 160.0

        # Thrust & burn
        self.max_thrust = 5200.0
        self.burn_rate_full = 9.6  # kg/s @ throttle=1

        # Aerodynamics sederhana
        self.drag_cd = 0.36
        self.area = 0.32

        self.time = 0.0
        self.phase = "READY"

        self.engine_on = False
        self.cooling = False
        self.throttle = 0.0

        # Launch sequence timers
        self._chilldown_t = 0.0
        self._ignition_t = 0.0
        self._hold_down_t = 0.0

    @property
    def mass(self):
        return self.mass_empty + self.fuel

    def launch(self):
        # Space = mulai chilldown (pendinginan) dulu
        if self.phase == "READY":
            self.phase = "CHILLDOWN"
            self._chilldown_t = 0.0
            self._ignition_t = 0.0
            self._hold_down_t = 0.0
            self.engine_on = False
            self.cooling = True
            self.throttle = 0.0

    def _rho(self, altitude):
        # Densitas udara turun dengan ketinggian (approx)
        # rho = 1.225 * exp(-h/H), H ~ 8500m. Sim ini kecil, tapi tetap kerasa drag-nya.
        return 1.225 * math.exp(-max(0.0, altitude) / 8500.0)

    def update(self, dt):
        self.time += dt
        self.cooling = False

        thrust = 0.0

        if self.phase == "READY":
            self.engine_on = False
            self.throttle = 0.0

        elif self.phase == "CHILLDOWN":
            # venting/pendinginan dulu biar kerasa prosedural
            self.engine_on = False
            self.throttle = 0.0
            self.cooling = True
            self._chilldown_t += dt

            # durasi chilldown
            if self._chilldown_t >= 3.8:
                self.phase = "IGNITION"
                self._ignition_t = 0.0
                self._hold_down_t = 0.0

        elif self.phase == "IGNITION":
            # engine start + throttle ramp, roket masih di-hold dulu sebentar
            self.engine_on = True
            self._ignition_t += dt

            # ramp up throttle (lebih smooth)
            ramp = clamp(self._ignition_t / 2.2, 0.0, 1.0)
            self.throttle = 0.08 + 0.92 * (ramp * ramp * (3 - 2 * ramp))  # smoothstep

            self._hold_down_t += dt
            thrust = self.max_thrust * self.throttle

            # roket belum lepas clamp sampai cukup “matang”
            if self._hold_down_t >= 1.1:
                self.phase = "ASCENT"

        elif self.phase == "ASCENT":
            self.engine_on = True

            # throttle curve: awal kuat, lalu sedikit turun biar stabil
            # juga dipengaruhi speed biar nggak “rocket to the moon” terlalu cepat
            base = 0.92
            if self.altitude < 12:
                base = 0.98
            elif self.altitude < 50:
                base = 0.90
            else:
                base = 0.84

            # limiter kalau speed sudah tinggi
            speed_limit = clamp(1.0 - max(0.0, self.velocity - 55.0) * 0.008, 0.70, 1.0)
            self.throttle = clamp(base * speed_limit, 0.70, 1.0)

            thrust = self.max_thrust * self.throttle

            # cutoff condition
            if self.altitude > 155 or self.fuel <= 52:
                self.phase = "COAST"
                self.engine_on = False
                self.throttle = 0.0
                thrust = 0.0

        elif self.phase == "COAST":
            self.engine_on = False
            self.throttle = 0.0

            # masuk landing burn saat turun dan mendekat
            if self.velocity < -12 and self.altitude < 90:
                self.phase = "LANDING_BURN"
                self.engine_on = True

        elif self.phase == "LANDING_BURN":
            self.engine_on = True

            # target descent lebih halus dekat ground
            target = -5.0 if self.altitude > 25 else -3.2
            err = (target - self.velocity)  # jika terlalu cepat turun (lebih negatif), err jadi positif

            # throttle controller
            self.throttle = clamp(0.48 + err * 0.030, 0.36, 1.0)

            # extra “cooling/steam” dekat tanah (vent + dust suppression vibe)
            if self.altitude < 16:
                self.cooling = True
                self.throttle = clamp(self.throttle + 0.10, 0.36, 1.0)

            thrust = self.max_thrust * self.throttle

            # touchdown
            if self.altitude <= 0.22 and abs(self.velocity) < 8.5:
                self.altitude = 0.0
                self.velocity = 0.0
                self.acceleration = 0.0
                self.phase = "COOLDOWN"
                self.engine_on = False
                self.throttle = 0.0
                self.cooling = True
                return self.acceleration

        elif self.phase == "COOLDOWN":
            self.engine_on = False
            self.throttle = 0.0
            self.cooling = True
            return self.acceleration

        # Propellant use (proportional to throttle)
        if self.engine_on and self.fuel > 0.0:
            burn = self.burn_rate_full * max(0.0, self.throttle)
            used = min(self.fuel, burn * dt)
            self.fuel -= used
        else:
            thrust = 0.0

        # Forces
        gravity = self.mass * GRAVITY
        rho = self._rho(self.altitude)
        drag = 0.5 * rho * self.velocity * abs(self.velocity) * self.drag_cd * self.area
        net_force = thrust - gravity - drag

        # Hold-down clamp during ignition (no movement, tapi tetap “getar” via particles di render)
        if self.phase == "IGNITION" and self._hold_down_t < 1.1:
            self.acceleration = 0.0
            self.velocity = 0.0
            self.altitude = 0.0
            return self.acceleration

        self.acceleration = net_force / self.mass
        self.velocity += self.acceleration * dt
        self.altitude += self.velocity * dt

        if self.altitude < 0.0:
            self.altitude = 0.0
            self.velocity = 0.0

        return self.acceleration