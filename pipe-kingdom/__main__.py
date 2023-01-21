import math
from dataclasses import dataclass
from enum import Enum, auto

import arcade
import arcade.gui
from arcade import Sprite, SpriteList, Window


GRID_WIDTH = 30
GRID_HEIGHT = 40


@dataclass
class Building:
    x: int
    y: int
    sprite: Sprite

    def squared_distance(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2

    def distance(self, x, y):
        return math.sqrt(self.squared_distance(x, y))


class BuildingType(Enum):
    HOUSE = auto()
    TREATMENT_CENTRE = auto()
    VERTICAL_PIPE = auto()
    HORIZONTAL_PIPE = auto()
    CHEMICAL_PLANT = auto()
    WATER_PUMP = auto()

    @property
    def resource(self):
        return "assets/" + self.resource_name

    @property
    def resource_name(self):
        match self:
            case BuildingType.HOUSE:
                return "house.png"
            case BuildingType.TREATMENT_CENTRE:
                return "treatmentplant.png"
            case BuildingType.VERTICAL_PIPE:
                return "vertical-pipe.png"
            case BuildingType.HORIZONTAL_PIPE:
                return "horizontal-pipe.png"
            case BuildingType.CHEMICAL_PLANT:
                return "chemical.png"
            case BuildingType.WATER_PUMP:
                return "pump.png"


    @property
    def is_pipe(self):
        match self:
            case BuildingType.VERTICAL_PIPE | BuildingType.HORIZONTAL_PIPE:
                return True
        return False

    @property
    def is_big(self):
        return self != BuildingType.VERTICAL_PIPE and self != BuildingType.HORIZONTAL_PIPE


class PipeKingdom(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        self.title = title
        self.show_menu = None
        self.current_building_type = None
        self.building_pipes = False

        self.pipes = [
            [None for _ in range(height // GRID_HEIGHT)]
            for _ in range(width // GRID_WIDTH)
        ]

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.menu_button = arcade.gui.UIFlatButton(text="Show menu", width=200)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="top",
                child=self.menu_button,
            )
        )
        self.menu_button.on_click = self.toggle_menu

        self.menu_box = arcade.gui.UIManager()
        self.menu_box.enable()

        self.menu_box_layout = arcade.gui.UIBoxLayout(space_between=7.5)
        self.house_button = arcade.gui.UIFlatButton(text="House", width=400)
        self.horizontal_pipe_button = arcade.gui.UIFlatButton(
            text="Horizontal pipe", width=400
        )
        self.vertical_pipe_button = arcade.gui.UIFlatButton(
            text="Vertical pipe", width=400
        )
        self.sewage_button = arcade.gui.UIFlatButton(
            text="Sewage treatment centre", width=400
        )
        self.nothing_button = arcade.gui.UIFlatButton(text="Do nothing", width=400)
        self.chemical_plant_button = arcade.gui.UIFlatButton(text="Chemical plant", width=400)
        self.water_pump_button = arcade.gui.UIFlatButton(text="Water pump", width=400)

        self.house_button.on_click = self.building_setter(BuildingType.HOUSE)
        self.sewage_button.on_click = self.building_setter(
            BuildingType.TREATMENT_CENTRE
        )
        self.horizontal_pipe_button.on_click = self.building_setter(
            BuildingType.HORIZONTAL_PIPE
        )
        self.vertical_pipe_button.on_click = self.building_setter(
            BuildingType.VERTICAL_PIPE
        )
        self.chemical_plant_button.on_click = self.building_setter(
            BuildingType.CHEMICAL_PLANT
        )
        self.water_pump_button.on_click = self.building_setter(
            BuildingType.WATER_PUMP
        )

        self.nothing_button.on_click = self.building_setter(None)

        self.menu_box_layout.add(self.house_button)
        self.menu_box_layout.add(self.sewage_button)
        self.menu_box_layout.add(self.nothing_button)
        self.menu_box_layout.add(self.horizontal_pipe_button)
        self.menu_box_layout.add(self.vertical_pipe_button)
        self.menu_box_layout.add(self.water_pump_button)
        self.menu_box_layout.add(self.chemical_plant_button)

        self.message_box_manager = arcade.gui.UIManager()
        self.message_box = arcade.gui.UIMessageBox(
            width=300,
            height=400,
            message_text="Too close to existing building",
            buttons=["OK"],
        )

        self.menu_box.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="top",
                child=self.menu_box_layout,
            )
        )

        self.sprite_list = SpriteList()

        self.buildings = []

    def toggle_building_pipes(self):
        self.building_pipes = not self.building_pipes

    def building_setter(self, building_type):
        def set(event):
            self.current_building_type = building_type

        return set

    def toggle_menu(self, event):
        self.show_menu = not self.show_menu

    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture("assets/background.jpg")

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.width, self.height, self.background
        )
        self.sprite_list.draw()
        self.manager.draw()
        if self.show_menu:
            self.menu_box.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_building_type:
            if self.current_building_type.is_big:
                for building in self.buildings:
                    if building.distance(x, y) < 100:
                        return

            if self.current_building_type.is_pipe:
                pipe_x = x // GRID_WIDTH
                pipe_y = (y + 30) // GRID_HEIGHT
                x = pipe_x * GRID_WIDTH
                y = pipe_y * GRID_HEIGHT

            sprite = Sprite(
                self.current_building_type.resource, center_x=x, center_y=y, scale=0.1
            )
            self.buildings.append(Building(x, y, sprite))
            self.sprite_list.append(sprite)

            if self.current_building_type.is_pipe:
                self.pipes[pipe_x][pipe_y] = sprite


def main():
    window = PipeKingdom(1920, 1080, "Pipe Kingdom")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
