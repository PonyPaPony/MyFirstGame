import pygame
import config


class Foo: # temporary name
    def create_screen(self, mode):
        width, height = config.SCREEN_SETTINGS[mode]['size']
        method = config.SCREEN_SETTINGS[mode]['method']

        screen = pygame.display.set_mode((width, height), method)

        return screen, *screen.get_size()

    def setup_pygame(self):
        pygame.init()

        screen, w, h = self.create_screen('Window')
        world = pygame.Surface((config.SURW, config.SURH))
        world_rect = world.get_rect()
        pygame.display.set_caption(config.GAME_NAME)
        clock = pygame.time.Clock()
        camera = [0, 0, w, h]
        camera_rect = pygame.Rect(camera)

        return screen, world,  world_rect, clock, camera_rect

    def get_events(self):
        return pygame.event.get()

    def handle_events(self, dc, events):
        for event in events:

            if event.type == pygame.QUIT:
                return False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_BACKQUOTE:
                dc.toggle()
                continue

            if dc.opened:
                dc.handle_event(event)

        return True

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
