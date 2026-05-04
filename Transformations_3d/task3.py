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
# 1. Обертання навколо осі Z (0,0,1) на 60°
R1 = Mat4x4.rotation_z(60, is_radians=False)

# 2. Обертання навколо осі (1,1,1) на 45°
axis = Vec3(1, 1, 1)
R2 = Mat4x4.rotation(45, axis, is_radians=False)

# 3. Переміщення на вектор (4, -2, 1)
T = Mat4x4.translation(4, -2, 1)

# Загальна матриця (спочатку R1, потім R2, потім T)
M = T * R2 * R1

# Застосовуємо трансформацію до вершин
transformed_vertices = [M * v for v in vertices]


# ========= Візуалізація =========
def initial_frame(scene: Scene):
    draw_cube(scene.plt_axis, vertices, color="gray", alpha=0.3)


def transformed_frame(scene: Scene):
    draw_cube(scene.plt_axis, transformed_vertices, color="red", alpha=0.5)


# Створюємо сцену
scene = Scene(
    coordinate_rect=(-2, -3, -2, 6, 4, 5),
    title="3D Task 3: Rotation Z(60°) → Rotation around (1,1,1)(45°) → Translation (4,-2,1)",
    axis_show=True,
    grid_show=True
)

scene.add_frames(initial_frame, transformed_frame)
scene.show()