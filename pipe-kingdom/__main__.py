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

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.menu_button = arcade.gui.UIFlatButton(text="Menu", width=200)
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="top",
                child=self.menu_button,
            )
        )

        self.sprite_list = SpriteList()

        self.buildings = []

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

    def on_mouse_press(self, x, y, button, modifiers):
        sprite = Sprite("assets/house.png", center_x=x, center_y=y, scale=0.2)
        self.buildings.append(Building(x, y, sprite))
        self.sprite_list.append(sprite)


def main():
    window = PipeKingdom(1920, 1080, "Pipe Kingdom")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
