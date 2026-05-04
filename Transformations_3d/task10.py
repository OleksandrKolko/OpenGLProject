import sys
import numpy as np

sys.path.append('src')

from src.engine.scene.Scene import Scene
from src.engine.model.Cube import Cube
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3

# ========= Параметри трансформацій =========
pivot = Vec3(1, 1, 1)                    # опорна точка
sx, sy, sz = 2, 1, 1                    # розтяг по X у 2 рази
angle_y = 45                            # поворот навколо Y
translation = Vec3(-3, 4, 2)            # переміщення

# ========= Матриці =========
T_to_origin = Mat4x4.translation(-pivot.x, -pivot.y, -pivot.z)
T_back = Mat4x4.translation(pivot.x, pivot.y, pivot.z)

S = Mat4x4.scale(sx, sy, sz)            # розтяг відносно початку
R_y = Mat4x4.rotation_y(angle_y, is_radians=False)  # поворот навколо Y
T_trans = Mat4x4.translation(translation.x, translation.y, translation.z)

# Загальна матриця (розтяг → поворот навколо pivot → переміщення)
M = T_trans * T_back * R_y * S * T_to_origin

# ========= Обчислення координат для звіту =========
print("=" * 60)
print("Завдання 10: Комплексна трансформація")
print("=" * 60)

# Вершини куба
cube_vertices = [
    Vec3(0,0,0), Vec3(1,0,0), Vec3(1,1,0), Vec3(0,1,0),
    Vec3(0,0,1), Vec3(1,0,1), Vec3(1,1,1), Vec3(0,1,1)
]

print("\nПочаткові вершини куба:")
for i, v in enumerate(cube_vertices):
    print(f"  V{i+1}: ({v.x}, {v.y}, {v.z})")

# Після розтягу відносно pivot
S_pivot = T_back * S * T_to_origin
after_scale = [S_pivot * v for v in cube_vertices]
print("\nВершини після розтягу по X у 2 рази відносно pivot (1,1,1):")
for i, v in enumerate(after_scale):
    print(f"  V{i+1}': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

# Після повороту (але до переміщення)
R_pivot = T_back * R_y * T_to_origin
after_rotation = [R_pivot * v for v in after_scale]
print("\nВершини після повороту на 45° навколо Y відносно pivot:")
for i, v in enumerate(after_rotation):
    print(f"  V{i+1}'': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

# Фінальне положення
transformed_vertices = [M * v for v in cube_vertices]
print("\nВершини після переміщення на (-3, 4, 2) (кінцеве положення):")
for i, v in enumerate(transformed_vertices):
    print(f"  V{i+1}''': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")
print("=" * 60)

# ========= Візуалізація =========
# Початковий куб (сірий)
initial_cube = Cube(color="gray", alpha=0.3)

# Трансформований куб (червоний)
transformed_cube = Cube(color="red", alpha=0.5)
transformed_cube.transformation = M

# Створюємо сцену
scene = Scene(
    coordinate_rect=(-5, -2, -2, 4, 6, 4),
    title="3D Task 10: Scale X2 around (1,1,1) → Rotation Y 45° around (1,1,1) → Translation (-3,4,2)",
    axis_show=True,
    grid_show=True
)

scene["initial_cube"] = initial_cube
scene["transformed_cube"] = transformed_cube

scene.show()