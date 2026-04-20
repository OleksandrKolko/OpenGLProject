import sys
import numpy as np

sys.path.append('src')

from engine.scene.Scene import Scene
from engine.model.Polygon import Polygon

FIGURE_KEY = "square"


class Task6Scene(Scene):
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
    square.scale = (1, 1)


def order1_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    square["color"] = "red"
    square["line_style"] = "solid"

    square.scale = (1, 3)
    square.rotation = np.radians(60)
    square.translation = (2, 3)


def order2_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    square["color"] = "blue"
    square["line_style"] = "solid"

    square.translation = (2, 3)
    square.scale = (1, 3)
    square.rotation = np.radians(60)


scene = Task6Scene(
    image_size=(8, 6),
    coordinate_rect=(-2, -4, 11, 7),
    title="Task 6: Two Orders of Transformations",
    axis_show=True,
    grid_show=True,
    axis_color=("red", "green"),
    base_axis_show=False
)

scene.add_frames(initial_frame, order1_frame, order2_frame)
scene.show()