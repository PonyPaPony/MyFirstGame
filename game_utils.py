import pygame
import config
from console import Console, ConsoleCommands
from debug import DebugRenderer


class GameUtils:
    """
    Класс для настройки игрового окна и сопутствующих функций
    """
    def __init__(self):
        self.screen = None
        self.world = None
        self.clock = None
        self.camera_rect = None
        self.world_rect = None

        self.render_camera = None
        self.render_scale = 1
        self.render_size = None
        self.render_offset = pygame.Vector2(0, 0)

        self.mouse = Mouse(self)
        self.devs = None
        self.console = None

    @staticmethod
    def create_screen(mode):
        width, height = config.SCREEN_SETTINGS[mode]['size']
        method = config.SCREEN_SETTINGS[mode]['method']

        return pygame.display.set_mode((width, height), method)

    @staticmethod
    def current_rect(image, pos):
        return image.get_rect(topleft=pos)

    def setup_pygame(self, size='window'):
        pygame.init()

        self.screen = self.create_screen(size)
        self.world = pygame.Surface(config.SURFACE)
        self.clock = pygame.time.Clock()
        self.camera_rect = pygame.Rect(*self.get_camera(size))
        pygame.display.set_caption(config.GAME_NAME)

        #! NOTE: Создаём инструменты разработчика
        self.devs = Devs(self)
        self.console = self.devs.console

        return self


    def get_camera(self, size):
        settings = config.SCREEN_SETTINGS[size]['camera']
        if settings is None:
            w, h = self.screen.get_size()

            settings = (
                min(w, 2560),
                min(h, 1440)
            )

        return [0, 0, *settings]

    def follow_camera(self, target):
        self.camera_rect.center = target.get_rect().center
        self.camera_rect.clamp_ip(self.world_rect)

    @staticmethod
    def get_events():
        return pygame.event.get()

    def get_delta_time(self):
        return self.clock.tick(config.FPS) / 1000


    #! NOTE: Обработчик событий и нажатий
    def handle_events(self, events):
        interact = False
        for event in events:
            if event.type == pygame.QUIT:
                return False, interact

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_BACKQUOTE:
                self.console.toggle()
                continue

            if self.console.opened:
                self.console.handle_event(event)
                continue

            match event.key:
                case pygame.K_ESCAPE:
                    return False, interact

                case pygame.K_e:
                    interact = True

        return True, interact

    @staticmethod
    def handle_move(keys):
        dx, dy = 0, 0
        for key, (mx, my) in config.MOVEMENT_KEYS.items():
            if keys[key]:
                dx += mx
                dy += my
        return dx, dy

    #! NOTE: Настройки рендера камеры и еже сними
    def render_clamp(self):
        world_rect = self.world_rect

        self.render_camera.size = (
            min(self.render_camera.width, world_rect.width),
            min(self.render_camera.height, world_rect.height)
        )

        self.render_camera.center = self.camera_rect.center
        self.render_camera.clamp_ip(world_rect)

        return self.render_camera

    def set_world_rect(self, rect):
        self.world_rect = rect

    def get_scaled(self, frame):
        screen_w, screen_h = self.screen.get_size()
        frame_w, frame_h = frame.get_size()

        self.render_scale = min(screen_w / frame_w, screen_h / frame_h)

        render_w = int(frame_w * self.render_scale)
        render_h = int(frame_h * self.render_scale)

        return render_w, render_h

    def get_rendered_pos(self, render_size):
        w, h = self.screen.get_size()
        render_w, render_h = render_size

        x = (w - render_w) // 2
        y = (h - render_h) // 2

        return x, y

    def render(self, player=None):
        if player is not None:
            self.follow_camera(player)

        self.render_camera = self.camera_rect.copy()
        self.render_clamp()

        frame = self.world.subsurface(self.render_camera)

        self.render_size = self.get_scaled(frame)
        frame = pygame.transform.scale(frame, self.render_size)

        render_pos = self.get_rendered_pos(self.render_size)

        self.screen.fill(config.BACKGROUND_COLOR)
        self.screen.blit(frame, render_pos)

        self.render_offset.update(render_pos)

    @property
    def render_settings(self):
        return (
            self.render_camera,
            self.render_scale,
            tuple(self.render_offset),
            self.render_size
        )

    #! NOTE: Отрисовка всех юнитов
    def render_units(self, *args):
        for arg in args:
            arg.draw(self.world)


class Mouse:
    def __init__(self, game):
        self.game = game

    @staticmethod
    def player_mouse(events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    return pygame.Vector2(event.pos)
        return None

    def world_mouse(self, events):
        mouse = self.player_mouse(events)

        if mouse is None or self.game.render_camera is None:
            return None

        return (
            (mouse - self.game.render_offset)
            / self.game.render_scale
            + pygame.Vector2(self.game.render_camera.topleft)
        )

class Devs:
    def __init__(self, game):
        self.game = game

        self.console = Console()
        self.debug = DebugRenderer(game.screen)
        self.commands = ConsoleCommands(self.debug)
        self.commands.register_commands(self.console)


    def connect(self, units, spawner, world_time, space_id):
        self.commands.units = units
        self.commands.spawner = spawner
        self.commands.world_time = world_time
        self.commands.get_current_space = space_id

    def draw(self, objects=None):
        self.debug.set_camera(*self.game.render_settings)
        self.debug.debug_draw(
            *self.commands.units.get_all(),
            line_from=self.commands.units.player,
            player=self.commands.units.player,
            enemies=self.commands.units.enemies
        )
        self.debug.draw_building(objects)
        self.debug.draw_building(objects, color='green', arg='threshold')
        self.debug.draw_attack_status(self.commands.units.enemies, self.commands.units.player)
        #! NOTE: Консоль рисуем последней, поверх игры
        self.console.console_draw(self.game.screen)


class WorldTime:
    def __init__(self):
        self.total_minutes = 0

    def update(self, dt):
        self.total_minutes += dt

    def get_calendar_day(self):
        days = self.get_day()

        year = days // config.CALENDAR['year']
        month = (days % config.CALENDAR['year']) // config.CALENDAR['month']
        day = days % config.CALENDAR['month']

        yield year, month, day

    def get_day(self):
        return int(self.total_minutes // config.TIMES['day'])

    def get_hour(self):
        return int(self.total_minutes // config.TIMES['hour']) % 24

    def get_minute(self):
        return int(self.total_minutes) % 60

    #! NOTE: to develop moment
    def set_time(self, minutes):
        self.total_minutes = int(minutes)