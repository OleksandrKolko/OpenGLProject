import sys
import numpy as np

sys.path.append('src')

from engine.scene.Scene import Scene
from engine.model.Polygon import Polygon

T = np.array([
    [0.866, 0.5, 4],
    [0.5, 0.866, 3],
    [0, 0, 1]
])


def transform_point(point, matrix):
    x, y = point
    x_new = matrix[0, 0] * x + matrix[0, 1] * y + matrix[0, 2]
    y_new = matrix[1, 0] * x + matrix[1, 1] * y + matrix[1, 2]
    return (x_new, y_new)


original_points = [(0, 0), (1, 0), (1, 1), (0, 1)]
transformed_points = [transform_point(p, T) for p in original_points]

print("Трансформовані вершини:")
for p in transformed_points:
    print(f"({p[0]:.3f}, {p[1]:.3f})")


class Task12Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        original_square = Polygon(
            0, 0,
            1, 0,
            1, 1,
            0, 1,
            color="gray",
            linewidth=2,
            line_style="solid",
            vertices_show=True,
            vertex_color="black",
            vertex_size=30
        )

        transformed_square = Polygon(
            transformed_points[0][0], transformed_points[0][1],
            transformed_points[1][0], transformed_points[1][1],
            transformed_points[2][0], transformed_points[2][1],
            transformed_points[3][0], transformed_points[3][1],
            color="red",
            linewidth=2,
            line_style="solid",
            vertices_show=True,
            vertex_color="black",
            vertex_size=30
        )

        self["original"] = original_square
        self["transformed"] = transformed_square


scene = Task12Scene(
    image_size=(10, 8),
    coordinate_rect=(-1, -1, 6, 5),
    title="Task 12: Square transformed by matrix T",
    axis_show=True,
    grid_show=True,
    axis_color=("red", "green"),
    base_axis_show=False
)

scene.show()