import sys
import typing
import pygame
from models import Color, FallingTile
from .pages import Page
from helpers import AutoEnum


class NavigationAction(AutoEnum):
    """Enum to define navigation actions."""

    UP: int
    DOWN: int
    SELECT: int
    NONE: int
    EXIT: int


class MainMenu(Page):
    def __init__(
        self,
        screen,
        height: typing.Union[int, float],
        width: typing.Union[int, float],
        scale: typing.Union[int, float],
        game,
        options: typing.Tuple[str] = None,
    ) -> None:
        super().__init__(screen, height, width, scale, game)
        self.fonts = (
            pygame.font.SysFont(None, int(72 * self.scale)),
            pygame.font.SysFont(None, int(25 * self.scale)),
            pygame.font.SysFont(None, int(48 * self.scale)),
        )
        self.selected_option: int = 0
        self.options = options or ("Play", "Settings", "Info")
        self.texts = ("BRICKMANIA", "Press Q to Quit", "Press Enter to Select")
        self._tiles = None

    def generate(
        self,
        color: Color,
        brick_width: typing.Union[int, float],
        brick_height: typing.Union[int, float],
    ) -> typing.Optional[int]:
        """
        Render the main menu and allow navigation/selection using arrow keys.
        Returns the selected option index when Enter is pressed.
        """
        if not self._tiles:
            self._tiles = [
                FallingTile(
                    brick_width,
                    brick_height,
                    self.width,
                    self.height,
                    self.scale,
                    color,
                )
                for _ in range(20)
            ]
        while True:
            action = self._process_events()
            if action == NavigationAction.UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif action == NavigationAction.DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif action == NavigationAction.SELECT:
                return self.selected_option
            self._render_menu(color)

    def _process_events(self) -> NavigationAction:
        """Process user input and map it to a navigation action."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return NavigationAction.EXIT
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    return NavigationAction.DOWN
                elif event.key == pygame.K_UP:
                    return NavigationAction.UP
                elif event.key == pygame.K_RETURN:
                    return NavigationAction.SELECT
        return NavigationAction.NONE

    def _render_menu(self, color: Color) -> None:
        """Render the main menu UI elements on the screen."""
        self.screen.fill(color.BLACK)
        for tile in self._tiles:
            tile.move(self.height, self.width)
            tile.draw(self.screen)
        self.render_text(
            text=self.texts[0],
            font=self.fonts[0],
            color=color.YELLOW,
            x=(self.width // 2) * self.scale,
            y=(self.height // 2 - 150) * self.scale,
            center=True,
        )
        self.render_text(
            text=self.texts[1],
            font=self.fonts[1],
            color=color.GREY,
            x=10,
            y=(self.height - 10) * self.scale - self.fonts[1].get_height(),
        )
        self.render_text(
            text=self.texts[2],
            font=self.fonts[1],
            color=color.GREY,
            x=self.width * self.scale - 10,
            y=(self.height - 10) * self.scale - self.fonts[1].get_height(),
            center=False,
            right_align=True,
        )
        for i, option in enumerate(self.options):
            color_option = [color.WHITE, color.GREEN][i == self.selected_option]
            self.render_text(
                text=option,
                font=self.fonts[2],
                color=color_option,
                x=(self.width // 2) * self.scale,
                y=(self.height // 2 + i * 60) * self.scale,
                center=True,
            )
        pygame.display.flip()
