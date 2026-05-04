import sys
import numpy as np

sys.path.append('src')

from src.engine.scene.Scene import Scene
from src.engine.model.Cube import Cube
from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3


# ========= Функція декомпозиції афінної матриці =========
def decompose_affine_matrix(M):
    """Розкладає афінну матрицю 4x4 на компоненти: переміщення, масштаб, обертання (кут і вісь)"""

    if isinstance(M, Mat4x4):
        data = M.data
    else:
        data = np.array(M)

    # 1. Переміщення (останній стовпець)
    translation = Vec3(data[0, 3], data[1, 3], data[2, 3])

    # 2. Верхня ліва підматриця 3x3
    A = data[:3, :3].copy()

    # 3. Масштаб (довжини стовпців)
    sx = np.linalg.norm(A[:, 0])
    sy = np.linalg.norm(A[:, 1])
    sz = np.linalg.norm(A[:, 2])
    scale = Vec3(sx, sy, sz)

    # 4. Матриця обертання (нормалізована)
    R = A.copy()
    R[:, 0] /= sx
    R[:, 1] /= sy
    R[:, 2] /= sz

    # 5. Кут повороту
    trace = np.trace(R)
    cos_angle = np.clip((trace - 1) / 2, -1, 1)
    angle_rad = np.arccos(cos_angle)
    angle_deg = np.degrees(angle_rad)

    # 6. Вісь обертання
    if np.sin(angle_rad) < 1e-6:
        if abs(angle_rad) < 1e-6:
            axis = Vec3(1, 0, 0)
        else:
            diag = np.diag(R)
            axis_vec = np.sqrt(np.maximum((diag + 1) / 2, 0))
            if R[0, 1] < 0: axis_vec[1] = -axis_vec[1]
            if R[0, 2] < 0: axis_vec[2] = -axis_vec[2]
            if R[1, 2] < 0 and axis_vec[1] * axis_vec[2] > 0: axis_vec[2] = -axis_vec[2]
            axis = Vec3(axis_vec[0], axis_vec[1], axis_vec[2]).normalized()
    else:
        axis_x = R[2, 1] - R[1, 2]
        axis_y = R[0, 2] - R[2, 0]
        axis_z = R[1, 0] - R[0, 1]
        axis = Vec3(axis_x, axis_y, axis_z) / (2 * np.sin(angle_rad))
        axis = axis.normalized()

    # Перевірка ортогональності
    ortho_check = R @ R.T
    is_orthogonal = np.allclose(ortho_check, np.eye(3), atol=1e-6)

    return {
        'translation': translation,
        'scale': scale,
        'angle_deg': angle_deg,
        'angle_rad': angle_rad,
        'axis': axis,
        'is_orthogonal': is_orthogonal,
        'rotation_matrix': Mat4x4(R)
    }


# ========= Параметри трансформацій =========
pivot = Vec3(1, 1, 1)  # опорна точка
scale_factor = 2  # масштабування у 2 рази
angle_deg = 90  # внутрішнє обертання на 90°
axis_local = Vec3(0, 1, 0)  # локальна вісь Y (можна змінити)
translation_ext = Vec3(-3, 4, 2)  # зовнішнє переміщення

# ========= Матриці =========
T_to_origin = Mat4x4.translation(-pivot.x, -pivot.y, -pivot.z)
T_back = Mat4x4.translation(pivot.x, pivot.y, pivot.z)

S = Mat4x4.scale(scale_factor, scale_factor, scale_factor)
S_pivot = T_back * S * T_to_origin

R_local = Mat4x4.rotation(angle_deg, axis_local, is_radians=False)

T_ext = Mat4x4.translation(translation_ext.x, translation_ext.y, translation_ext.z)

# Повний ланцюг (масштаб відносно pivot → внутрішнє обертання → зовнішнє переміщення)
M_final = T_ext * S_pivot * R_local

# ========= Вершини куба =========
cube_vertices = [
    Vec3(0, 0, 0), Vec3(1, 0, 0), Vec3(1, 1, 0), Vec3(0, 1, 0),
    Vec3(0, 0, 1), Vec3(1, 0, 1), Vec3(1, 1, 1), Vec3(0, 1, 1)
]

# Застосовуємо трансформацію
transformed_vertices = [M_final * v for v in cube_vertices]

# ========= Вивід результатів =========
print("=" * 70)
print("Завдання 15: Складна композиція з опорною точкою та декомпозиція")
print("=" * 70)

print("\nПочаткові вершини куба:")
for i, v in enumerate(cube_vertices):
    print(f"  V{i + 1}: ({v.x}, {v.y}, {v.z})")

print("\nФінальні вершини куба після всіх трансформацій:")
for i, v in enumerate(transformed_vertices):
    print(f"  V{i + 1}': ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

print("\n" + "=" * 70)
print("Фінальна матриця трансформації M_final:")
print(M_final)

# ========= Декомпозиція фінальної матриці =========
print("\n" + "=" * 70)
print("Декомпозиція фінальної матриці:")
print("=" * 70)

decomposed = decompose_affine_matrix(M_final)

print(
    f"\n1. Вектор переміщення: ({decomposed['translation'].x:.3f}, {decomposed['translation'].y:.3f}, {decomposed['translation'].z:.3f})")
print(f"\n2. Вектор масштабу: ({decomposed['scale'].x:.3f}, {decomposed['scale'].y:.3f}, {decomposed['scale'].z:.3f})")
print(f"\n3. Матриця обертання ортогональна? {decomposed['is_orthogonal']}")
print(f"\n4. Кут повороту: {decomposed['angle_deg']:.3f}° ({decomposed['angle_rad']:.4f} рад)")
print(f"\n5. Вісь обертання: ({decomposed['axis'].x:.3f}, {decomposed['axis'].y:.3f}, {decomposed['axis'].z:.3f})")

# ========= Візуалізація =========
initial_cube = Cube(color="gray", alpha=0.3)
transformed_cube = Cube(color="red", alpha=0.5)
transformed_cube.transformation = M_final

scene = Scene(
    coordinate_rect=(-5, -2, -2, 4, 6, 5),
    title="3D Task 15: Scale around (1,1,1) ×2 → Internal Rotation Y 90° → Translation (-3,4,2)",
    axis_show=True,
    grid_show=True
)

scene["initial_cube"] = initial_cube
scene["transformed_cube"] = transformed_cube

scene.show()