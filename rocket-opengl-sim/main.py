import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from physics import Rocket
from render import (
    init_gl,
    draw_world,
    draw_rocket,
    draw_particles,
    spawn_engine_particles,
    spawn_cooling_particles,
    spawn_ignition_puffs,
    draw_hud,
)

WIDTH, HEIGHT = 1200, 760


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Rocket Launch Simulation - Python OpenGL")

    init_gl(WIDTH, HEIGHT)

    clock = pygame.time.Clock()
    rocket = Rocket()

    camera_angle = 34.0
    camera_distance = 44.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        dt = min(dt, 1.0 / 30.0)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    rocket.launch()
                elif event.key == K_r:
                    rocket = Rocket()
                elif event.key == K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[K_a]:
            camera_angle -= 55 * dt
        if keys[K_d]:
            camera_angle += 55 * dt
        if keys[K_w]:
            camera_distance = max(22, camera_distance - 22 * dt)
        if keys[K_s]:
            camera_distance = min(95, camera_distance + 22 * dt)

        rocket.update(dt)

        # Particles (lebih realistis: chilldown / ignition / ascent / landing)
        if rocket.cooling:
            spawn_cooling_particles(rocket.altitude, rocket.phase, rocket.time)

        if rocket.phase == "IGNITION":
            spawn_ignition_puffs(rocket.altitude, rocket.time)

        if rocket.engine_on:
            spawn_engine_particles(
                rocket.altitude,
                rocket.phase,
                rocket.throttle,
                rocket.velocity,
                rocket.time,
            )

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        angle = math.radians(camera_angle)
        cam_x = math.sin(angle) * camera_distance
        cam_z = math.cos(angle) * camera_distance

        # kamera naik pelan ngikutin rocket, tapi tetep cinematic
        cam_y = max(16, rocket.altitude * 0.42 + 17)

        gluLookAt(
            cam_x, cam_y, cam_z,
            0, rocket.altitude + 5.0, 0,
            0, 1, 0
        )

        draw_world(rocket.time, rocket.phase, rocket.altitude)
        draw_rocket(rocket.altitude, rocket.engine_on, rocket.phase, rocket.throttle, rocket.time)
        draw_particles(dt)
        draw_hud(WIDTH, HEIGHT, rocket)

        pygame.display.set_caption(
            f"Rocket Sim | {rocket.phase} | "
            f"Alt {rocket.altitude:.1f} m | V {rocket.velocity:.1f} m/s | "
            f"Fuel {rocket.fuel:.1f} kg | Throttle {rocket.throttle:.2f}"
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()