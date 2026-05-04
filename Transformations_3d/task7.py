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
pivot = Vec3(1, 2, 3)  # опорна точка
scale_z = 3  # розтяг по осі Z у 3 рази
angle_deg = 30  # кут обертання навколо Z

# ========= Матриці =========
# Переміщення до початку координат і назад
T_to_origin = Mat4x4.translation(-pivot.x, -pivot.y, -pivot.z)
T_back = Mat4x4.translation(pivot.x, pivot.y, pivot.z)

# Трансформації відносно початку координат
S = Mat4x4.scale(1, 1, scale_z)  # масштабування по Z
R = Mat4x4.rotation_z(angle_deg, is_radians=False)  # обертання навколо Z

# Загальна матриця (спочатку масштабування, потім обертання, pivot враховано)
M = T_back * R * S * T_to_origin

# Застосовуємо трансформацію до вершин
transformed_vertices = [M * v for v in vertices]


# ========= Візуалізація =========
def initial_frame(scene: Scene):
    draw_cube(scene.plt_axis, vertices, color="gray", alpha=0.3)
    # Малюємо опорну точку
    from src.base.points import draw_point
    draw_point(scene.plt_axis, [pivot.x, pivot.y, pivot.z], color="purple", size=50)


def transformed_frame(scene: Scene):
    draw_cube(scene.plt_axis, transformed_vertices, color="red", alpha=0.5)


# Обчислюємо межі для coordinate_rect з запасом
all_points = vertices + transformed_vertices
all_x = [v.x for v in all_points] + [pivot.x]
all_y = [v.y for v in all_points] + [pivot.y]
all_z = [v.z for v in all_points] + [pivot.z]

x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)
z_min, z_max = min(all_z), max(all_z)

padding = 2
coordinate_rect = (x_min - padding, y_min - padding, z_min - padding,
                   x_max + padding, y_max + padding, z_max + padding)

# Створюємо сцену
scene = Scene(
    coordinate_rect=coordinate_rect,
    title="3D Task 7: Scale Z(3x) around pivot (1,2,3) → Rotation Z(30°) around same pivot",
    axis_show=True,
    grid_show=True
)

scene.add_frames(initial_frame, transformed_frame)
scene.show()