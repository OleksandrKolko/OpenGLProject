import sys
import numpy as np

sys.path.append('src')

from engine.scene.Scene import Scene
from engine.model.Polygon import Polygon

FIGURE_KEY = "square"


class Task1Scene(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        square = Polygon(
            0, 0,
            1, 0,
            1, 1,
            0, 1,
            color="gray",
            linewidth=2,
            line_style="solid"
        )

        self[FIGURE_KEY] = square


def initial_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    square["color"] = "gray"
    square["line_style"] = "solid"
    square.rotation = 0
    square.translation = (0, 0)


def transformed_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    square["color"] = "red"
    square["line_style"] = "solid"

    square.rotation = np.radians(30)

    square.translation = (2, 3)


scene = Task1Scene(
    image_size=(8, 6),
    coordinate_rect=(-1, -1, 5, 5),
    title="Task 1: Rotation 30° + Translation (2,3)",
    axis_show=True,
    grid_show=True,
    axis_color=("red", "green"),
    base_axis_show=False
)

scene.add_frames(initial_frame, transformed_frame)

scene.show()