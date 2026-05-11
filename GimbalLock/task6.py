import numpy as np
from src.engine.model.Vector import Vector
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Mat4x4 import Mat4x4

print("=" * 60)
print("ЗАВДАННЯ 6: Інтерполяція в зоні сингулярності")
print("=" * 60)

# Положення А (0,0,0) -> Б (90,90,90), 10 кроків
steps = 10
angles_a = np.array([0.0, 0.0, 0.0])
angles_b = np.array([90.0, 90.0, 90.0])

print("\nКрок |  X   |  Y   |  Z   | Вектор погляду [0,0,1]")
print("-" * 55)

trajectory = []
for i in range(steps + 1):
    t = i / steps
    angles = angles_a + (angles_b - angles_a) * t
    ax, ay, az = np.radians(angles)
    R = Mat4x4.rotation_euler(ax, ay, az, Mat4x4.XYZ)

    look = R * np.array([0, 0, 1, 1])
    look_dir = np.array([look[0], look[1], look[2]])
    trajectory.append(look_dir)

    print(
        f"  {i:2d}  | {angles[0]:5.0f} | {angles[1]:5.0f} | {angles[2]:5.0f} | ({look_dir[0]:7.4f}, {look_dir[1]:7.4f}, {look_dir[2]:7.4f})")

# Аналіз
print("\nАналіз траєкторії:")
for i in range(1, len(trajectory)):
    angle_change = np.degrees(np.arccos(np.clip(np.dot(trajectory[i - 1], trajectory[i]), -1, 1)))
    print(f"  Крок {i}: зміна напрямку = {angle_change:.2f}°")

print("\nПроблема: при Y≈90° малі зміни X та Z дають великі стрибки напрямку.")
print("Рух нерівномірний — це наслідок gimbal lock при інтерполяції кутів Ейлера.")

# Візуалізація
LOOK_KEY = "look"
VECTORS = [f"v{i}" for i in range(steps + 1)]


class Task6Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i, d in enumerate(trajectory):
            vec = Vector(0, 0, 0, *d, color="red", linewidth=2.0)
            self[VECTORS[i]] = vec


def frame1(scene):
    for i in range(steps + 1):
        scene[VECTORS[i]].color = "blue" if i == 0 or i == steps else "red"
        scene[VECTORS[i]].linewidth = 3.0 if i == 0 or i == steps else 1.0


scene = Task6Scene(
    title="Завдання 6: Траєкторія погляду (Lerp кутів Ейлера)",
    coordinate_rect=(-1, -1, -1, 1, 1, 1),
    axis_show_from_origin=True,
)
scene.add_frames(frame1)
scene.show()