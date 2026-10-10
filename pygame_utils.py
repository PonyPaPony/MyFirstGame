import pygame
import config
from debug import DebugRenderer
from console import DevConsole, DevCommands


class Foo: # temporary name
    def __init__(self):
        self.render_camera = None
        self.render_scale = 1
        self.render_offset = pygame.Vector2(0, 0)


    def create_screen(self, mode):
        width, height = config.SCREEN_SETTINGS[mode]['size']
        method = config.SCREEN_SETTINGS[mode]['method']

        screen = pygame.display.set_mode((width, height), method)

        return screen

    def setup_pygame(self, size='Window'):
        pygame.init()

        screen = self.create_screen(size)
        world = pygame.Surface((config.SURW, config.SURH))
        pygame.display.set_caption(config.GAME_NAME)
        clock = pygame.time.Clock()
        camera = [0, 0, config.CAMERA_W, config.CAMERA_H]
        camera_rect = pygame.Rect(camera)

        return screen, world, clock, camera_rect

    def render(self, screen, world, camera_rect, world_rect):
        render_camera = camera_rect.copy()

        render_camera.width = min(render_camera.width, world_rect.width)
        render_camera.height = min(render_camera.height, world_rect.height)

        render_camera.clamp_ip(world_rect)

        frame = world.subsurface(render_camera)

        screen_w, screen_h = screen.get_size()
        frame_w, frame_h = frame.get_size()

        scale = min(
            screen_w / frame_w,
            screen_h / frame_h
        )

        render_w = int(frame_w * scale)
        render_h = int(frame_h * scale)

        frame = pygame.transform.scale(
            frame,
            (render_w, render_h)
        )

        x = (screen_w - render_w) // 2
        y = (screen_h - render_h) // 2

        screen.fill(config.BACKGROUND_COLOR)
        screen.blit(frame, (x, y))

        self.render_camera = render_camera.copy()
        self.render_scale = scale
        self.render_offset.update(x, y)

        return (
            render_camera,
            scale,
            (x, y),
            (render_w, render_h)
        )

    @staticmethod
    def current_rect(image, pos):
        return image.get_rect(topleft=pos)

    def get_events(self):
        return pygame.event.get()

    def handle_events(self, console, events):
        interact = False
        for event in events:

            if event.type == pygame.QUIT:
                return False, interact

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_ESCAPE:
                return False, interact

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

    def world_mouse(self, events):
        mouse = self.player_mouse(events)

        if mouse is None:
            return None

        if self.render_camera is None:
            return None

        return (
                (mouse - self.render_offset) / self.render_scale
                + pygame.Vector2(self.render_camera.topleft)
        )

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
