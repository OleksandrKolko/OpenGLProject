import sys
import numpy as np

sys.path.append('src')

from engine.scene.Scene import Scene
from engine.model.Polygon import Polygon

T = np.array([
    [2.934, -0.416, 2.000],
    [0.624, 1.956, 3.400],
    [0, 0, 1]
])

global_points = [(2.0, 3.4), (4.9, 4.0), (4.5, 6.0), (1.6, 5.4)]

T_inv = np.linalg.inv(T)


def transform_point(point, matrix):
    x, y = point
    x_new = matrix[0, 0] * x + matrix[0, 1] * y + matrix[0, 2]
    y_new = matrix[1, 0] * x + matrix[1, 1] * y + matrix[1, 2]
    return (x_new, y_new)


local_points = [transform_point(p, T_inv) for p in global_points]

print("Локальні вершини:")
for p in local_points:
    print(f"({p[0]:.3f}, {p[1]:.3f})")


class Task11Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        local_rect = Polygon(
            local_points[0][0], local_points[0][1],
            local_points[1][0], local_points[1][1],
            local_points[2][0], local_points[2][1],
            local_points[3][0], local_points[3][1],
            color="blue",
            linewidth=2,
            line_style="solid",
            vertices_show=True,
            vertex_color="black",
            vertex_size=30
        )

        global_rect = Polygon(
            global_points[0][0], global_points[0][1],
            global_points[1][0], global_points[1][1],
            global_points[2][0], global_points[2][1],
            global_points[3][0], global_points[3][1],
            color="red",
            linewidth=2,
            line_style="solid",
            vertices_show=True,
            vertex_color="black",
            vertex_size=30
        )

        self["local"] = local_rect
        self["global"] = global_rect


scene = Task11Scene(
    image_size=(10, 8),
    coordinate_rect=(-1, -1, 6, 7),
    title="Task 11: Local and Global Rectangle",
    axis_show=True,
    grid_show=True,
    axis_color=("red", "green"),
    base_axis_show=False
)

scene.show()