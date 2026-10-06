import random
import pygame
import config
from data.unit_templates import UNITS
from spawner import spawn_creature
from enemy import Enemy

class DevConsole:
    def __init__(self):
        self.commands = {}

        self.opened = False
        self.input = ''

        self.font = pygame.font.Font(None, 28)

    @staticmethod
    def command(name):
        def decorator(func):
            func.command_name = name
            return func

        return decorator

    def draw(self, screen):
        if not self.opened:
            return

        pygame.draw.rect(
            screen,
            (20, 20, 20),
            (0, 0, screen.get_width(), 60)
        )

        text = self.font.render(
            '> ' + self.input,
            True,
            'white'
        )

        screen.blit(text, (10, 15))

    def handle_event(self, event):
        if event.key == pygame.K_RETURN:
            self.execute(self.input)
            self.input = ''

        elif event.key == pygame.K_BACKSPACE:
            self.input = self.input[:-1]

        else:
            self.input += event.unicode

    def execute(self, text):
        parts = text.split()

        if not parts:
            return

        name, *args = parts
        command = self.commands.get(name)

        if command is None:
            print("Unknown command:", name)
            return

        try:
            command(*args)
        except (TypeError, ValueError) as e:
            print(f'Error executing command: {e}')

    def toggle(self):
        self.opened = not self.opened

class DevCommands:
    def __init__(self, player, enemies, npc=None, world_time=None, debug_render=None):
        self.player = player
        self.enemies = enemies
        self.npc = npc
        self.world_time = world_time
        self.debug = debug_render

    def register_all(self, console):
        for name in dir(self):
            method = getattr(self, name)

            command_name = getattr(
                method, 'command_name', None
            )

            if command_name is not None:
                console.commands[command_name] = method

    def print_current_coordinates(self, trigger_phrase):
        if trigger_phrase == 'player':
            print(f"Player: {self.player.pos}")
            return

        if not self.enemies:
            print("No enemies")
            return

        for i, enemy in enumerate(self.enemies):
            commands = {
                'sur': f"Slot [{i}]: {enemy.surround_slot}",
                'enemy': f"Enemy [{i}]: {enemy.pos}"
            }

            result = commands.get(trigger_phrase)

            if result is not None:
                print(result)

    def get_real_name(self, name):
        names = {
            'sword': 'goblin_swordman',
            'archer': 'goblin_archer',
        }
        return names.get(name, name)

    @DevConsole.command('targets')
    def toggle_targets(self):
        self.debug.show_targets = (
            not self.debug.show_targets
        )

    @DevConsole.command('to_enemy')
    def toggle_to_enemy(self):
        self.debug.to_enemy = (
            not self.debug.to_enemy
        )

    @DevConsole.command('spawn')
    def spawn(self, name, count=1):
        if name == 'priscilla':
            print('Cannot spawn player as enemy')
            return

        real_name = self.get_real_name(name)

        if real_name not in UNITS:
            print(f'Unknown creature: {name}')
            return

        try:
            count = int(count)
        except ValueError:
            print(f'Invalid count: {count}')
            return

        if not 1 <= count <= 100:
            print('Count must be between 1 and 100')
            return

        for _ in range(count):
            new_x = random.randint(
                int(self.player.pos.x - 100),
                int(self.player.pos.x + 100)
            )
            new_y = random.randint(
                int(self.player.pos.y - 100),
                int(self.player.pos.y + 100)
            )

            enemy = spawn_creature(
                Enemy,
                real_name,
                (new_x, new_y)
            )

            self.enemies.append(enemy)

    @DevConsole.command('debug')
    def toggle_debug(self):
        self.debug.enabled = not  self.debug.enabled

    @DevConsole.command('tp')
    def teleport(self, x, y):
        x, y = int(x), int(y)
        self.player.pos.update(x, y)

    @DevConsole.command('pos')
    def debug_print(self, target='player'):
        self.print_current_coordinates(target)

    @DevConsole.command('killall')
    def killall(self):
        self.enemies.clear()
        print("All enemies removed")

    @DevConsole.command('ai')
    def ai(self):
        for i, enemy in enumerate(self.enemies):
            print(
                f"{i}: {enemy.unit_type} "
                f"state={enemy.state} "
                f"slot={enemy.surround_slot}"
            )

    @DevConsole.command('slots')
    def slots(self):
        for unit_type, count in config.SLOTS.items():
            occupied = {
                enemy.surround_slot
                for enemy in self.enemies
                if enemy.unit_type == unit_type
                   and enemy.surround_slot is not None
            }

            free = set(range(count)) - occupied

            print(
                f"{unit_type}: "
                f"occupied={sorted(occupied)}, "
                f"free={sorted(free)}"
            )

    @DevConsole.command('run')
    def run_t(self, number=1, name='sword'):
        self.teleport(500, 500)
        self.debug_print('player')
        self.spawn(name, number)
        self.teleport(800, 800)
        self.debug_print('enemy')

    @DevConsole.command('set_hp')
    def set_hp(self, target, num):
        num = max(0, int(num))
        if target == 'player':
            self.player.stats['current_health'] = num
        else:
            for enemy in self.enemies:
                enemy.stats['current_health'] = num

    @DevConsole.command("status")
    def status(self):
        print(f"Player HP: {self.player.stats['current_health']}")
        for enemy in self.enemies:
            print(f"Enemy HP: {enemy.stats['current_health']}")

    @DevConsole.command("time")
    def time(self, set_time=False):
        if not set_time:
            print(
                "day", self.world_time.get_day(),
                "hour", self.world_time.get_hour(),
                "minute", self.world_time.get_minute()
            )
        else:
            self.world_time.set_time(int(set_time))
            print(
                "day", self.world_time.get_day(),
                "hour", self.world_time.get_hour(),
                "minute", self.world_time.get_minute()
            )

    @DevConsole.command('quit')
    def quit(self):
        pygame.quit()