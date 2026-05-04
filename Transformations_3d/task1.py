import sys
import numpy as np

sys.path.append('src')

from src.engine.scene.Scene import Scene
from src.math.Vec3 import Vec3
from src.math.Mat4x4 import Mat4x4


def draw_cube(plt_axis, vertices, edges, color="gray", alpha=0.5):
    """Малює куб через його грані."""
    # Грані куба (кожна грань — це 4 вершини в порядку обходу)
    faces = [
        [0, 1, 2, 3],  # нижня
        [4, 5, 6, 7],  # верхня
        [0, 1, 5, 4],  # передня
        [2, 3, 7, 6],  # задня
        [1, 2, 6, 5],  # права
        [0, 3, 7, 4]  # ліва
    ]

    for face in faces:
        face_vertices = [vertices[i] for i in face]
        # Конвертуємо Vec3 у списки для сумісності з Poly3DCollection
        face_points = [[v.x, v.y, v.z] for v in face_vertices]

        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        polygon = Poly3DCollection([face_points], alpha=alpha, edgecolor=color, facecolor=color)
        plt_axis.add_collection3d(polygon)

vertices = [
    Vec3(0, 0, 0), Vec3(1, 0, 0), Vec3(1, 1, 0), Vec3(0, 1, 0),
    Vec3(0, 0, 1), Vec3(1, 0, 1), Vec3(1, 1, 1), Vec3(0, 1, 1)
]

axis = Vec3(1, 1, 0)
angle_deg = 45

R = Mat4x4.rotation(angle_deg, axis, is_radians=False)
T = Mat4x4.translation(2, -1, 3)
M = T * R  # спочатку обертання, потім переміщення

transformed_vertices = [M * v for v in vertices]

def initial_frame(scene: Scene):
    draw_cube(scene.plt_axis, vertices, None, color="gray", alpha=0.3)


def transformed_frame(scene: Scene):
    draw_cube(scene.plt_axis, transformed_vertices, None, color="red", alpha=0.5)

scene = Scene(
    coordinate_rect=(-3, -3, -3, 6, 6, 6),
    title="3D Task 1: Rotation around (1,1,0) 45° + Translation (2,-1,3)",
    axis_show=True,
    grid_show=True
)

scene.add_frames(initial_frame, transformed_frame)
scene.show()