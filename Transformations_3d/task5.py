import sys
import numpy as np
import random

sys.path.append('src')

from src.engine.scene.Scene import Scene
from src.math.Vec3 import Vec3
from src.math.Mat4x4 import Mat4x4


def draw_tetrahedron(plt_axis, vertices, color="gray", alpha=0.5):
    """Малює тетраедр через його грані."""
    # Грані тетраедра (кожна грань — це 3 вершини)
    faces = [
        [0, 1, 2],  # основа (0,0,0), (1,0,0), (0,1,0)
        [0, 1, 3],  # (0,0,0), (1,0,0), (0,0,1)
        [0, 2, 3],  # (0,0,0), (0,1,0), (0,0,1)
        [1, 2, 3]  # (1,0,0), (0,1,0), (0,0,1)
    ]

    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    for face in faces:
        face_vertices = [vertices[i] for i in face]
        face_points = [[v.x, v.y, v.z] for v in face_vertices]
        polygon = Poly3DCollection([face_points], alpha=alpha, edgecolor=color, facecolor=color)
        plt_axis.add_collection3d(polygon)


# Вершини тетраедра
vertices = [
    Vec3(0, 0, 0),
    Vec3(1, 0, 0),
    Vec3(0, 1, 0),
    Vec3(0, 0, 1)
]

# ========= Генерація випадкових параметрів =========
# 1. Випадкова вісь обертання
axes = {
    "X": Vec3(1, 0, 0),
    "Y": Vec3(0, 1, 0),
    "Z": Vec3(0, 0, 1)
}
axis_name = random.choice(["X", "Y", "Z"])
axis = axes[axis_name]

# 2. Випадковий кут (від 10° до 90°)
angle_deg = random.uniform(10, 90)

# 3. Випадкове переміщення (від -5 до 5)
tx = random.uniform(-5, 5)
ty = random.uniform(-5, 5)
tz = random.uniform(-5, 5)

# Виводимо параметри для звіту
print("=" * 50)
print("Завдання 5: Рандомізоване обертання і зсув")
print(f"Вісь обертання: {axis_name}")
print(f"Кут обертання: {angle_deg:.2f}°")
print(f"Переміщення: ({tx:.2f}, {ty:.2f}, {tz:.2f})")
print("=" * 50)

# ========= Побудова матриць =========
# 1. Матриця обертання
R = Mat4x4.rotation(angle_deg, axis, is_radians=False)

# 2. Матриця переміщення
T = Mat4x4.translation(tx, ty, tz)

# Загальна матриця (спочатку обертання, потім переміщення)
M = T * R

# Застосовуємо трансформацію до вершин
transformed_vertices = [M * v for v in vertices]


# ========= Візуалізація =========
def initial_frame(scene: Scene):
    draw_tetrahedron(scene.plt_axis, vertices, color="gray", alpha=0.3)


def transformed_frame(scene: Scene):
    draw_tetrahedron(scene.plt_axis, transformed_vertices, color="red", alpha=0.5)


# Обчислюємо межі для coordinate_rect
all_x = [v.x for v in vertices] + [v.x for v in transformed_vertices]
all_y = [v.y for v in vertices] + [v.y for v in transformed_vertices]
all_z = [v.z for v in vertices] + [v.z for v in transformed_vertices]

x_min, x_max = min(all_x), max(all_x)
y_min, y_max = min(all_y), max(all_y)
z_min, z_max = min(all_z), max(all_z)

# Додаємо відступ у 1 одиницю
padding = 1
coordinate_rect = (x_min - padding, y_min - padding, z_min - padding,
                   x_max + padding, y_max + padding, z_max + padding)

# Створюємо сцену
scene = Scene(
    coordinate_rect=coordinate_rect,
    title=f"3D Task 5: Random Rotation around {axis_name} axis ({angle_deg:.1f}°) → Random Translation ({tx:.1f}, {ty:.1f}, {tz:.1f})",
    axis_show=True,
    grid_show=True
)

scene.add_frames(initial_frame, transformed_frame)
scene.show()