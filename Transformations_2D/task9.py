import sys
import numpy as np

sys.path.append('src')

from engine.scene.Scene import Scene
from engine.model.Polygon import Polygon

FIGURE_KEY = "square"
PIVOT_KEY = "pivot_point"


class Task9Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        square = Polygon(
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

        pivot = Polygon(
            1, 1,
            color="black",
            vertices_show=True,
            vertex_color="purple",
            vertex_size=50
        )

        self[FIGURE_KEY] = square
        self[PIVOT_KEY] = pivot


def initial_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    pivot: Polygon = scene[PIVOT_KEY]

    square["color"] = "gray"
    square["line_style"] = "solid"
    square.rotation = 0
    square.translation = (0, 0)
    square.scale = (1, 1)

    pivot.pivot(1, 1)
    pivot.scale = (1, 1)
    pivot.translation = (0, 0)


def order1_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    pivot: Polygon = scene[PIVOT_KEY]

    square["color"] = "red"
    square["line_style"] = "solid"

    square.pivot(1, 1)
    square.scale = (2, 1)
    square.translation = (3, -2)

    pivot.pivot(1, 1)
    pivot.scale = (1, 1)
    pivot.translation = (3, -2)


def order2_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    pivot: Polygon = scene[PIVOT_KEY]

    square["color"] = "blue"
    square["line_style"] = "solid"

    square.translation = (3, -2)
    square.pivot(1, 1)
    square.scale = (2, 1)

    pivot.translation = (3, -2)
    pivot.pivot(1, 1)
    pivot.scale = (1, 1)


scene = Task9Scene(
    image_size=(10, 8),
    coordinate_rect=(-1, -4, 9, 3),
    title="Task 9: Two Orders (Scale around pivot (1,1) + Translation)",
    axis_show=True,
    grid_show=True,
    axis_color=("red", "green"),
    base_axis_show=False
)

scene.add_frames(initial_frame, order1_frame, order2_frame)
scene.show()