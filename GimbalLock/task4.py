import numpy as np
from src.math.Mat4x4 import Mat4x4

print("=" * 60)
print("ЗАВДАННЯ 4: Gimbal Lock")
print("=" * 60)

# 1. Загальний вигляд R = Rz * Ry * Rx
print("\n1. R = Rz(γ) * Ry(β) * Rx(α):")
print("R = [")
print("  [cosβ·cosγ, sinα·sinβ·cosγ - cosα·sinγ, cosα·sinβ·cosγ + sinα·sinγ],")
print("  [cosβ·sinγ, sinα·sinβ·sinγ + cosα·cosγ, cosα·sinβ·sinγ - sinα·cosγ],")
print("  [  -sinβ  ,         sinα·cosβ          ,         cosα·cosβ          ]")
print("]")

# 2. Підстановка β = 90°
print("\n2. β = 90°: cos(90°)=0, sin(90°)=1")
print("R(β=90°) = [")
print("  [   0  , sinα·cosγ - cosα·sinγ, cosα·cosγ + sinα·sinγ],")
print("  [   0  , sinα·sinγ + cosα·cosγ, cosα·sinγ - sinα·cosγ],")
print("  [  -1  ,           0          ,           0           ]")
print("]")

# 3. Тригонометричні тотожності
print("\n3. Тотожності:")
print("   sin(α-γ) = sinα·cosγ - cosα·sinγ")
print("   cos(α-γ) = cosα·cosγ + sinα·sinγ")

print("\n   R[0,1] = sinα·cosγ - cosα·sinγ = sin(α-γ)")
print("   R[0,2] = cosα·cosγ + sinα·sinγ = cos(α-γ)")
print("   R[1,1] = sinα·sinγ + cosα·cosγ = cos(α-γ)")
print("   R[1,2] = cosα·sinγ - sinα·cosγ = sin(α-γ)")

# 4. Фінальна матриця
print("\n4. R(α, 90°, γ) = [")
print("  [ -sin(α-γ),    0    , cos(α-γ) ],")
print("  [  cos(α-γ),    0    , sin(α-γ) ],")
print("  [     0    ,   -1    ,    0     ]")
print("]")

# 5. Перевірка
print("\n5. Перевірка (α=45°, β=90°, γ=30°):")
a, b, g = np.radians(45), np.radians(90), np.radians(30)
R = Mat4x4.rotation_euler(a, b, g, Mat4x4.XYZ)
print(R)
print(f"α-γ = 15°, sin = {np.sin(a-g):.4f}, cos = {np.cos(a-g):.4f}")

# 6. Демонстрація
print("\n6. Демонстрація: різні α,γ при однаковому (α-γ) = та сама матриця")
a1, g1 = np.radians(45), np.radians(30)  # α-γ = 15°
a2, g2 = np.radians(60), np.radians(45)  # α-γ = 15°
R1 = Mat4x4.rotation_euler(a1, np.radians(90), g1, Mat4x4.XYZ)
R2 = Mat4x4.rotation_euler(a2, np.radians(90), g2, Mat4x4.XYZ)
print(f"  (45°, 90°, 30°): α-γ = {np.degrees(a1-g1):.0f}°")
print(f"  (60°, 90°, 45°): α-γ = {np.degrees(a2-g2):.0f}°")
print(f"  Матриці однакові: {np.allclose(R1.data, R2.data)}")

print("\nВисновок: при β=90° орієнтація залежить лише від (α-γ).")
print("Осі X і Z збігаються — втрата одного ступеня вільності.")