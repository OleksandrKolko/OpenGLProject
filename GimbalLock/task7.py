import numpy as np
from src.math.Mat4x4 import Mat4x4

print("=" * 60)
print("ЗАВДАННЯ 7: Декомпозиція та неоднозначність")
print("=" * 60)

# Задана матриця: поворот на 90° навколо Y
R = Mat4x4.rotation_y(np.radians(90))
print("\n1. Матриця повороту на 90° навколо Y:")
print(R)

# Алгоритм декомпозиції XYZ
def euler_from_matrix_xyz(R, tol=1e-6):
    r = R.data if isinstance(R, Mat4x4) else R
    if abs(r[0, 2]) > (1.0 - tol):
        # Сингулярність: sin(beta) ≈ ±1, beta = ±90°
        beta = np.pi/2 if r[0, 2] > 0 else -np.pi/2
        alpha = 0.0  # фіксуємо alpha
        gamma = np.arctan2(r[2, 0], r[2, 1]) if beta > 0 else np.arctan2(-r[2, 0], r[2, 1])
        singular = True
    else:
        beta = np.arcsin(r[0, 2])
        alpha = np.arctan2(-r[1, 2], r[2, 2])
        gamma = np.arctan2(-r[0, 1], r[0, 0])
        singular = False
    return np.degrees(alpha), np.degrees(beta), np.degrees(gamma), singular

a, b, g, sing = euler_from_matrix_xyz(R)
print(f"\n2. Декомпозиція: α={a:.1f}°, β={b:.1f}°, γ={g:.1f}°")
print(f"   Сингулярність: {sing}")

# Нескінченна кількість комбінацій
print("\n3. Нескінченна кількість комбінацій (α, γ) з β=90°:")
print("   Будь-яка пара (α, γ) де α-γ = const дає ту саму матрицю.")
print(f"   Для даної матриці α-γ = {a - g:.1f}°")
print()
for test_a in [0, 30, -45, 90]:
    test_g = test_a - (a - g)
    R_test = Mat4x4.rotation_euler(np.radians(test_a), np.radians(90), np.radians(test_g), Mat4x4.XYZ)
    same = np.allclose(R.data, R_test.data)
    print(f"   α={test_a:5.0f}°, γ={test_g:5.0f}° -> та сама матриця: {same}")

# Модифікований алгоритм з примусовим α=0
def euler_from_matrix_xyz_fixed(R, tol=1e-6):
    r = R.data if isinstance(R, Mat4x4) else R
    if abs(r[0, 2]) > (1.0 - tol):
        beta = np.pi/2 if r[0, 2] > 0 else -np.pi/2
        alpha = 0.0
        gamma = np.arctan2(r[2, 0], r[2, 1]) if beta > 0 else np.arctan2(-r[2, 0], r[2, 1])
    else:
        beta = np.arcsin(r[0, 2])
        alpha = np.arctan2(-r[1, 2], r[2, 2])
        gamma = np.arctan2(-r[0, 1], r[0, 0])
    return np.degrees(alpha), np.degrees(beta), np.degrees(gamma)

a_f, b_f, g_f = euler_from_matrix_xyz_fixed(R)
print(f"\n4. Модифікований алгоритм (α=0 при сингулярності):")
print(f"   α={a_f:.1f}°, β={b_f:.1f}°, γ={g_f:.1f}°")

# Перевірка: відновлюємо матрицю
R_rec = Mat4x4.rotation_euler(np.radians(a_f), np.radians(b_f), np.radians(g_f), Mat4x4.XYZ)
print(f"   Відновлена матриця збігається: {np.allclose(R.data, R_rec.data)}")