import numpy as np
from src.engine.model.Cube import Cube
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4

# 1. ТЕОРЕТИЧНА ЧАСТИНА: Розрахунок матриць та позицій вершин

# --- Етап 1: Розтяг ---
print("\n1. Матриця розтягу (Scale): Sx=2, Sy=0.5, Sz=1")
S = Mat4x4.scale(2, 0.5, 1)
print(S)

# --- Етап 2: Обертання ---
print("\n2. Матриця обертання (Euler XYZ): X=30°, Y=45°, Z=60°")
angle_x, angle_y, angle_z = np.radians(30), np.radians(45), np.radians(60)
R = Mat4x4.rotation_euler(angle_x, angle_y, angle_z, Mat4x4.XYZ)
print(R)

# --- Етап 3: Переміщення ---
print("\n3. Матриця переміщення (Translation): (-3, 2, 5)")
T = Mat4x4.translation(-3, 2, 5)
print(T)

# --- Фінальна матриця трансформації ---
M_final = T * R * S
print("\n4. Фінальна матриця трансформації (M = T * R * S):")
print(M_final)

# Розрахунок нових позицій діагональних вершин (0,0,0) та (1,1,1)
v1_initial = np.array([0, 0, 0, 1])
v2_initial = np.array([1, 1, 1, 1])

v1_final = M_final.data @ v1_initial
v2_final = M_final.data @ v2_initial

print("\n5. Положення ключових вершин після трансформації:")
print(f"   Початкове: (0,0,0) -> Кінцеве: ({v1_final[0]:.2f}, {v1_final[1]:.2f}, {v1_final[2]:.2f})")
print(f"   Початкове: (1,1,1) -> Кінцеве: ({v2_final[0]:.2f}, {v2_final[1]:.2f}, {v2_final[2]:.2f})")

# 2. ВІЗУАЛЬНА ЧАСТИНА: Побудова сцени
CUBE_INITIAL = "cube_initial"
CUBE_FINAL = "cube_final"


class Task1Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Початковий куб (сірий, напівпрозорий)
        cube_initial = Cube(alpha=0.2, edge_color="grey", color="grey")
        self[CUBE_INITIAL] = cube_initial

        # Фінальний куб, до якого застосовано всі трансформації
        cube_final = Cube(alpha=0.5, color="cyan", edge_color="blue")
        cube_final.transformation = M_final
        self[CUBE_FINAL] = cube_final


# Створення та показ сцени
scene = Task1Scene(
    title="Завдання 1: Розтяг, обертання, переміщення",
    coordinate_rect=(-4, -2, -2, 4, 5, 7),  # Розширені межі для кращого огляду
    axis_show_from_origin=True,
)
scene.show()