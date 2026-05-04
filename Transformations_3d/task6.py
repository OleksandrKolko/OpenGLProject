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

# ========= Параметри трансформацій =========
pivot = Vec3(2, 0, 3)  # опорна точка
angle_deg = 45  # кут обертання
translation = Vec3(-1, 2, 4)  # переміщення

# ========= Матриці =========
# Обертання навколо pivot
T_to_origin = Mat4x4.translation(-pivot.x, -pivot.y, -pivot.z)
R_y = Mat4x4.rotation_y(angle_deg, is_radians=False)
T_back = Mat4x4.translation(pivot.x, pivot.y, pivot.z)

R_pivot = T_back * R_y * T_to_origin

# Переміщення
T_trans = Mat4x4.translation(translation.x, translation.y, translation.z)

# Загальна матриця
M = T_trans * R_pivot

# Застосовуємо трансформацію до вершин
transformed_vertices = [M * v for v in vertices]


# ========= Візуалізація =========
def initial_frame(scene: Scene):
    draw_cube(scene.plt_axis, vertices, color="gray", alpha=0.3)
    # Малюємо опорну точку (для наочності)
    from src.base.points import draw_point
    draw_point(scene.plt_axis, [pivot.x, pivot.y, pivot.z], color="purple", size=50)


def transformed_frame(scene: Scene):
    draw_cube(scene.plt_axis, transformed_vertices, color="red", alpha=0.5)


# Створюємо сцену
scene = Scene(
    coordinate_rect=(-2, -2, -2, 6, 5, 7),
    title="3D Task 6: Rotation around pivot (2,0,3) 45° around Y → Translation (-1,2,4)",
    axis_show=True,
    grid_show=True
)

scene.add_frames(initial_frame, transformed_frame)
scene.show()