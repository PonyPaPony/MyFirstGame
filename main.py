import pygame
import config
from game_utils import GameUtils
from core import WorldInit


game = GameUtils().setup_pygame('border') #? WHAT: Инициализируем игру и львиную долю настроек
dev = game.devs #? WHAT: Инициализируем инструментарий для отладки
world = WorldInit() #? WHAT: Инициализируем мир и львиную долю мировых параметров
dev.connect(world.units, world.world_spawn, world.world_time, world.core.current_space) #? WHAT: Передам юнитов и метод спавна в dev инструментарий

world_rect = game.current_rect(world.image, world.pos) #? WHAT: Получаем границы мира из размера фона
game.set_world_rect(world_rect) #? WHAT: Устанавливаем границы мира

running = True

while running:
    #! NOTE: подключаем события дельту времени и кнопочки
    events = game.get_events()
    running, interact = game.handle_events(events)
    dt = game.get_delta_time()

    keys = pygame.key.get_pressed()
    mouse_pos = game.mouse.world_mouse(events)

    #! NOTE: Для отладки возможность рисовать полигоны онлайн без смс и регистрации
    if dev.debug.polygon_editor and not dev.console.opened:
        for event in events:
            dev.debug.handle_event(event, mouse_pos)

    if not dev.console.opened and not dev.debug.polygon_editor:
        world.tick(dt, game.camera_rect) #? WHAT: Обновляем мир

        player_obstacles = world.units.enemies + world.units.npc + world.objects
        dx, dy = game.handle_move(keys)
        world.units.player.update_player(
            pygame.Vector2(dx, dy),
            dt,
            mouse_pos,
            world_rect,
            world.units.enemies,
            player_obstacles
        )

        if interact and (
                world.units.player.interaction_target
                or world.units.player.can_exit_from_location(*world.core.exit_from())
        ):
            #! NOTE: Переход в новую локацию
            world.world_update() #? WHAT: Обновляем информацию о мире
            world_rect = game.current_rect(world.image, world.pos) #? WHAT: Получаем границы мира из размера фона
            game.set_world_rect(world_rect) #? WHAT: устанавливаем новые границы мира

        for enemy in world.units.enemies:
            obstacles = [world.units.player] + [
                unit for unit in world.units.enemies
                if unit is not enemy
            ] + world.objects
            enemy.update_ai(world.units.player, dt, world_rect, obstacles=obstacles, enemies=world.units.enemies)

    game.world.fill(config.BACKGROUND_COLOR)
    game.world.blit(world.image, world.pos)

    game.render_units(*world.units.get_all()) #? HOW: Получаем коллекцию всех юнитов для последующей отрисовки
    game.render(world.units.player) #? WHAT: Рендерим мир по положению игрока

    dev.draw(world.objects) #? WHAT: Рисуем dev отладку
    dev.debug.polygon_editor_draw(mouse_pos) #? WHAT: Рисуем полигоны онлайн без смс и регистрации

    pygame.display.flip()

pygame.quit()