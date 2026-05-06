from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random

particles = []
_STARS = []


def _rand_unit_vec():
    z = random.uniform(-1.0, 1.0)
    t = random.uniform(0.0, math.tau)
    r = math.sqrt(max(0.0, 1.0 - z * z))
    return (r * math.cos(t), z, r * math.sin(t))


def clamp01(x):
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


def init_gl(width, height):
    global _STARS
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, width / height, 0.1, 6000)
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glShadeModel(GL_SMOOTH)

    # IMPORTANT: turunin diffuse + matiin specular biar gak "keputihan"
    glLightfv(GL_LIGHT0, GL_POSITION, [-0.35, 0.85, -0.40, 0.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.62, 0.60, 0.58, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.02, 0.02, 0.03, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.10, 0.10, 0.10, 1.0])

    glLightfv(GL_LIGHT1, GL_POSITION, [0.25, 0.10, 0.25, 0.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.10, 0.11, 0.13, 1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])

    # MATIIN kilap global (ini yang bikin concrete/atap jadi putih)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 1.0)

    glClearColor(0.03, 0.04, 0.065, 1.0)

    random.seed(1337)
    _STARS = []
    for _ in range(1200):
        x, y, z = _rand_unit_vec()
        if y < -0.08:
            continue
        mag = random.uniform(0.55, 1.0)
        size = 1.0 if random.random() < 0.92 else 2.0
        _STARS.append((x, y, z, mag, size))
    random.seed()


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


def sphere(x, y, z, radius, color, slices=24, stacks=16):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluSphere(q, radius, slices, stacks)
    glPopMatrix()


# ---------- SKY ----------
def draw_stars():
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    R = 1600.0
    for (x, y, z, mag, size) in _STARS:
        glPointSize(size)
        glBegin(GL_POINTS)
        glColor4f(0.9 * mag, 0.95 * mag, 1.0 * mag, 0.95)
        glVertex3f(x * R, y * R, z * R)
        glEnd()

    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)


def draw_sun_and_moon(t):
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    sun_dir = (-0.35, 0.85, -0.40)
    norm = math.sqrt(sun_dir[0] ** 2 + sun_dir[1] ** 2 + sun_dir[2] ** 2)
    sx, sy, sz = (sun_dir[0] / norm, sun_dir[1] / norm, sun_dir[2] / norm)

    R = 1500.0
    sun_x, sun_y, sun_z = sx * R, sy * R, sz * R

    sphere(sun_x, sun_y, sun_z, 18.0, (1.0, 0.70, 0.10), 20, 14)
    glColor4f(1.0, 0.65, 0.12, 0.14)
    glPushMatrix()
    glTranslatef(sun_x, sun_y, sun_z)
    q = gluNewQuadric()
    gluSphere(q, 62.0, 14, 10)
    glPopMatrix()

    glColor4f(1.0, 0.85, 0.30, 0.06)
    glPushMatrix()
    glTranslatef(sun_x, sun_y, sun_z)
    q = gluNewQuadric()
    gluSphere(q, 105.0, 14, 10)
    glPopMatrix()

    mx, my, mz = -sx * 1450.0 + 140.0, sy * 1200.0 + 35.0, -sz * 1450.0
    sphere(mx, my, mz, 22.0, (0.78, 0.80, 0.82), 18, 12)

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


def draw_thin_clouds(t):
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    base_y = 95.0
    for i in range(5):
        x = -120 + i * 60 + math.sin(t * (0.05 + i * 0.01)) * 6.0
        z = -220 - i * 55
        glColor4f(0.65, 0.70, 0.78, 0.06)
        glPushMatrix()
        glTranslatef(x, base_y + i * 3.0, z)
        glScalef(1.0, 0.65, 1.0)
        q = gluNewQuadric()
        gluSphere(q, 38.0, 18, 12)
        glPopMatrix()

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


def draw_sky(t):
    draw_stars()
    draw_sun_and_moon(t)
    draw_thin_clouds(t)


# ---------- WORLD / TERRAIN ----------
def _terrain_height(x, z):
    r = math.sqrt(x * x + z * z)
    if r < 55:
        return 0.0
    h = (
        2.2 * math.sin(0.035 * x + 0.4) +
        1.7 * math.cos(0.030 * z - 0.8) +
        1.1 * math.sin(0.022 * (x + z))
    )
    h *= clamp01((r - 55.0) / 85.0)
    return max(0.0, h)


def _terrain_color(x, z):
    n = (
        0.5 * math.sin(0.11 * x) +
        0.4 * math.cos(0.10 * z) +
        0.25 * math.sin(0.07 * (x + z))
    )
    n = (n + 1.2) / 2.4
    n = clamp01(n)
    g1 = (0.08, 0.16, 0.10)
    g2 = (0.12, 0.22, 0.13)
    r = g1[0] * (1 - n) + g2[0] * n
    g = g1[1] * (1 - n) + g2[1] * n
    b = g1[2] * (1 - n) + g2[2] * n
    return (r, g, b)


def draw_terrain():
    glDisable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)

    size = 190
    step = 10
    for x in range(-size, size, step):
        for z in range(-size, size, step):
            x0, z0 = float(x), float(z)
            x1, z1 = float(x + step), float(z + step)

            y00 = _terrain_height(x0, z0) - 0.10
            y10 = _terrain_height(x1, z0) - 0.10
            y11 = _terrain_height(x1, z1) - 0.10
            y01 = _terrain_height(x0, z1) - 0.10

            c = _terrain_color((x0 + x1) * 0.5, (z0 + z1) * 0.5)
            glColor3f(*c)

            dx = (y10 - y00)
            dz = (y01 - y00)
            nx, ny, nz = (-dx, 2.0, -dz)
            nlen = math.sqrt(nx * nx + ny * ny + nz * nz)
            if nlen > 1e-6:
                nx, ny, nz = nx / nlen, ny / nlen, nz / nlen
            glNormal3f(nx, ny, nz)

            glVertex3f(x0, y00, z0)
            glVertex3f(x1, y10, z0)
            glVertex3f(x1, y11, z1)
            glVertex3f(x0, y01, z1)

    glEnd()


def draw_tree(x, z, scale=1.0):
    y = _terrain_height(x, z)
    trunk_h = 1.8 * scale
    trunk_r = 0.18 * scale
    canopy_r = 0.95 * scale

    glPushMatrix()
    glTranslatef(x, y, z)

    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    cylinder(trunk_r, trunk_h, (0.20, 0.13, 0.08), 16)
    glPopMatrix()

    sphere(0, trunk_h + canopy_r * 0.55, 0, canopy_r, (0.10, 0.22, 0.12), 16, 12)
    sphere(0.55 * scale, trunk_h + canopy_r * 0.35, 0.2 * scale, canopy_r * 0.82, (0.09, 0.20, 0.11), 16, 12)
    sphere(-0.45 * scale, trunk_h + canopy_r * 0.35, -0.15 * scale, canopy_r * 0.78, (0.10, 0.21, 0.12), 16, 12)

    glPopMatrix()


def draw_launch_complex():
    # SUPER IMPORTANT: semua dibuat gelap (no putih)
    CONCRETE = (0.16, 0.17, 0.18)
    CONCRETE_DARK = (0.11, 0.12, 0.13)
    ASPHALT = (0.05, 0.05, 0.06)
    LINE = (0.55, 0.50, 0.18)

    WALL = (0.22, 0.23, 0.25)
    WALL_DARK = (0.16, 0.17, 0.19)
    ROOF = (0.06, 0.06, 0.07)
    GLASS = (0.05, 0.18, 0.32)

    cube(0, 0.02, 0, 16, 0.10, 16, CONCRETE)
    cube(0, 0.09, 0, 7.2, 0.07, 7.2, CONCRETE_DARK)
    cube(0, -0.02, 0, 3.0, 0.06, 3.0, (0.07, 0.07, 0.08))

    cube(0, 0.02, 24, 12, 0.06, 60, ASPHALT)
    cube(-18, 0.02, 28, 22, 0.06, 10, ASPHALT)

    for k in range(10):
        cube(0, 0.05, 6 + k * 6.0, 0.55, 0.01, 1.8, LINE)
    for k in range(5):
        cube(-18, 0.05, 22 + k * 2.2, 1.5, 0.01, 0.35, LINE)

    cube(-34, 0.02, 26, 14, 0.05, 10, (0.06, 0.06, 0.07))
    for i in range(6):
        cube(-40 + i * 2.3, 0.04, 22.5, 0.9, 0.01, 0.12, (0.42, 0.42, 0.44))
        cube(-40 + i * 2.3, 0.04, 25.0, 0.9, 0.01, 0.12, (0.42, 0.42, 0.44))
        cube(-40 + i * 2.3, 0.04, 27.5, 0.9, 0.01, 0.12, (0.42, 0.42, 0.44))

    cube(-42, 1.9, 10, 7.0, 1.9, 4.8, WALL)
    cube(-42, 4.1, 10, 7.3, 0.2, 5.1, ROOF)
    for i in range(7):
        cube(-46.7 + i * 1.55, 2.4, 14.0, 0.32, 0.44, 0.06, GLASS)

    cube(-26, 2.2, -6, 8.5, 2.2, 6.0, WALL_DARK)
    cube(-26, 4.55, -6, 8.8, 0.2, 6.3, ROOF)
    cube(-20.5, 1.4, -0.2, 2.6, 1.4, 0.15, (0.10, 0.11, 0.12))

    for z in [-40, -32, -24, -16, -8, 0, 8, 16, 24, 32, 40]:
        cube(-60, 0.60, z, 0.12, 0.60, 0.12, (0.07, 0.07, 0.07))
        cube(60, 0.60, z, 0.12, 0.60, 0.12, (0.07, 0.07, 0.07))
    cube(-60, 1.10, 0, 0.08, 0.06, 45, (0.06, 0.06, 0.06))
    cube(60, 1.10, 0, 0.08, 0.06, 45, (0.06, 0.06, 0.06))

    for x in (22, 28, 34):
        sphere(x, 2.8, -16, 2.4, (0.28, 0.28, 0.28))
        cube(x, 0.65, -16, 0.18, 0.65, 3.0, (0.18, 0.18, 0.18))
    for z in (-4, 0, 4):
        cube(11.5, 0.30, z, 6.6, 0.12, 0.12, (0.22, 0.22, 0.22))
        cube(18.5, 0.30, z, 0.12, 0.12, 4.6, (0.22, 0.22, 0.22))

    for x in (-36, -30, -24, -18):
        cube(x, 0.40, 20, 1.35, 0.40, 0.95, (0.34, 0.18, 0.06))
        cube(x, 1.08, 20, 1.05, 0.20, 0.72, (0.26, 0.13, 0.05))

    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    for x in (-10.5, 10.5):
        glColor4f(0.90, 0.82, 0.55, 0.55)
        glPushMatrix()
        glTranslatef(x, 0.45, 2.8)
        q = gluNewQuadric()
        gluSphere(q, 0.22, 10, 8)
        glPopMatrix()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


def draw_launch_tower():
    METAL = (0.22, 0.22, 0.23)
    METAL_D = (0.16, 0.16, 0.17)
    RED = (0.62, 0.12, 0.10)

    for x in [4.6, 6.8]:
        cube(x, 6.2, 0, 0.24, 6.2, 0.24, METAL)
        cube(x, 6.2, 1.7, 0.24, 6.2, 0.24, METAL)

    for y in [2.2, 4.4, 6.6, 8.8, 11.0]:
        cube(5.7, y, 0.85, 1.75, 0.12, 1.20, METAL_D)

    cube(2.9, 4.3, 0.42, 2.35, 0.10, 0.18, RED)
    cube(2.75, 7.3, 0.42, 2.55, 0.10, 0.18, RED)

    cube(5.7, 11.9, 0.85, 1.85, 0.22, 1.25, METAL)
    cube(5.7, 12.2, 0.85, 1.55, 0.06, 1.02, (0.10, 0.10, 0.11))

    cube(11.8, 5.1, 5.8, 0.25, 5.1, 0.25, METAL)
    cube(16.3, 5.1, 5.8, 0.25, 5.1, 0.25, METAL)
    cube(14.0, 9.9, 5.8, 2.5, 0.18, 0.25, METAL_D)

    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 0.22, 0.12, 0.55)
    for yy in (3.2, 6.0, 8.8, 11.2):
        glPushMatrix()
        glTranslatef(6.9, yy, 1.7)
        q = gluNewQuadric()
        gluSphere(q, 0.12, 10, 8)
        glPopMatrix()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


def draw_world(t, phase, altitude):
    draw_sky(t)
    draw_terrain()
    draw_launch_complex()
    draw_launch_tower()

    random.seed(2026)
    for _ in range(90):
        x = random.uniform(-170, 170)
        z = random.uniform(-170, 170)
        if (x * x + z * z) < (70 * 70):
            continue
        if abs(x) < 70 and -30 < z < 80:
            continue
        if _terrain_height(x, z) < 0.2:
            continue
        s = random.uniform(0.7, 1.35)
        draw_tree(x, z, s)
    random.seed()


# ---------- ROCKET ----------
def draw_rocket(altitude, engine_on, phase, throttle, t):
    glPushMatrix()
    glTranslatef(0, altitude + 0.35, 0)
    glRotatef(-90, 1, 0, 0)

    # sedikit diturunin biar gak "putih banget"
    cylinder(0.56, 6.2, (0.72, 0.74, 0.76))
    cylinder(0.32, 6.0, (0.62, 0.10, 0.08))

    glPushMatrix()
    glTranslatef(0, 0, 6.2)
    cone(0.56, 1.35, (0.66, 0.12, 0.10))
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, -0.24)
    cylinder(0.42, 0.32, (0.07, 0.07, 0.08))
    glPopMatrix()

    for ang in (0, 120, 240):
        r = math.radians(ang)
        x = math.cos(r)
        y = math.sin(r)
        glColor3f(0.66, 0.12, 0.10)
        glBegin(GL_TRIANGLES)
        glNormal3f(x, y, 0)
        glVertex3f(x * 0.50, y * 0.50, 0.40)
        glVertex3f(x * 1.22, y * 1.22, -0.82)
        glVertex3f(x * 0.50, y * 0.50, 1.95)
        glEnd()

    sphere(0, 0.60, 4.45, 0.18, (0.04, 0.08, 0.14))

    if engine_on and throttle > 0.05:
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        flick = 0.85 + (math.sin(t * 38.0) * 0.08) + random.random() * 0.05
        L = (1.4 + 3.2 * throttle) * flick
        if phase == "LANDING_BURN":
            L *= 0.70
        if phase == "IGNITION":
            L *= 0.55

        glBegin(GL_TRIANGLES)
        glColor4f(1.0, 0.86, 0.25, 0.85)
        glVertex3f(-0.32, 0, -0.18)
        glVertex3f(0.32, 0, -0.18)
        glColor4f(1.0, 0.18, 0.02, 0.05)
        glVertex3f(0, 0, -L)
        glEnd()

        glBegin(GL_TRIANGLES)
        glColor4f(0.40, 0.70, 1.0, 0.65)
        glVertex3f(-0.14, 0, -0.16)
        glVertex3f(0.14, 0, -0.16)
        glColor4f(0.92, 0.98, 1.0, 0.05)
        glVertex3f(0, 0, -L * 0.55)
        glEnd()

        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

    glPopMatrix()


# ---------- PARTICLES ----------
def _add_particle(x, y, z, vx, vy, vz, size, life, kind, r, g, b, a, growth):
    particles.append({
        "x": x, "y": y, "z": z,
        "vx": vx, "vy": vy, "vz": vz,
        "size": size,
        "life": life,
        "kind": kind,
        "r": r, "g": g, "b": b, "a": a,
        "growth": growth,
        "seed": random.random() * 10.0,
    })


def spawn_engine_particles(altitude, phase, throttle, velocity, t):
    if throttle <= 0.02:
        return

    if phase == "ASCENT":
        smoke_n = int(22 + 26 * throttle)
        flame_n = int(10 + 12 * throttle)
        spread = 1.35
    elif phase == "LANDING_BURN":
        smoke_n = int(10 + 10 * throttle)
        flame_n = int(6 + 8 * throttle)
        spread = 0.80
    else:
        smoke_n = int(18 + 22 * throttle)
        flame_n = int(9 + 10 * throttle)
        spread = 1.10

    base_y = max(0.0, altitude + 0.10)

    for _ in range(smoke_n):
        x = random.uniform(-spread, spread)
        z = random.uniform(-spread, spread)
        down = -random.uniform(1.0, 3.8) * (1.15 if phase in ("IGNITION", "ASCENT") else 0.8)
        up = random.uniform(0.6, 1.4)

        vx = random.uniform(-2.8, 2.8)
        vz = random.uniform(-2.8, 2.8)
        vy = down + up

        size = random.uniform(0.22, 0.55) * (1.15 if phase == "ASCENT" else 1.0)
        life = random.uniform(0.9, 1.25)
        shade = random.uniform(0.32, 0.48)
        _add_particle(x, base_y, z, vx, vy, vz, size, life, "smoke", shade, shade, shade, 0.95, 1.9)

    for _ in range(flame_n):
        x = random.uniform(-0.35, 0.35)
        z = random.uniform(-0.35, 0.35)

        vx = random.uniform(-1.2, 1.2)
        vz = random.uniform(-1.2, 1.2)
        vy = -random.uniform(8.0, 15.0) * (0.8 + 0.6 * throttle)

        size = random.uniform(0.06, 0.15) * (1.0 + 0.6 * throttle)
        life = random.uniform(0.12, 0.22)

        if random.random() < 0.35:
            r, g, b = (0.55, 0.75, 1.0)
        else:
            r, g, b = (1.0, 0.55, 0.10)
        _add_particle(x, base_y, z, vx, vy, vz, size, life, "flame", r, g, b, 0.90, 0.35)


def spawn_ignition_puffs(altitude, t):
    if altitude > 2.0:
        return
    for _ in range(10):
        x = random.uniform(-2.4, 2.4)
        z = random.uniform(-2.4, 2.4)
        y = random.uniform(0.02, 0.30)
        vx = random.uniform(-1.8, 1.8)
        vz = random.uniform(-1.8, 1.8)
        vy = random.uniform(0.8, 2.2)
        size = random.uniform(0.30, 0.65)
        life = random.uniform(0.65, 1.0)
        shade = random.uniform(0.38, 0.55)
        _add_particle(x, y, z, vx, vy, vz, size, life, "smoke", shade, shade, shade, 0.80, 2.2)


def spawn_cooling_particles(altitude, phase, t):
    if phase == "CHILLDOWN":
        n = 14
        side = 0.68
        base_y = 1.3
    elif phase == "COOLDOWN":
        n = 10
        side = 0.85
        base_y = 0.7
    else:
        n = 6
        side = 0.9
        base_y = 0.9

    for _ in range(n):
        x = random.uniform(-side, side)
        z = random.uniform(-side, side)
        y = random.uniform(base_y, base_y + 1.25)

        vx = random.uniform(-0.8, 0.8)
        vz = random.uniform(-0.8, 0.8)
        vy = random.uniform(1.2, 2.4)

        size = random.uniform(0.14, 0.34)
        life = random.uniform(0.75, 1.15)
        _add_particle(
            x, y + max(0.0, altitude), z,
            vx, vy, vz,
            size, life, "steam",
            0.86, 0.92, 1.0, 0.75, 1.05
        )

    for _ in range(max(0, n - 6)):
        x = random.uniform(-2.2, 2.2)
        z = random.uniform(-2.2, 2.2)
        y = random.uniform(0.05, 0.22)
        vx = random.uniform(-1.0, 1.0)
        vz = random.uniform(-1.0, 1.0)
        vy = random.uniform(1.0, 2.2)
        size = random.uniform(0.18, 0.42)
        life = random.uniform(0.65, 1.0)
        _add_particle(
            x, y, z,
            vx, vy, vz,
            size, life, "steam",
            0.88, 0.94, 1.0, 0.55, 1.0
        )


def draw_particles(dt):
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_LIGHTING)

    particles.sort(key=lambda p: p["size"], reverse=True)

    for p in particles[:]:
        turb = (math.sin(p["seed"] + p["x"] * 0.7 + p["z"] * 0.7) * 0.6)

        if p["kind"] == "smoke":
            p["vy"] += (2.4 + turb) * dt
            p["vx"] += random.uniform(-1.2, 1.2) * dt
            p["vz"] += random.uniform(-1.2, 1.2) * dt
            p["size"] += p["growth"] * dt
            decay = 0.46
        elif p["kind"] == "steam":
            p["vy"] += (1.4 + 0.6 * turb) * dt
            p["vx"] += random.uniform(-0.7, 0.7) * dt
            p["vz"] += random.uniform(-0.7, 0.7) * dt
            p["size"] += p["growth"] * dt
            decay = 0.62
        else:
            p["vy"] -= 6.0 * dt
            p["size"] += p["growth"] * dt
            decay = 4.4

        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt
        p["z"] += p["vz"] * dt

        p["life"] -= decay * dt
        if p["life"] <= 0:
            particles.remove(p)
            continue

        if p["kind"] in ("smoke", "steam") and p["y"] < 0.02:
            p["y"] = 0.02
            p["vy"] = abs(p["vy"]) * 0.2

        alpha = clamp01(p["life"]) * p["a"]
        if p["kind"] == "flame":
            alpha *= clamp01(p["life"] * 1.8)

        glColor4f(p["r"], p["g"], p["b"], alpha)

        glPushMatrix()
        glTranslatef(p["x"], p["y"], p["z"])
        q = gluNewQuadric()
        gluSphere(q, p["size"], 12, 8)
        glPopMatrix()

    glEnable(GL_LIGHTING)
    glDisable(GL_BLEND)


# ---------- HUD ----------
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

    panel(18, 18, 292, 106, (0.02, 0.03, 0.04))
    bar(38, 46, 230, 12, rocket.fuel / rocket.max_fuel, (1.0, 0.45, 0.05))
    bar(38, 72, 230, 12, min(1, rocket.altitude / 160), (0.20, 0.65, 1.0))
    bar(38, 98, 230, 12, rocket.throttle, (0.65, 0.92, 0.25))

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