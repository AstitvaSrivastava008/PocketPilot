from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle


class AnimatedBar(Widget):

    percentage = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            Color(0.10, 0.32, 0.82, 1)
            self.rect = RoundedRectangle(radius=[8])

        self.bind(
            pos=self.update_rect,
            size=self.update_rect,
            percentage=self.update_rect
        )

    def update_rect(self, *args):

        bar_height = self.height * self.percentage

        self.rect.pos = self.x, self.y
        self.rect.size = self.width, bar_height

    def animate(self, value):

        Animation.cancel_all(self)

        anim = Animation(
            percentage=value,
            duration=1.2
        )

        anim.start(self)