import sys
import numpy as np

sys.path.append('src')

from src.math.Mat4x4 import Mat4x4
from src.math.Vec3 import Vec3


def decompose_affine_matrix(M):
    """
    Розкладає афінну матрицю 4x4 на компоненти:
    - translation (Vec3)
    - scale (Vec3)
    - rotation (Mat4x4)
    - angle (радіани, градуси)
    - axis (Vec3)
    """
    # Отримуємо дані у вигляді numpy масиву 4x4
    if isinstance(M, Mat4x4):
        data = M.data
    else:
        data = np.array(M)

    # 1. Вектор переміщення
    translation = Vec3(data[0, 3], data[1, 3], data[2, 3])

    # 2. Верхня ліва підматриця 3x3
    A = data[:3, :3].copy()

    # 3. Масштаб (довжини стовпців)
    sx = np.linalg.norm(A[:, 0])
    sy = np.linalg.norm(A[:, 1])
    sz = np.linalg.norm(A[:, 2])
    scale = Vec3(sx, sy, sz)

    # 4. Матриця обертання (нормалізуємо стовпці)
    R = A.copy()
    R[:, 0] /= sx
    R[:, 1] /= sy
    R[:, 2] /= sz

    # Перевірка на ортогональність
    ortho_check = R @ R.T
    is_orthogonal = np.allclose(ortho_check, np.eye(3), atol=1e-6)

    # 5. Кут повороту та вісь
    trace = np.trace(R)
    cos_angle = (trace - 1) / 2
    cos_angle = np.clip(cos_angle, -1, 1)
    angle_rad = np.arccos(cos_angle)
    angle_deg = np.degrees(angle_rad)

    # 6. Вісь обертання
    if np.sin(angle_rad) < 1e-6:
        # Кут близький до 0 або π
        if abs(angle_rad) < 1e-6:
            axis = Vec3(1, 0, 0)  # довільна вісь
        else:
            # Кут = π (180°), вісь знаходимо з діагоналі
            diag = np.diag(R)
            axis_vec = np.sqrt(np.maximum((diag + 1) / 2, 0))
            # Визначаємо знаки з позадіагональних елементів
            if R[0, 1] < 0: axis_vec[1] = -axis_vec[1]
            if R[0, 2] < 0: axis_vec[2] = -axis_vec[2]
            if R[1, 2] < 0 and axis_vec[1] * axis_vec[2] > 0: axis_vec[2] = -axis_vec[2]
            axis = Vec3(axis_vec[0], axis_vec[1], axis_vec[2]).normalized()
    else:
        # Загальний випадок: з антисиметричної частини
        axis_x = R[2, 1] - R[1, 2]
        axis_y = R[0, 2] - R[2, 0]
        axis_z = R[1, 0] - R[0, 1]
        axis = Vec3(axis_x, axis_y, axis_z) / (2 * np.sin(angle_rad))
        axis = axis.normalized()

    return {
        'translation': translation,
        'scale': scale,
        'rotation_matrix': Mat4x4(R),
        'angle_rad': angle_rad,
        'angle_deg': angle_deg,
        'axis': axis,
        'is_orthogonal': is_orthogonal
    }


# ========= Приклад: тестова матриця =========
# Створюємо матрицю з конкретними параметрами для перевірки
# Розтяг (2, 1.5, 1), поворот на 45° навколо осі (1,1,1), переміщення (2,3,4)

angle_test = np.radians(45)
axis_test = Vec3(1, 1, 1).normalized()
R_test = Mat4x4.rotation(45, Vec3(1, 1, 1), is_radians=False)
S_test = Mat4x4.scale(2, 1.5, 1)
T_test = Mat4x4.translation(2, 3, 4)

M_test = T_test * R_test * S_test

print("=" * 70)
print("Завдання 12: Декомпозиція афінної матриці")
print("=" * 70)

print("\nТестова матриця (створена як T × R × S):")
print(M_test)

# Виконуємо декомпозицію
result = decompose_affine_matrix(M_test)

print("\n" + "=" * 70)
print("Результати декомпозиції:")
print("=" * 70)

print(
    f"\n1. Вектор переміщення: ({result['translation'].x:.3f}, {result['translation'].y:.3f}, {result['translation'].z:.3f})")

print(f"\n2. Вектор масштабу: ({result['scale'].x:.3f}, {result['scale'].y:.3f}, {result['scale'].z:.3f})")

print(f"\n3. Матриця обертання:")
print(result['rotation_matrix'])

print(f"\n4. Матриця обертання ортогональна? {result['is_orthogonal']}")

print(f"\n5. Кут повороту: {result['angle_deg']:.3f}° ({result['angle_rad']:.4f} рад)")

print(f"\n6. Вісь обертання: ({result['axis'].x:.3f}, {result['axis'].y:.3f}, {result['axis'].z:.3f})")

# ========= Перевірка: відновлюємо матрицю =========
R_dec = result['rotation_matrix']
S_dec = Mat4x4.scale(result['scale'].x, result['scale'].y, result['scale'].z)
T_dec = Mat4x4.translation(result['translation'].x, result['translation'].y, result['translation'].z)

M_reconstructed = T_dec * R_dec * S_dec
print("\n" + "=" * 70)
print("Перевірка: відновлена матриця")
print("=" * 70)
print(M_reconstructed)

diff = (M_test - M_reconstructed).norm()
print(f"\nРізниця між оригінальною та відновленою матрицями: {diff:.6f}")
if diff < 1e-6:
    print("✅ Декомпозиція виконана правильно!")
else:
    print("⚠️ Є похибка у декомпозиції")