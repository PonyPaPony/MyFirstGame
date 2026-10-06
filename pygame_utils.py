import pygame
import config
from debug import DebugRenderer
from console import DevConsole, DevCommands


class Foo: # temporary name
    def create_screen(self, mode):
        width, height = config.SCREEN_SETTINGS[mode]['size']
        method = config.SCREEN_SETTINGS[mode]['method']

        screen = pygame.display.set_mode((width, height), method)

        return screen, *screen.get_size()

    def setup_pygame(self, size='Window'):
        pygame.init()

        screen, w, h = self.create_screen(size)
        world = pygame.Surface((config.SURW, config.SURH))
        world_rect = world.get_rect()
        pygame.display.set_caption(config.GAME_NAME)
        clock = pygame.time.Clock()
        camera = [0, 0, w, h]
        camera_rect = pygame.Rect(camera)

        return screen, world,  world_rect, clock, camera_rect

    def get_events(self):
        return pygame.event.get()

    def handle_events(self, console, events):
        interact = False
        for event in events:

            if event.type == pygame.QUIT:
                return False, interact

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_BACKQUOTE:
                console.toggle()
                continue

            if event.key == pygame.K_e:
                interact = True

            if console.opened:
                console.handle_event(event)

        return True, interact

    def player_mouse(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return pygame.Vector2(event.pos)
                else:
                    return None
        return None

    def world_mouse(self, events, camera_rect):
        mouse = self.player_mouse(events)

        if mouse is None:
            return None

        return mouse + camera_rect.topleft

    def handle_move(self, keys):
        dx, dy = 0, 0
        for key, (mx, my) in config.MOVEMENT.items():
            if keys[key]:
                dx += mx
                dy += my
        return dx, dy

    @staticmethod
    def units_draw(*args, place):
        for arg in args:
            arg.draw(place)

    @staticmethod
    def dev_utils(*args, screen, world_time):
        debug = DebugRenderer(screen)
        cmd = DevCommands(*args, world_time=world_time, debug_render=debug)
        console = DevConsole()

        return debug, cmd, console

class WorldTime:
    def __init__(self):
        self.total_minutes = 0

    def update(self, dt):
        self.total_minutes += dt

    def get_calendar_day(self):
        days = self.get_day()

        year = days // 360
        month = (days % 360) // 30
        day = days % 30

        return year, month, day

    def get_day(self):
        return int(self.total_minutes // 1440)

    def get_hour(self):
        return int(self.total_minutes // 60) % 24

    def get_minute(self):
        return int(self.total_minutes) % 60

    def set_time(self, minutes):
        self.total_minutes = minutes
