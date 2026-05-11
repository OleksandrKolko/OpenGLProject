import numpy as np
from src.engine.model.Cube import Cube
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4

# 1. ТЕОРЕТИЧНА ЧАСТИНА: Розрахунок матриць та позицій вершин

# --- Етап 1: Обертання ---
print("\n1. Матриця обертання (Euler ZYX): Z=20°, Y=35°, X=50°")
angle_z, angle_y, angle_x = np.radians(20), np.radians(35), np.radians(50)
R = Mat4x4.rotation_euler(angle_z, angle_y, angle_x, Mat4x4.ZYX)
print(R)

# --- Етап 2: Переміщення ---
print("\n2. Матриця переміщення (Translation): (1, 3, -2)")
T = Mat4x4.translation(1, 3, -2)
print(T)

# --- Фінальна матриця трансформації ---
M_final = T * R
print("\n3. Фінальна матриця трансформації (M = T * R):")
print(M_final)

# Розрахунок нових позицій діагональних вершин (0,0,0) та (1,1,1)
v1_initial = np.array([0, 0, 0, 1])
v2_initial = np.array([1, 1, 1, 1])

v1_final = M_final.data @ v1_initial
v2_final = M_final.data @ v2_initial

print("\n4. Положення ключових вершин після трансформації:")
print(f"   Початкове: (0,0,0) -> Кінцеве: ({v1_final[0]:.2f}, {v1_final[1]:.2f}, {v1_final[2]:.2f})")
print(f"   Початкове: (1,1,1) -> Кінцеве: ({v2_final[0]:.2f}, {v2_final[1]:.2f}, {v2_final[2]:.2f})")

# 2. ВІЗУАЛЬНА ЧАСТИНА: Побудова сцени
CUBE_INITIAL = "cube_initial"
CUBE_FINAL = "cube_final"


class Task2Scene(AnimatedScene):
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
scene = Task2Scene(
    title="Завдання 2: Поворот у системі кутів Ейлера ZYX",
    coordinate_rect=(-2, -2, -3, 4, 5, 3),
    axis_show_from_origin=True,
)
scene.show()