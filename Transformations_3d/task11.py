import sys
import numpy as np

sys.path.append('src')

from src.engine.scene.Scene import Scene
from src.engine.model.Cube import Cube
from src.math.Mat4x4 import Mat4x4

# ========= Функція для виведення матриці =========
def print_matrix(name, M):
    print(f"\n{name}:")
    print(M)

# ========= Кути (в градусах) =========
# Кути для зовнішнього обертання (30,45,60) порядок XYZ
alpha1, beta1, gamma1 = 30, 45, 60

# Кути для внутрішнього обертання (60,45,30) порядок XYZ
alpha2, beta2, gamma2 = 60, 45, 30

# ========= Трансформація А (зовнішня) =========
# Зовнішнє: R = Rz(gamma) × Ry(beta) × Rx(alpha)
R_A = Mat4x4.rotation_z(gamma1, is_radians=False) * \
      Mat4x4.rotation_y(beta1, is_radians=False) * \
      Mat4x4.rotation_x(alpha1, is_radians=False)

# ========= Трансформація Б (внутрішня) =========
# Внутрішнє (ті ж осі XYZ, але кути в іншому порядку)
# R = Rx(alpha2) × Ry(beta2) × Rz(gamma2) для внутрішнього?
# Ні! Для внутрішнього обертання в тому ж порядку XYZ:
R_B = Mat4x4.rotation_z(gamma2, is_radians=False) * \
      Mat4x4.rotation_y(beta2, is_radians=False) * \
      Mat4x4.rotation_x(alpha2, is_radians=False)

# ========= Порівняння =========
print("=" * 70)
print("Завдання 11: Порівняння зовнішніх та внутрішніх обертань")
print("=" * 70)

print("\nТрансформація А (Зовнішня): обертання навколо СВІТОВИХ осей")
print(f"  Порядок: Rx({alpha1}°) → Ry({beta1}°) → Rz({gamma1}°)")
print_matrix("R_A", R_A)

print("\nТрансформація Б (Внутрішня): обертання навколо ВЛАСНИХ осей")
print(f"  Порядок: Rx({alpha2}°) → Ry({beta2}°) → Rz({gamma2}°)")
print_matrix("R_B", R_B)

# ========= Перевірка чи однакові матриці =========
diff = (R_A - R_B).norm()
print(f"\nРізниця між матрицями (норма): {diff:.6f}")
if diff < 1e-6:
    print("Матриці ІДЕНТИЧНІ! (що не очікувалося для різних кутів)")
else:
    print("Матриці РІЗНІ (що правильно, бо кути різні)")

# ========= Вершини куба =========
cube_vertices_original = [
    (0,0,0), (1,0,0), (1,1,0), (0,1,0),
    (0,0,1), (1,0,1), (1,1,1), (0,1,1)
]

# Перетворюємо у Vec3
from src.math.Vec3 import Vec3
vertices = [Vec3(*v) for v in cube_vertices_original]

# Застосовуємо трансформації
transformed_A = [R_A * v for v in vertices]
transformed_B = [R_B * v for v in vertices]

print("\n" + "=" * 70)
print("Фінальні координати вершин куба")
print("=" * 70)

print("\nТрансформація А (зовнішня):")
for i, v in enumerate(transformed_A):
    print(f"  V{i+1}: ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

print("\nТрансформація Б (внутрішня):")
for i, v in enumerate(transformed_B):
    print(f"  V{i+1}: ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

# ========= Візуалізація =========
# Початковий куб (сірий)
initial_cube = Cube(color="gray", alpha=0.2)

# Куб після трансформації А (червоний)
cube_A = Cube(color="red", alpha=0.5)
cube_A.transformation = R_A

# Куб після трансформації Б (синій)
cube_B = Cube(color="blue", alpha=0.5)
cube_B.transformation = R_B

# Створюємо сцену
scene = Scene(
    coordinate_rect=(-2, -2, -2, 2, 2, 2),
    title="3D Task 11: External vs Internal Rotations",
    axis_show=True,
    grid_show=True
)

scene["initial"] = initial_cube
scene["external"] = cube_A
scene["internal"] = cube_B

scene.show()