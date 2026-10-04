import config
import pygame
from enemy import Enemy
from player import Player
from units import Units
from world_spawn import WorldSpawn
from world_rules import WorldRules
from pygame_utils import Foo, WorldTime


foo = Foo() # maybe Core be good name for this
world_time = WorldTime()
world_rules = WorldRules(world_time)
units = Units()
world_spawn = WorldSpawn(units)

screen, world, world_rect, clock, camera_rect = foo.setup_pygame()

running = True
camp = world_rules.add_camp()

world_spawn.spawn_player(Player, 'priscilla', (0, 0), max_health=10000, speed=50) # need add default

gobs = [
    world_spawn.add_record(Enemy, 'goblin_swordman', (500, 500), 'enemies', max_health=1),
    world_spawn.add_record(Enemy, 'goblin_archer', (700, 500), 'enemies', max_health=1)
]  # temporary is here, then remove

camp.add_record(*gobs)  # that also

debug, cmd, console = foo.dev_utils(units.player, units.enemies, screen=screen, world_time=world_time)

cmd.register_all(console)

while running:
    events = foo.get_events()
    running = foo.handle_events(console, events)

    dt = clock.tick(config.FPS) / 1000
    world_time.update(dt)

    world.fill(config.BACKGROUND_COLOR)

    keys = pygame.key.get_pressed()
    mouse_pos = foo.world_mouse(events, camera_rect)

    if not console.opened:
        dx, dy = foo.handle_move(keys)
        units.player.update_player(pygame.Vector2(dx, dy), dt, mouse_pos, world_rect, units.enemies)

        for enemy in units.enemies:
            obstacles = [units.player] + [unit for unit in units.enemies if unit is not enemy]
            enemy.update_ai(units.player, dt, world_rect, obstacles=obstacles, enemies=units.enemies)

    foo.units_draw(*units.get_all(), place=world)

    camera_rect.center = units.player.get_rect().center
    camera_rect.clamp_ip(world_rect)

    world_spawn.update(camera_rect)
    world_rules.update()

    screen.blit(world, (0, 0), camera_rect)

    debug.set_camera(camera_rect)
    debug.mega_draw(units.player, *units.enemies, line_from=units.player, world=True)
    debug.draw_surround_targets(units.player, units.enemies)
    console.draw(screen)

    pygame.display.flip()

pygame.quit()
