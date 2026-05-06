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
    camera_distance = 38.0

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

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
            camera_angle -= 45 * dt
        if keys[K_d]:
            camera_angle += 45 * dt
        if keys[K_w]:
            camera_distance = max(20, camera_distance - 18 * dt)
        if keys[K_s]:
            camera_distance = min(75, camera_distance + 18 * dt)

        rocket.update(dt)

        if rocket.engine_on:
            spawn_engine_particles(rocket.altitude, rocket.phase)

        if rocket.cooling:
            spawn_cooling_particles()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        angle = math.radians(camera_angle)
        cam_x = math.sin(angle) * camera_distance
        cam_z = math.cos(angle) * camera_distance
        cam_y = max(14, rocket.altitude * 0.48 + 15)

        gluLookAt(
            cam_x, cam_y, cam_z,
            0, rocket.altitude + 4, 0,
            0, 1, 0
        )

        draw_world(rocket.time)
        draw_rocket(rocket.altitude, rocket.engine_on, rocket.phase)
        draw_particles(dt)
        draw_hud(WIDTH, HEIGHT, rocket)

        pygame.display.set_caption(
            f"Rocket Launch Simulation | {rocket.phase} | "
            f"Altitude {rocket.altitude:.1f} m | Fuel {rocket.fuel:.1f} kg"
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
