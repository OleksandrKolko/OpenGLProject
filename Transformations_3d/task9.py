import sys
import numpy as np

sys.path.append('src')

from src.engine.scene.Scene import Scene
from src.engine.model.SimplePolygon import SimplePolygon
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3

# ========= Вершини прямокутника =========
rect_vertices = [
    Vec3(1, 2, 0),
    Vec3(4, 2, 0),
    Vec3(4, 5, 0),
    Vec3(1, 5, 0)
]

# Перетворюємо у плоский список для SimplePolygon
vertices_flat = []
for v in rect_vertices:
    vertices_flat.extend([v.x, v.y, v.z])

# ========= Параметри трансформацій =========
pivot = Vec3(3, 3, 0)        # опорна точка
angle_y = 60                 # поворот навколо Y
angle_x = 30                 # поворот навколо X

# ========= Матриці =========
# Переміщення до pivot і назад
T_to_pivot = Mat4x4.translation(-pivot.x, -pivot.y, -pivot.z)
T_back = Mat4x4.translation(pivot.x, pivot.y, pivot.z)

# Повороти
R_y = Mat4x4.rotation_y(angle_y, is_radians=False)
R_x = Mat4x4.rotation_x(angle_x, is_radians=False)

# Повороти навколо pivot
R_y_pivot = T_back * R_y * T_to_pivot
R_x_pivot = T_back * R_x * T_to_pivot

# Загальна матриця (спочатку поворот навколо Y, потім навколо X)
M = R_x_pivot * R_y_pivot

# Або спрощено (без проміжного повернення):
# M = T_back * R_x * R_y * T_to_pivot

# ========= Обчислення координат для звіту =========
print("=" * 60)
print("Завдання 9: Зміна перспективи з використанням опорної точки")
print("=" * 60)

print("\nПочаткові вершини прямокутника:")
for i, v in enumerate(rect_vertices):
    print(f"  P{i+1}: ({v.x}, {v.y}, {v.z})")

# Після повороту навколо Y
rotated_y = [R_y_pivot * v for v in rect_vertices]
print("\nВершини після повороту на 60° навколо Y відносно pivot (3,3,0):")
for i, v in enumerate(rotated_y):
    print(f"  P{i+1}': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

# Після повороту навколо X
transformed_vertices = [M * v for v in rect_vertices]
print("\nВершини після повороту на 30° навколо X (кінцеве положення):")
for i, v in enumerate(transformed_vertices):
    print(f"  P{i+1}'': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")
print("=" * 60)

# ========= Візуалізація =========
# Початковий прямокутник (сірий)
initial_rect = SimplePolygon(
    *vertices_flat,
    color="gray",
    edgecolor="black",
    alpha=0.3,
    line_width=2
)

# Трансформований прямокутник (червоний)
transformed_flat = []
for v in transformed_vertices:
    transformed_flat.extend([v.x, v.y, v.z])

transformed_rect = SimplePolygon(
    *transformed_flat,
    color="red",
    edgecolor="darkred",
    alpha=0.5,
    line_width=2
)

# Створюємо сцену
scene = Scene(
    coordinate_rect=(-2, -2, -4, 6, 6, 4),
    title="3D Task 9: Rotation Y(60°) then X(30°) around pivot (3,3,0)",
    axis_show=True,
    grid_show=True
)

scene["initial_rect"] = initial_rect
scene["transformed_rect"] = transformed_rect

scene.show()