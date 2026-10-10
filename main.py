import config
import pygame
from units import Units
from core import Core
from world_spawn import WorldSpawn
from world_rules import WorldRules
from pygame_utils import Foo, WorldTime


foo = Foo() # maybe Core be good name for this
core = Core()
world_time = WorldTime()
world_rules = WorldRules(world_time)
units = Units()
world_spawn = WorldSpawn(units)

screen, world, clock, camera_rect = foo.setup_pygame("Border")

core.init_units(world_spawn)
core.register_units(units)
camp = core.connect(world_rules)
img, pos, objects = core.update(world_spawn)
world_rect = foo.current_rect(img, pos)
debug, cmd, console = foo.dev_utils(units.player, units.enemies, screen=screen, world_time=world_time)
cmd.register_all(console)

running = True
interact = False

collisions = []

while running:
    events = foo.get_events()
    running, interact = foo.handle_events(console, events)

    dt = clock.tick(config.FPS) / 1000
    world_time.update(dt)

    world.fill(config.BACKGROUND_COLOR)
    world.blit(img, pos)

    keys = pygame.key.get_pressed()
    mouse_pos = foo.world_mouse(events)
    if mouse_pos is not None:
        collisions.append((round(mouse_pos.x), round(mouse_pos.y)))

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

        if interact and (
                units.player.interaction_target
                or units.player.can_exit_building(*core.exit_from())
        ):
            img, pos, objects = core.update(world_spawn)
            world_rect = foo.current_rect(img, pos)

        for enemy in units.enemies:
            obstacles = [units.player] + [
                unit for unit in units.enemies if unit is not enemy] + objects
            enemy.update_ai(units.player, dt, world_rect, obstacles=obstacles, enemies=units.enemies)

    foo.units_draw(*units.get_all(), place=world)

    camera_rect.center = units.player.get_rect().center
    camera_rect.clamp_ip(world_rect)

    world_spawn.update(camera_rect)
    world_rules.update()

    render_camera, scale, render_offset, render_size = foo.render(screen, world, camera_rect, world_rect)

    debug.set_camera(render_camera, scale, render_offset, render_size)
    debug.mega_draw(units.player, *units.enemies, line_from=units.player, world=True)
    debug.draw_surround_targets(units.player, units.enemies)
    debug.draw_buildings(objects)
    debug.draw_buildings(objects, color='green', arg='threshold')
    console.draw(screen)

    pygame.display.flip()

pygame.quit()

if not running:
    print(collisions)