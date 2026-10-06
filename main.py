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
interact = False
camp = world_rules.add_camp()

world_spawn.spawn_player(Player, 'priscilla', (773, 260), max_health=10000, speed=50) # need add default


img, pos = world_spawn.load_location('start_city') # temporary is here, then remove
objects = world_spawn.get_objects('start_city')

debug, cmd, console = foo.dev_utils(units.player, units.enemies, screen=screen, world_time=world_time)

cmd.register_all(console)

while running:
    events = foo.get_events()
    running, interact = foo.handle_events(console, events)

    dt = clock.tick(config.FPS) / 1000
    world_time.update(dt)

    world.fill(config.BACKGROUND_COLOR)
    world.blit(img, pos)

    keys = pygame.key.get_pressed()
    mouse_pos = foo.world_mouse(events, camera_rect)
    if mouse_pos is not None:
        print((round(mouse_pos.x), round(mouse_pos.y)),',')

    if not console.opened:
        player_obstacles = units.enemies + objects
        dx, dy = foo.handle_move(keys)
        units.player.update_player(
            pygame.Vector2(dx, dy),
            dt,
            mouse_pos,
            world_rect,
            units.enemies,
            player_obstacles
        )

        if interact and units.player.interaction_target:
            print("INTERACT WITH:", units.player.interaction_target.name)

        for enemy in units.enemies:
            obstacles = [units.player] + [
                unit for unit in units.enemies if unit is not enemy] + objects
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
    debug.draw_buildings(objects)
    debug.draw_buildings(objects, color='green', arg='threshold')
    console.draw(screen)

    pygame.display.flip()

pygame.quit()
