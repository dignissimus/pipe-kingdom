import arcade
import arcade.gui
from arcade import Window, Sprite, SpriteList
from dataclasses import dataclass


@dataclass
class Building:
    x: int
    y: int
    sprite: Sprite


class PipeKingdom(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        self.title = title
        self.show_menu = None
        self.current_building_type = None

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
        self.sewage_button = arcade.gui.UIFlatButton(
            text="Sewage treatment centre", width=400
        )
        self.nothing_button = arcade.gui.UIFlatButton(text="Do nothing", width=400)

        self.house_button.on_click = self.building_setter(True)
        self.sewage_button.on_click = self.building_setter(True)
        self.nothing_button.on_click = self.building_setter(None)

        self.menu_box_layout.add(self.house_button)
        self.menu_box_layout.add(self.sewage_button)
        self.menu_box_layout.add(self.nothing_button)

        self.menu_box.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="top",
                child=self.menu_box_layout,
            )
        )

        self.sprite_list = SpriteList()

        self.buildings = []

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
            sprite = Sprite("assets/house.png", center_x=x, center_y=y, scale=0.1)
            self.buildings.append(Building(x, y, sprite))
            self.sprite_list.append(sprite)


def main():
    window = PipeKingdom(1920, 1080, "Pipe Kingdom")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
