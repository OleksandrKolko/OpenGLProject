import numpy as np
from src.math.Quaternion import Quaternion
from src.math.Vec4 import Vec4

# 1. Точка p = (1, 0, 0) як чистий кватерніон
p = Vec4(1, 0, 0)
v = Quaternion(p)  # v = (w=0, x=1, y=0, z=0)
print(f"v = {v}")

# Кватерніон повороту навколо Z на 90°
theta = np.radians(90)
axis = (0, 0, 1)
q = Quaternion.rotation(theta, axis)
q_inv = q.inverse()
print(f"q = {q}")
print(f"q⁻¹ = {q_inv}")

# 2. Поворот: v' = q * v * q⁻¹
v_rotated = q * v * q_inv
print(f"v' = {v_rotated}")

# 3. Векторна частина
p_rotated = (v_rotated.x, v_rotated.y, v_rotated.z)
print(f"Координати після повороту: {p_rotated}")

# Перевірка: (1,0,0) повернутий на 90° навколо Z дає (0,1,0)
expected = (0, 1, 0)
print(f"Очікуваний результат: {expected}")
print(f"Збігається: {p_rotated[0] == expected[0] and p_rotated[1] == expected[1] and p_rotated[2] == expected[2]}")