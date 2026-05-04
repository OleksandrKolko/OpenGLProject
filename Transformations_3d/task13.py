import sys
import numpy as np

sys.path.append('src')

from src.engine.scene.Scene import Scene
from src.engine.model.SimplePolygon import SimplePolygon
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3

# ========= Вершини тетраедра =========
tetra_vertices = [
    Vec3(0, 0, 0),
    Vec3(1, 0, 0),
    Vec3(0, 1, 0),
    Vec3(0, 0, 1)
]

# Перетворюємо у плоский список для SimplePolygon (грані)
# Тетраедр має 4 грані (трикутники)
faces_vertices = [
    [tetra_vertices[0], tetra_vertices[1], tetra_vertices[2]],  # грань ABC
    [tetra_vertices[0], tetra_vertices[1], tetra_vertices[3]],  # грань ABD
    [tetra_vertices[0], tetra_vertices[2], tetra_vertices[3]],  # грань ACD
    [tetra_vertices[1], tetra_vertices[2], tetra_vertices[3]]   # грань BCD
]

# ========= Параметри трансформацій =========
angle1_deg = 45      # перше обертання навколо осі Y
translation_dist = 2  # переміщення вздовж локальної осі Z
angle2_deg = 30      # друге обертання навколо осі X

# ========= Матриці трансформацій (в локальній системі) =========
# Перше обертання навколо Y
R1_local = Mat4x4.rotation_y(angle1_deg, is_radians=False)

# Переміщення вздовж осі Z
T_local = Mat4x4.translation(0, 0, translation_dist)

# Друге обертання навколо X
R2_local = Mat4x4.rotation_x(angle2_deg, is_radians=False)

# Загальна матриця (внутрішні трансформації — множимо справа)
M = R1_local * T_local * R2_local

# ========= Обчислення координат після кожного кроку =========
print("=" * 70)
print("Завдання 13: Внутрішні обертання та локальна система координат")
print("=" * 70)

print("\nПочаткові вершини тетраедра:")
for i, v in enumerate(tetra_vertices):
    print(f"  V{i+1}: ({v.x}, {v.y}, {v.z})")

# Крок 1: після першого обертання
after_R1 = [R1_local * v for v in tetra_vertices]
print("\nПісля кроку 1 (обертання на 45° навколо осі Y):")
for i, v in enumerate(after_R1):
    print(f"  V{i+1}': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

# Крок 2: після переміщення
after_T = [T_local * v for v in after_R1]
print("\nПісля кроку 2 (переміщення на 2 вздовж локальної осі Z):")
for i, v in enumerate(after_T):
    print(f"  V{i+1}'': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

# Крок 3: після другого обертання
after_R2 = [M * v for v in tetra_vertices]
print("\nПісля кроку 3 (обертання на 30° навколо локальної осі X):")
for i, v in enumerate(after_R2):
    print(f"  V{i+1}''': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")
print("=" * 70)

# ========= Візуалізація =========
def create_triangle(v1, v2, v3, color, alpha):
    """Створює трикутник з трьох вершин"""
    flat = [v1.x, v1.y, v1.z, v2.x, v2.y, v2.z, v3.x, v3.y, v3.z]
    return SimplePolygon(*flat, color=color, edgecolor=color, alpha=alpha, line_width=2)

# Початковий тетраедр (сірий)
initial_faces = []
for face in faces_vertices:
    initial_faces.append(create_triangle(face[0], face[1], face[2], "gray", 0.2))

# Трансформований тетраедр (червоний)
transformed_vertices = after_R2
transformed_faces = [
    [transformed_vertices[0], transformed_vertices[1], transformed_vertices[2]],
    [transformed_vertices[0], transformed_vertices[1], transformed_vertices[3]],
    [transformed_vertices[0], transformed_vertices[2], transformed_vertices[3]],
    [transformed_vertices[1], transformed_vertices[2], transformed_vertices[3]]
]

transformed_objects = []
for face in transformed_faces:
    transformed_objects.append(create_triangle(face[0], face[1], face[2], "red", 0.5))

# Створюємо сцену
scene = Scene(
    coordinate_rect=(-3, -3, -3, 4, 4, 4),
    title="3D Task 13: Internal Rotations and Local Coordinate System",
    axis_show=True,
    grid_show=True
)

# Додаємо початковий тетраедр
for i, face in enumerate(initial_faces):
    scene[f"initial_face_{i}"] = face

# Додаємо трансформований тетраедр
for i, face in enumerate(transformed_objects):
    scene[f"transformed_face_{i}"] = face

scene.show()