from helpers.constants import HEIGHT, WIDTH, SCALE, track_path, track1, track2, track3, brick_width, brick_height
from models import Player, Ball, Color
import sys
from pages.main_menu_page import MainMenu
from pages.main_game_page import MainGame
from pages.settings_page import Settings
from pages.info_page import Info
from pages.loading_screen import loading_screen
import pygame


class Game:
    def __init__(
        self,
        *,
        height=HEIGHT,
        width=WIDTH,
        scale=SCALE,
    ) -> None:
        pygame.init()
        # window
        self.height = height
        self.width = width
        self.scale = scale
        self.screen = pygame.display.set_mode((self.width, self.height))
        # colors
        self.colors = Color()
        # entities
        self.player = Player(
            screen=self.screen, height=self.height, width=self.width, scale=self.scale
        )
        self.balls = [
            Ball(
                screen=self.screen,
                height=self.height,
                width=self.width,
                scale=self.scale,
            )
        ]
        # game variables
        self.clock = pygame.time.Clock()
        self.music_files = track_path, track1, track2, track3
        self.music_is_playing = False
        self.is_main_menu = True
        # entity variables
        self.trails = {}
        # pages
        self.main_menu = MainMenu(self.screen, self.height, self.width, self.scale)
        self.settings_page = Settings(
            self.screen,
            self,
            self.height,
            self.width,
            self.scale,
        )
        self.info_page = Info(
            self.screen, self, self.height, self.width, self.scale, self.colors
        )
        self.game_page = MainGame(
            self.screen, self.height, self.width, self.scale, self
        )

    def gameloop(self):
        while True:
            if self.music_is_playing:
                pygame.mixer.music.load(self.music_files[0])
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()
            self.screen.fill(self.colors.BLACK)
            if self.is_main_menu:
                selected_option = self.main_menu.generate(
                    self.colors, brick_width, brick_height, self.clock
                )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if selected_option == 0:
                self.is_main_menu = False
                loading_screen()
                self.is_main_menu = self.game_page.runner(
                    self.colors,
                    self.player,
                    self.balls,
                    brick_height,
                    brick_width,
                    self.trails,
                    self.clock,
                )
            if selected_option == 1:
                self.is_main_menu = False
                self.is_main_menu = self.settings_page.display(self.colors)
            elif selected_option == 2:
                self.is_main_menu = False
                self.is_main_menu = self.info_page.scroll(self.colors)


if __name__ == "__main__":
    game = Game()
    game.gameloop()
