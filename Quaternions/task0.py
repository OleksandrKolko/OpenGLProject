import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3

# 1. Побудова кватерніона
theta = np.radians(60)
u = Vec3(1, 1, 1).normalized()  # u = (1/√3, 1/√3, 1/√3)

q = Quaternion.rotation(theta, u)
print(f"Кватерніон q = {q}")

# 2. Перевірка норми
norm = q.norm()
print(f"|q| = {norm}")

# 3. Матриця повороту
R = q.toRotationMatrix()
print("Матриця повороту R:")
print(R)