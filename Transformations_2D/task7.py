import sys
import numpy as np

sys.path.append('src')

from engine.scene.Scene import Scene
from engine.model.Polygon import Polygon

FIGURE_KEY = "square"


class Task7Scene(Scene):
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


def pivot1_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    square["color"] = "red"
    square["line_style"] = "solid"

    square.pivot(0.5, 0.5)
    square.rotation = np.radians(60)
    square.translation = (0, 0)


def pivot2_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    square["color"] = "blue"
    square["line_style"] = "solid"

    square.pivot(0, 1)
    square.rotation = np.radians(60)
    square.translation = (0, 0)


def pivot3_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    square["color"] = "green"
    square["line_style"] = "solid"

    square.pivot(1, 1)
    square.rotation = np.radians(60)
    square.translation = (0, 0)


def pivot4_frame(scene: Scene):
    square: Polygon = scene[FIGURE_KEY]
    square["color"] = "orange"
    square["line_style"] = "solid"

    square.pivot(2, 2)
    square.rotation = np.radians(60)
    square.translation = (0, 0)


scene = Task7Scene(
    image_size=(10, 8),
    coordinate_rect=(-1, -2, 5, 3),
    title="Task 7: Rotation around different pivots (60°)",
    axis_show=True,
    grid_show=True,
    axis_color=("red", "green"),
    base_axis_show=False
)

scene.add_frames(initial_frame, pivot1_frame, pivot2_frame, pivot3_frame, pivot4_frame)
scene.show()