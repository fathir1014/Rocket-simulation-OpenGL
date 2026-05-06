from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

particles = []


def init_gl(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(58, width / height, 0.1, 4000)
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glShadeModel(GL_SMOOTH)

    glLightfv(GL_LIGHT0, GL_POSITION, [-60.0, 85.0, -110.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.88, 0.62, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.32, 0.38, 0.45, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.9, 0.82, 0.65, 1.0])

    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.25, 0.25, 0.25, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 24)

    glClearColor(0.48, 0.68, 0.92, 1.0)


def cube(x, y, z, sx, sy, sz, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glColor3f(*color)

    glBegin(GL_QUADS)

    glNormal3f(0, 0, 1)
    glVertex3f(-1, -1, 1); glVertex3f(1, -1, 1); glVertex3f(1, 1, 1); glVertex3f(-1, 1, 1)

    glNormal3f(0, 0, -1)
    glVertex3f(-1, -1, -1); glVertex3f(-1, 1, -1); glVertex3f(1, 1, -1); glVertex3f(1, -1, -1)

    glNormal3f(0, 1, 0)
    glVertex3f(-1, 1, -1); glVertex3f(-1, 1, 1); glVertex3f(1, 1, 1); glVertex3f(1, 1, -1)

    glNormal3f(0, -1, 0)
    glVertex3f(-1, -1, -1); glVertex3f(1, -1, -1); glVertex3f(1, -1, 1); glVertex3f(-1, -1, 1)

    glNormal3f(1, 0, 0)
    glVertex3f(1, -1, -1); glVertex3f(1, 1, -1); glVertex3f(1, 1, 1); glVertex3f(1, -1, 1)

    glNormal3f(-1, 0, 0)
    glVertex3f(-1, -1, -1); glVertex3f(-1, -1, 1); glVertex3f(-1, 1, 1); glVertex3f(-1, 1, -1)

    glEnd()
    glPopMatrix()


def cylinder(radius, height, color, slices=48):
    glColor3f(*color)
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluCylinder(q, radius, radius, height, slices, 18)


def cone(radius, height, color):
    glColor3f(*color)
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluCylinder(q, radius, 0, height, 48, 18)


def sphere(x, y, z, radius, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluSphere(q, radius, 24, 16)
    glPopMatrix()


def draw_sky(t):
    glDisable(GL_LIGHTING)

    sphere(-72, 78, -135, 8.0, (1.0, 0.78, 0.12))
    sphere(-72, 78, -135, 11.5, (1.0, 0.55, 0.03))

    sphere(92, 60, -150, 4.6, (0.82, 0.84, 0.80))

    glEnable(GL_LIGHTING)

    draw_cloud(-42 + math.sin(t * 0.10) * 2, 45, -60, 2.4)
    draw_cloud(10 + math.sin(t * 0.08) * 2, 54, -72, 3.1)
    draw_cloud(52 + math.sin(t * 0.12) * 2, 40, -45, 2.2)
    draw_cloud(-68 + math.sin(t * 0.07) * 2, 58, -85, 2.7)


def draw_cloud(x, y, z, scale):
    sphere(x, y, z, scale * 1.30, (0.95, 0.96, 0.95))
    sphere(x + scale * 1.2, y + scale * 0.15, z, scale, (0.98, 0.98, 0.98))
    sphere(x - scale * 1.1, y, z + scale * 0.25, scale, (0.92, 0.94, 0.95))
    sphere(x + scale * 0.1, y + scale * 0.45, z - scale * 0.4, scale * 1.1, (1.0, 1.0, 1.0))


def draw_world(t):
    cube(0, -0.08, 0, 160, 0.08, 160, (0.18, 0.43, 0.22))
    cube(0, 0.02, 18, 9, 0.05, 38, (0.09, 0.09, 0.10))
    cube(0, 0.06, 0, 9, 0.08, 9, (0.36, 0.36, 0.39))
    cube(0, 0.17, 0, 3.2, 0.12, 3.2, (0.16, 0.16, 0.18))

    draw_sky(t)
    draw_launch_tower()
    draw_buildings()
    draw_site_props()


def draw_launch_tower():
    for x in [4.2, 6.2]:
        cube(x, 5.7, 0, 0.22, 5.7, 0.22, (0.58, 0.56, 0.52))
        cube(x, 5.7, 1.4, 0.22, 5.7, 0.22, (0.58, 0.56, 0.52))

    for y in [2.2, 4.2, 6.2, 8.2, 10.2]:
        cube(5.2, y, 0.7, 1.55, 0.12, 1.05, (0.64, 0.61, 0.56))

    cube(3.0, 4.1, 0.35, 2.2, 0.10, 0.16, (0.85, 0.20, 0.16))
    cube(2.8, 7.0, 0.35, 2.4, 0.10, 0.16, (0.85, 0.20, 0.16))
    cube(5.2, 11.4, 0.7, 1.7, 0.22, 1.1, (0.64, 0.61, 0.56))

    cube(11.8, 5.0, 5.5, 0.25, 5.0, 0.25, (0.62, 0.58, 0.50))
    cube(16.0, 5.0, 5.5, 0.25, 5.0, 0.25, (0.62, 0.58, 0.50))
    cube(13.9, 9.7, 5.5, 2.3, 0.18, 0.25, (0.62, 0.58, 0.50))
    cube(17.2, 8.6, 5.5, 1.2, 0.12, 0.12, (0.85, 0.18, 0.14))


def draw_buildings():
    cube(-16, 1.2, -8, 5.5, 1.2, 3.2, (0.75, 0.78, 0.78))
    cube(-16, 2.55, -8, 5.8, 0.22, 3.5, (0.18, 0.24, 0.27))
    for i in range(6):
        cube(-20.2 + i * 1.6, 1.55, -4.75, 0.32, 0.35, 0.05, (0.08, 0.32, 0.55))

    cube(-29, 2.0, 8, 6.0, 2.0, 4.0, (0.58, 0.61, 0.64))
    cube(-29, 4.15, 8, 6.3, 0.2, 4.3, (0.16, 0.18, 0.20))
    cube(-25, 4.9, 8, 0.45, 0.7, 0.45, (0.12, 0.12, 0.13))

    cube(-4, 1.8, -18, 3.6, 1.8, 2.0, (0.62, 0.65, 0.67))
    cube(-4, 3.75, -18, 3.8, 0.2, 2.2, (0.18, 0.20, 0.22))


def draw_site_props():
    for z in [-24, -18, -12, -6, 0, 6, 12, 18, 24]:
        cube(-40, 0.45, z, 0.12, 0.45, 0.12, (0.12, 0.12, 0.12))
        cube(40, 0.45, z, 0.12, 0.45, 0.12, (0.12, 0.12, 0.12))

    cube(-40, 0.9, 0, 0.08, 0.06, 25, (0.10, 0.10, 0.10))
    cube(40, 0.9, 0, 0.08, 0.06, 25, (0.10, 0.10, 0.10))

    for x in [-34, -28, -22, -16]:
        cube(x, 0.35, 18, 1.2, 0.35, 0.8, (0.78, 0.42, 0.08))
        cube(x, 1.0, 18, 1.0, 0.18, 0.65, (0.55, 0.28, 0.05))

    for x in [18, 24, 30]:
        sphere(x, 2.4, -15, 2.2, (0.72, 0.72, 0.68))
        cube(x, 0.55, -15, 0.18, 0.55, 2.8, (0.42, 0.42, 0.40))

    for z in [-4, 0, 4]:
        cube(11, 0.28, z, 6.0, 0.12, 0.12, (0.55, 0.55, 0.52))
        cube(17, 0.28, z, 0.12, 0.12, 4.2, (0.55, 0.55, 0.52))

    cube(-8, 0.45, 11, 1.2, 0.35, 0.65, (0.95, 0.78, 0.12))
    cube(-8.3, 0.9, 11, 0.55, 0.35, 0.5, (0.10, 0.22, 0.35))
    cube(13, 0.55, 9, 1.6, 0.45, 0.7, (0.86, 0.14, 0.12))
    cube(13, 1.05, 9, 0.8, 0.35, 0.52, (0.12, 0.18, 0.24))


def draw_rocket(altitude, engine_on, phase):
    glPushMatrix()
    glTranslatef(0, altitude + 0.35, 0)
    glRotatef(-90, 1, 0, 0)

    cylinder(0.54, 6.0, (0.91, 0.93, 0.94))
    cylinder(0.31, 5.8, (0.86, 0.10, 0.08))

    glPushMatrix()
    glTranslatef(0, 0, 6.0)
    cone(0.54, 1.3, (0.88, 0.12, 0.10))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, -0.22)
    cylinder(0.40, 0.30, (0.08, 0.08, 0.09))
    glPopMatrix()

    for ang in (0, 120, 240):
        r = math.radians(ang)
        x = math.cos(r)
        y = math.sin(r)
        glColor3f(0.86, 0.12, 0.10)
        glBegin(GL_TRIANGLES)
        glNormal3f(x, y, 0)
        glVertex3f(x * 0.47, y * 0.47, 0.35)
        glVertex3f(x * 1.18, y * 1.18, -0.78)
        glVertex3f(x * 0.47, y * 0.47, 1.85)
        glEnd()

    sphere(0, 0.56, 4.30, 0.17, (0.04, 0.08, 0.14))

    if engine_on:
        glDisable(GL_LIGHTING)

        flame = 1.8 + random.random() * 1.5
        if phase == "LANDING_BURN":
            flame *= 0.65

        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.90, 0.20)
        glVertex3f(-0.30, 0, -0.18)
        glVertex3f(0.30, 0, -0.18)
        glColor3f(1.0, 0.16, 0.02)
        glVertex3f(0, 0, -flame)
        glEnd()

        glBegin(GL_TRIANGLES)
        glColor3f(0.35, 0.65, 1.0)
        glVertex3f(-0.14, 0, -0.16)
        glVertex3f(0.14, 0, -0.16)
        glColor3f(0.9, 0.98, 1.0)
        glVertex3f(0, 0, -flame * 0.48)
        glEnd()

        glEnable(GL_LIGHTING)

    glPopMatrix()


def spawn_engine_particles(altitude, phase):
    count = 13 if phase == "ASCENT" else 7
    spread = 1.20 if phase == "ASCENT" else 0.65

    for _ in range(count):
        particles.append({
            "x": random.uniform(-spread, spread),
            "y": max(0, altitude + random.uniform(-0.35, 0.2)),
            "z": random.uniform(-spread, spread),
            "size": random.uniform(0.22, 0.58),
            "life": 1.0,
            "kind": "smoke"
        })


def spawn_cooling_particles():
    for _ in range(6):
        particles.append({
            "x": random.uniform(-1.6, 1.6),
            "y": random.uniform(0.2, 1.4),
            "z": random.uniform(-1.6, 1.6),
            "size": random.uniform(0.12, 0.34),
            "life": 0.85,
            "kind": "steam"
        })


def draw_particles(dt):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_LIGHTING)

    for p in particles[:]:
        p["x"] += random.uniform(-1.2, 1.2) * dt
        p["y"] += (1.0 if p["kind"] == "steam" else -0.35) * dt
        p["z"] += random.uniform(-1.2, 1.2) * dt
        p["size"] += (1.7 if p["kind"] == "smoke" else 0.95) * dt
        p["life"] -= (0.34 if p["kind"] == "smoke" else 0.55) * dt

        if p["life"] <= 0:
            particles.remove(p)
            continue

        if p["kind"] == "smoke":
            glColor4f(0.48, 0.48, 0.48, p["life"])
        else:
            glColor4f(0.85, 0.92, 1.0, p["life"])

        glPushMatrix()
        glTranslatef(p["x"], p["y"], p["z"])
        q = gluNewQuadric()
        gluSphere(q, p["size"], 12, 8)
        glPopMatrix()

    glEnable(GL_LIGHTING)
    glDisable(GL_BLEND)


def draw_hud(width, height, rocket):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    panel(18, 18, 270, 92, (0.02, 0.03, 0.04))
    bar(38, 48, 210, 12, rocket.fuel / rocket.max_fuel, (1.0, 0.45, 0.05))
    bar(38, 76, 210, 12, min(1, rocket.altitude / 135), (0.20, 0.65, 1.0))

    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def panel(x, y, w, h, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()


def bar(x, y, w, h, ratio, color):
    panel(x, y, w, h, (0.16, 0.16, 0.16))
    panel(x, y, w * max(0, min(1, ratio)), h, color)
