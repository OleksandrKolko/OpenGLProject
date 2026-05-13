import numpy as np
from src.math.Mat4x4 import Mat4x4
from src.math.utils_quat import rotation_matrix_to_quaternion

# Матриця повороту
R_data = np.array([
    [0, -1, 0],
    [1, 0, 0],
    [0, 0, 1]
])

R = Mat4x4(R_data)

# Знаходження кватерніона
q = rotation_matrix_to_quaternion(R)

print(f"Кватерніон q = {q}")
print(f"Перевірка норми: |q| = {q.norm()}")