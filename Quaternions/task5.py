import numpy as np
from src.math.Mat4x4 import Mat4x4
from src.math.utils_quat import rotation_matrix_to_quaternion

# Матриця трансформації
M_data = np.array([
    [0, -2, 0, 10],
    [1, 0, 0, -5],
    [0, 0, 1.5, 3],
    [0, 0, 0, 1]
], dtype=float)

M = Mat4x4(M_data)
print("Матриця M:")
print(M)

# 1. Вилучення трансляції
T = M[:3, 3]
print(f"\n1. Вектор перенесення T = ({T[0]}, {T[1]}, {T[2]})")

# 2. Вилучення масштабування
M3 = M[:3, :3]  # підматриця 3x3
sx = np.linalg.norm(M3[:, 0])  # норма першого стовпця
sy = np.linalg.norm(M3[:, 1])  # норма другого стовпця
sz = np.linalg.norm(M3[:, 2])  # норма третього стовпця

print(f"\n2. Масштабні коефіцієнти:")
print(f"   sx = {sx}")
print(f"   sy = {sy}")
print(f"   sz = {sz}")

# 3. Отримання чистої матриці обертання H
H_data = M3.copy()
H_data[:, 0] /= sx
H_data[:, 1] /= sy
H_data[:, 2] /= sz

H = Mat4x4(H_data)
print(f"\n3. Матриця обертання H:")
print(H)

# Перевірка ортогональності H^T * H = I
HTH = H.T * H
print(f"\nПеревірка H^T * H (повинна бути одиничною):")
print(HTH)

# 4. Конвертація в кватерніон
q = rotation_matrix_to_quaternion(H)
print(f"\n4. Кватерніон q = {q}")
print(f"   |q| = {q.norm()}")

# Додаткова перевірка: відновлення матриці
R_recovered = q.toRotationMatrix()
print(f"\nВідновлена матриця обертання з кватерніона:")
print(R_recovered)