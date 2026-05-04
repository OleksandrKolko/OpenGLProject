import sys
import numpy as np

sys.path.append('src')

from src.engine.scene.Scene import Scene
from src.math.Vec3 import Vec3
from src.math.Mat4x4 import Mat4x4


def draw_cube(plt_axis, vertices, color="gray", alpha=0.5):
    """Малює куб через його грані."""
    faces = [
        [0, 1, 2, 3],  # нижня
        [4, 5, 6, 7],  # верхня
        [0, 1, 5, 4],  # передня
        [2, 3, 7, 6],  # задня
        [1, 2, 6, 5],  # права
        [0, 3, 7, 4]  # ліва
    ]

    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    for face in faces:
        face_vertices = [vertices[i] for i in face]
        face_points = [[v.x, v.y, v.z] for v in face_vertices]
        polygon = Poly3DCollection([face_points], alpha=alpha, edgecolor=color, facecolor=color)
        plt_axis.add_collection3d(polygon)


# Вершини куба (0,0,0) - (1,1,1)
vertices = [
    Vec3(0, 0, 0), Vec3(1, 0, 0), Vec3(1, 1, 0), Vec3(0, 1, 0),
    Vec3(0, 0, 1), Vec3(1, 0, 1), Vec3(1, 1, 1), Vec3(0, 1, 1)
]

# ========= Трансформації =========
# Кути Ейлера (у градусах)
phi = 20  # Z
theta = 35  # Y
psi = 50  # X

# 1. Обертання за кутами Ейлера в порядку ZYX
R = Mat4x4.rotation_euler(
    np.radians(phi),
    np.radians(theta),
    np.radians(psi),
    configuration=Mat4x4.ZYX
)

# 2. Переміщення на вектор (1, 3, -2)
T = Mat4x4.translation(1, 3, -2)

# Загальна матриця (спочатку обертання, потім переміщення)
M = T * R

# Застосовуємо трансформацію до вершин
transformed_vertices = [M * v for v in vertices]


# ========= Візуалізація =========
def initial_frame(scene: Scene):
    draw_cube(scene.plt_axis, vertices, color="gray", alpha=0.3)


def transformed_frame(scene: Scene):
    draw_cube(scene.plt_axis, transformed_vertices, color="red", alpha=0.5)


# Створюємо сцену
scene = Scene(
    coordinate_rect=(-2, -2, -3, 4, 5, 3),
    title="3D Task 4: Euler Rotation ZYX (20°,35°,50°) → Translation (1,3,-2)",
    axis_show=True,
    grid_show=True
)

scene.add_frames(initial_frame, transformed_frame)
scene.show()