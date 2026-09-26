import config
import pygame
from Enemy import Enemy
from entity import Entity
from debug import DebugRenderer
from console import DevConsole, DevCommands
from spawner import multi_spawn, spawn_creature


def create_screen(mode):
    width, height = config.SCREEN_SETTINGS[mode]['size']
    method = config.SCREEN_SETTINGS[mode]['method']

    screen = pygame.display.set_mode((width, height), method)

    return screen, *screen.get_size()

def setup_pygame():
    pygame.init()

    screen, w, h = create_screen('Window')
    world = pygame.Surface((config.SURW, config.SURH))
    world_rect = world.get_rect()
    pygame.display.set_caption(config.GAME_NAME)
    clock = pygame.time.Clock()
    camera = [0, 0, w, h]
    camera_rect = pygame.Rect(camera)

    return screen, world,  world_rect, clock, camera_rect

def handle_events(dc):
    for event in pygame.event.get():

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

def handle_move(keys):
    dx, dy = 0, 0
    for key, (mx, my) in config.MOVEMENT.items():
        if keys[key]:
            dx += mx
            dy += my
    return dx, dy

screen, world, world_rect, clock, camera_rect = setup_pygame()


running = True

priscilla = spawn_creature(Entity, 'priscilla', (0, 0), speed=50)
enemies = []

db = DebugRenderer(screen)
cmd = DevCommands(priscilla, enemies, db)
dc = DevConsole()

dc.register('spawn', cmd.spawn)
dc.register('debug', cmd.toggle_debug)
dc.register('tp', cmd.teleport)
dc.register('current_pos', cmd.debug_print)
dc.register('run', cmd.run_t)

start_time = None

while running:
    running = handle_events(dc)
    dt = clock.tick(config.FPS) / 1000

    world.fill(config.BACKGROUND_COLOR)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] and start_time is None:
        start_time = pygame.time.get_ticks()

    if not dc.opened:
        dx, dy = handle_move(keys)
        priscilla.move(pygame.Vector2(dx, dy), dt, world_rect, obstacles=enemies)

        for enemy in enemies:
            obstacles = [priscilla] + [unit for unit in enemies if unit is not enemy]
            enemy.update_ai(priscilla, dt, world_rect, obstacles=obstacles, enemies=enemies)

    priscilla.draw(world)

    for enemy in enemies:
        enemy.draw(world)

    camera_rect.center = priscilla.get_rect().center
    camera_rect.clamp_ip(world_rect)

    screen.blit(world, (0, 0), camera_rect)

    db.set_camera(camera_rect)
    db.mega_draw(priscilla, *enemies, line_from=priscilla, world=True)
    dc.draw(screen)

    pygame.display.flip()

pygame.quit()
