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

# Параметри трансформацій
sx, sy, sz = 2.0, 0.5, 1.0  # розтяг
euler_angles = (30, 45, 60)  # кути Ейлера (градуси)
tx, ty, tz = -3, 2, 5  # переміщення

# Створюємо матриці за допомогою вбудованих методів Mat4x4
S = Mat4x4.scale(sx, sy, sz)  # масштаб
R = Mat4x4.rotation_euler(np.radians(30), np.radians(45), np.radians(60), Mat4x4.XYZ)  # поворот
T = Mat4x4.translation(tx, ty, tz)  # переміщення

# Загальна матриця (спочатку масштаб, потім поворот, потім переміщення)
M = T * R * S

# Застосовуємо трансформацію до вершин
transformed_vertices = [M * v for v in vertices]


# Функції кадрів для сцени
def initial_frame(scene: Scene):
    draw_cube(scene.plt_axis, vertices, color="gray", alpha=0.3)


def transformed_frame(scene: Scene):
    draw_cube(scene.plt_axis, transformed_vertices, color="red", alpha=0.5)


# Створюємо сцену
scene = Scene(
    coordinate_rect=(-5, -3, -2, 4, 4, 6),
    title="3D Task 2: Scale (2,0.5,1) → Euler Rotation (30,45,60) → Translation (-3,2,5)",
    axis_show=True,
    grid_show=True
)

scene.add_frames(initial_frame, transformed_frame)
scene.show()