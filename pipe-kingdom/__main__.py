import itertools
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple

import arcade
import arcade.gui
from arcade import Sprite, SpriteList, Window

GRID_WIDTH = 115
GRID_HEIGHT = 115


# x, y co-ordinates
Pipe = Tuple[int, int]


class BuildingType(Enum):
    HOUSE = auto()
    TREATMENT_CENTRE = auto()
    VERTICAL_PIPE = auto()
    HORIZONTAL_PIPE = auto()
    DOWN_RIGHT_PIPE = auto()
    UP_RIGHT_PIPE = auto()
    DOWN_LEFT_PIPE = auto()
    UP_LEFT_PIPE = auto()
    CROSS_PIPE = auto()
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
            case BuildingType.DOWN_RIGHT_PIPE:
                return "down-right.png"
            case BuildingType.UP_RIGHT_PIPE:
                return "up-right.png"
            case BuildingType.DOWN_LEFT_PIPE:
                return "down-left.png"
            case BuildingType.UP_LEFT_PIPE:
                return "up-left.png"
            case BuildingType.CHEMICAL_PLANT:
                return "chemical.png"
            case BuildingType.WATER_PUMP:
                return "pump.png"

    @property
    def is_pipe(self):
        match self:
            case BuildingType.VERTICAL_PIPE | BuildingType.HORIZONTAL_PIPE | BuildingType.DOWN_RIGHT_PIPE | BuildingType.UP_RIGHT_PIPE | BuildingType.DOWN_LEFT_PIPE | BuildingType.UP_LEFT_PIPE:
                return True
        return False

    @property
    def is_big(self):
        return not self.is_pipe
        #return (
        #    self != BuildingType.VERTICAL_PIPE and self != BuildingType.HORIZONTAL_PIPE
        #)


@dataclass
class Building:
    x: int
    y: int
    sprite: Sprite
    building_type: BuildingType = None
    pipes: list[Pipe] = field(default_factory=list)
    buildings: list = field(default_factory=list)

    def squared_distance(self, x, y):
        return (self.x - x) ** 2 + (self.y - y) ** 2

    def distance(self, x, y):
        return math.sqrt(self.squared_distance(x, y))


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
            [None for _ in range(height // GRID_HEIGHT + 3)]
            for _ in range(width // GRID_WIDTH + 3)
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
        self.chemical_plant_button = arcade.gui.UIFlatButton(
            text="Chemical plant", width=400
        )
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
        self.water_pump_button.on_click = self.building_setter(BuildingType.WATER_PUMP)

        self.nothing_button.on_click = self.building_setter(None)

        self.menu_box_layout.add(self.house_button)
        self.menu_box_layout.add(self.sewage_button)
        self.menu_box_layout.add(self.nothing_button)
        self.menu_box_layout.add(self.horizontal_pipe_button)
        self.menu_box_layout.add(self.vertical_pipe_button)
        self.menu_box_layout.add(self.water_pump_button)
        self.menu_box_layout.add(self.chemical_plant_button)

        self.win = False
        self.message_box_manager = arcade.gui.UIManager()
        self.message_box = arcade.gui.UIMessageBox(
            width=300,
            height=400,
            message_text="You have connected all of the houses! You have delivered clean water to the people!",
            buttons=["OK"],
        )
        self.message_box_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="top",
                child=self.message_box,
            )
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

        self.money = 3000

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
        if self.win:
            self.message_box_manager.draw()

        arcade.draw_text(
            f"Pipe money: ${self.money}",
            50,
            self.height - 50,
            arcade.color.BLACK,
            14,
            width=self.width - 200,
            align="left",
        )

    def connected_buildings(self, pipe_x, pipe_y, A=None):
        if A == None:
            A = []
        if pipe_x >= len(self.pipes) or pipe_y >= len(self.pipes[pipe_x]):
            return []

        pipe = self.pipes[pipe_x][pipe_y]
        if not pipe:
            return []
        if pipe in A:
            return []
        A.append(pipe)

        buildings = []
        buildings.extend(pipe.buildings)
        for _x in [-1, 0, 1]:
            for _y in [-1, 0, 1]:
                other_x = _x + pipe_x
                other_y = _y + pipe_y
                buildings.extend(self.connected_buildings(other_x, other_y, A))
        return buildings

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.current_building_type:
            return

        prev = self.current_building_type

        buildings = []

        scale = 0.1
        if self.current_building_type.is_pipe:
            pipe_x = x // GRID_WIDTH + 1
            pipe_y = y // GRID_HEIGHT + 1
            x = pipe_x * GRID_WIDTH
            y = pipe_y * GRID_HEIGHT
            scale = 0.4
            if self.pipes[pipe_x][pipe_y + 1] and self.pipes[pipe_x + 1][pipe_y]:
                self.current_building_type = BuildingType.UP_RIGHT_PIPE
            if self.pipes[pipe_x + 1][pipe_y] and self.pipes[pipe_x - 1][pipe_y]:
                self.current_building_type = BuildingType.HORIZONTAL_PIPE
            if self.pipes[pipe_x][pipe_y - 1] and self.pipes[pipe_x][pipe_y + 1]:
                self.current_building_type = BuildingType.VERTICAL_PIPE
            if self.pipes[pipe_x][pipe_y - 1] and self.pipes[pipe_x + 1][pipe_y]:
                self.current_building_type = BuildingType.DOWN_RIGHT_PIPE
            if self.pipes[pipe_x][pipe_y - 1] and self.pipes[pipe_x - 1][pipe_y]:
                self.current_building_type = BuildingType.DOWN_LEFT_PIPE
            if self.pipes[pipe_x][pipe_y + 1] and self.pipes[pipe_x - 1][pipe_y]:
                self.current_building_type = BuildingType.UP_LEFT_PIPE

        if self.current_building_type.is_big:
            for building in self.buildings:
                if building.distance(x, y) < 100 and building.building_type.is_big:
                    return
        else:
            # In this case, we're placing a pipe on the map
            for building in self.buildings:
                if building.distance(x, y) < 150 and building.building_type.is_big:
                    building.pipes.append((pipe_x, pipe_y))
                    buildings.append(building)

            if y < 200:
                # The hackiest of hacks
                buildings.append(None)

        sprite = Sprite(
            self.current_building_type.resource, center_x=x, center_y=y, scale=scale
        )
        building = Building(
            x, y, sprite, buildings=buildings, building_type=self.current_building_type
        )
        self.buildings.append(building)
        self.sprite_list.append(sprite)

        if self.current_building_type.is_pipe:
            self.pipes[pipe_x][pipe_y] = building
            self.money -= 50

        elif self.current_building_type == BuildingType.CHEMICAL_PLANT:
            self.money -= 200
        elif self.current_building_type == BuildingType.TREATMENT_CENTRE:
            self.money -= 300
        elif self.current_building_type == BuildingType.WATER_PUMP:
            self.money -= 100

        self.current_building_type = prev

        # print(self.connected_buildings(pipe_x, pipe_y))

        # Horrible algorithm
        z = []
        for building in self.buildings:
            if building.building_type.is_pipe:
                continue
            v = False
            for (x, y) in itertools.product(
                range(self.width // GRID_WIDTH), range(self.height // GRID_HEIGHT)
            ):
                pipe = self.pipes[x][y]
                if not pipe:
                    continue
                cb = self.connected_buildings(x, y)
                if building in cb and None in cb:
                    v = True
            z.append(v)

        if len(z) > 0 and all(z):
            # print("win")
            self.win = True


def main():
    window = PipeKingdom(1920, 1080, "Pipe Kingdom")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
