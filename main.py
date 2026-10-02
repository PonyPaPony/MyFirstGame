import config
import pygame
from enemy import Enemy
from player import Player
from pygame_utils import Foo
from debug import DebugRenderer
from console import DevConsole, DevCommands
from spawner import spawn_creature
from combat import is_alive


foo = Foo()

screen, world, world_rect, clock, camera_rect = foo.setup_pygame()

running = True

priscilla = spawn_creature(Player, 'priscilla', (0, 0), max_health=10000, speed=50)
enemies = []
npc = []

db = DebugRenderer(screen)
cmd = DevCommands(priscilla, enemies, db)
dc = DevConsole()

cmd.register_all(dc)

while running:
    events = foo.get_events()
    running = foo.handle_events(dc, events)
    dt = clock.tick(config.FPS) / 1000

    world.fill(config.BACKGROUND_COLOR)

    keys = pygame.key.get_pressed()
    mouse_pos = foo.world_mouse(events, camera_rect)

    if not dc.opened:
        dx, dy = foo.handle_move(keys)
        priscilla.update_player(pygame.Vector2(dx, dy), dt, mouse_pos, world_rect, enemies)

        enemies[:] = [enemy for enemy in enemies if is_alive(enemy.stats)]

        for enemy in enemies:
            obstacles = [priscilla] + [unit for unit in enemies if unit is not enemy]
            enemy.update_ai(priscilla, dt, world_rect, obstacles=obstacles, enemies=enemies)

    priscilla.draw(world)

    for enemy in enemies:
        enemy.draw(world)

    for person in npc: # for future NPC drawing
        pass

    camera_rect.center = priscilla.get_rect().center
    camera_rect.clamp_ip(world_rect)

    screen.blit(world, (0, 0), camera_rect)

    db.set_camera(camera_rect)
    db.mega_draw(priscilla, *enemies, line_from=priscilla, world=True)
    db.draw_surround_targets(priscilla, enemies)
    dc.draw(screen)

    pygame.display.flip()

pygame.quit()
