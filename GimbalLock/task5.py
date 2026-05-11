import numpy as np
from src.math.Mat4x4 import Mat4x4
from src.math.Vec4 import Vec4

print("=" * 60)
print("ЗАВДАННЯ 5: Втрачена вісь")
print("=" * 60)

# Вершини куба
vertices = [
    Vec4(0, 0, 0, 1), Vec4(1, 0, 0, 1), Vec4(1, 1, 0, 1), Vec4(0, 1, 0, 1),
    Vec4(0, 0, 1, 1), Vec4(1, 0, 1, 1), Vec4(1, 1, 1, 1), Vec4(0, 1, 1, 1),
]
names = ["(0,0,0)", "(1,0,0)", "(1,1,0)", "(0,1,0)", "(0,0,1)", "(1,0,1)", "(1,1,1)", "(0,1,1)"]

# Комбінація 1: X=30°, Y=90°, Z=45°
a1, b1, g1 = np.radians(30), np.radians(90), np.radians(45)
Rx1 = Mat4x4.rotation_x(a1)
Ry1 = Mat4x4.rotation_y(b1)
Rz1 = Mat4x4.rotation_z(g1)
M1 = Rz1 * Ry1 * Rx1

print("\n1. Комбінація 1: X=30°, Y=90°, Z=45°")
print(f"   α-γ = {np.degrees(a1 - g1):.0f}°")
print("   Координати вершин:")
for i, v in enumerate(vertices):
    res = M1 * v
    print(f"   {names[i]} -> ({res.x:.4f}, {res.y:.4f}, {res.z:.4f})")

# Комбінація 2: X=40°, Y=90°, Z=35°
a2, b2, g2 = np.radians(40), np.radians(90), np.radians(35)
Rx2 = Mat4x4.rotation_x(a2)
Ry2 = Mat4x4.rotation_y(b2)
Rz2 = Mat4x4.rotation_z(g2)
M2 = Rz2 * Ry2 * Rx2

print("\n2. Комбінація 2: X=40°, Y=90°, Z=35°")
print(f"   α-γ = {np.degrees(a2 - g2):.0f}° (X +10°, Z -10°)")
print("   Координати вершин:")
for i, v in enumerate(vertices):
    res = M2 * v
    print(f"   {names[i]} -> ({res.x:.4f}, {res.y:.4f}, {res.z:.4f})")

# Порівняння
print("\n3. Порівняння:")
print(f"   α-γ однакове: {np.degrees(a1 - g1):.0f}° = {np.degrees(a2 - g2):.0f}°")
print(f"   Матриці однакові: {np.allclose(M1.data, M2.data)}")

diffs = []
for i, v in enumerate(vertices):
    r1 = M1 * v
    r2 = M2 * v
    d = np.linalg.norm([r1.x - r2.x, r1.y - r2.y, r1.z - r2.z])
    diffs.append(d)

print(f"   Макс. різниця координат: {max(diffs):.2e}")

print("\nВисновок: X+10° і Z-10° компенсували одне одного.")
print("Осі X і Z 'склеїлись' — це і є gimbal lock.")