import sys
import numpy as np

sys.path.append('src')

from src.engine.scene.Scene import Scene
from src.engine.model.SimplePolygon import SimplePolygon
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3

# ========= Вершини трикутника =========
triangle_vertices = [
    Vec3(1, 2, 3),
    Vec3(4, 5, 6),
    Vec3(7, 8, 9)
]

# Перетворюємо у список списків для SimplePolygon
vertices_flat = []
for v in triangle_vertices:
    vertices_flat.extend([v.x, v.y, v.z])

# ========= Параметри трансформацій =========
pivot = Vec3(2, 3, 4)                     # точка на осі обертання
axis = Vec3(1, 1, 1)                     # напрям осі
angle_deg = 90                           # кут обертання
translation = Vec3(0, -3, 2)             # переміщення

# ========= Матриці =========
# Переміщення до початку координат і назад
T_to_origin = Mat4x4.translation(-pivot.x, -pivot.y, -pivot.z)
T_back = Mat4x4.translation(pivot.x, pivot.y, pivot.z)

# Обертання навколо осі (1,1,1) на 90°
R_axis = Mat4x4.rotation(angle_deg, axis, is_radians=False)

# Обертання навколо осі через pivot
R_pivot = T_back * R_axis * T_to_origin

# Переміщення
T_trans = Mat4x4.translation(translation.x, translation.y, translation.z)

# Загальна матриця (спочатку обертання, потім переміщення)
M = T_trans * R_pivot

# ========= Обчислення координат для звіту =========
print("=" * 60)
print("Завдання 8: Поворот навколо осі, що не проходить через початок координат")
print("=" * 60)

print("\nПочаткові вершини трикутника:")
for i, v in enumerate(triangle_vertices):
    print(f"  P{i+1}: ({v.x}, {v.y}, {v.z})")

# Після обертання
rotated_vertices = [R_pivot * v for v in triangle_vertices]
print("\nВершини після обертання навколо осі (1,1,1) через точку (2,3,4):")
for i, v in enumerate(rotated_vertices):
    print(f"  P{i+1}': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

# Після переміщення
transformed_vertices = [M * v for v in triangle_vertices]
print("\nВершини після переміщення на (0, -3, 2):")
for i, v in enumerate(transformed_vertices):
    print(f"  P{i+1}'': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")
print("=" * 60)

# ========= Візуалізація =========
# Початковий трикутник (сірий)
initial_triangle = SimplePolygon(
    *vertices_flat,
    color="gray",
    edgecolor="black",
    alpha=0.3,
    line_width=2
)

# Трансформований трикутник (червоний)
transformed_flat = []
for v in transformed_vertices:
    transformed_flat.extend([v.x, v.y, v.z])

transformed_triangle = SimplePolygon(
    *transformed_flat,
    color="red",
    edgecolor="darkred",
    alpha=0.5,
    line_width=2
)

# Створюємо сцену
scene = Scene(
    coordinate_rect=(-5, -5, -5, 15, 15, 15),
    title="3D Task 8: Rotation 90° around axis (1,1,1) through (2,3,4) → Translation (0,-3,2)",
    axis_show=True,
    grid_show=True
)

scene["initial_triangle"] = initial_triangle
scene["transformed_triangle"] = transformed_triangle

scene.show()