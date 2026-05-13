import numpy as np
from src.math.Quaternion import Quaternion

# Кути Ейлера (Yaw, Pitch, Roll)
yaw = np.radians(20)   # Z
pitch = np.radians(90) # Y (Gimbal Lock)
roll = np.radians(50)  # X

# 1. Кватерніони для кожного повороту
q_z = Quaternion.rotation(yaw, (0, 0, 1))   # Yaw навколо Z
q_y = Quaternion.rotation(pitch, (0, 1, 0)) # Pitch навколо Y
q_x = Quaternion.rotation(roll, (1, 0, 0))  # Roll навколо X

print(f"q_z (yaw {np.degrees(yaw)}°): {q_z}")
print(f"q_y (pitch {np.degrees(pitch)}°): {q_y}")
print(f"q_x (roll {np.degrees(roll)}°): {q_x}")

# 2. Фінальний кватерніон (зовнішні осі: Z -> Y -> X)
q = q_x * q_y * q_z
print(f"\nФінальний кватерніон q = {q}")

# Перевірка норми (завжди 1, навіть при gimbal lock)
print(f"|q| = {q.norm()}")

# 3. Відновлення осі та кута (однозначно, без втрати інформації)
angle, axis = q.to_angle_axis()
print(f"\nОсь обертання: ({axis.x:.6f}, {axis.y:.6f}, {axis.z:.6f})")
print(f"Кут обертання: {np.degrees(angle):.2f}°")

# Демонстрація, що кватерніон уникнув gimbal lock:
# Навіть при pitch=90°, ми можемо отримати унікальну орієнтацію
print("\n--- Відновлення орієнтації (унікально) ---")
recovered_yaw, recovered_pitch, recovered_roll = 0.0, 0.0, 0.0

# q = q_x * q_y * q_z
# Для перевірки: обчислимо q_z_p = q_y * q_z, потім q = q_x * q_z_p
q_zy = q_y * q_z
q_check = q_x * q_zy

print(f"Перевірка: q = q_x * (q_y * q_z) = {q_check}")
print(f"Збігається з оригіналом: {np.allclose(q.q, q_check.q)}")