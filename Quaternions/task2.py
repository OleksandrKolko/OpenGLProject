import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Vec4 import Vec4

# Вершини тетраедра
vertices = [
    Vec4(0, 0, 0),
    Vec4(1, 0, 0),
    Vec4(0, 1, 0),
    Vec4(0, 0, 1)
]

# 1. Кватерніони поворотів
q1 = Quaternion.rotation(np.radians(45), (1, 0, 0))  # X: 45°
q2 = Quaternion.rotation(np.radians(30), (0, 1, 0))  # Y: 30°

# 2. Результуючий кватерніон (зовнішні осі: спочатку X, потім Y)
q_total = q2 * q1
print(f"q_total = {q_total}")

# 3. Вісь та кут з q_total
angle, axis = q_total.to_angle_axis()
print(f"Кут: {np.degrees(angle):.2f}°")
print(f"Вісь: ({axis.x:.4f}, {axis.y:.4f}, {axis.z:.4f})")

# 4. Поворот вершин через кватерніони
q_total_inv = q_total.inverse()
print("\nНові координати вершин:")
for i, v in enumerate(vertices):
    v_rotated = q_total * Quaternion(v) * q_total_inv
    print(f"Вершина {i}: ({v_rotated.x:.4f}, {v_rotated.y:.4f}, {v_rotated.z:.4f})")