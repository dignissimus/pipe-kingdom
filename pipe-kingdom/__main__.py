import arcade
from arcade import Window


class PipeKingdom(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        self.title = title

    def setup(self):
        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture("assets/background.jpg")

    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(
            0, 0, self.width, self.height, self.background
        )
        arcade.draw_text(
            "Menu",
            self.width - 400,
            self.height - 100,
            arcade.color.BLACK,
            30,
            font_name="Kenney Blocks",
        )


def main():
    window = PipeKingdom(1920, 1080, "Pipe Kingdom")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
