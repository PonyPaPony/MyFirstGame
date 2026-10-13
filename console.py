import pygame
import config
import random
from enemy import Enemy
from data.entity_templates import UNITS
from data.locations_templates import BUILDINGS

class Console:
    def __init__(self):
        self.commands = {}
        self.opened = False
        self.input = ""

        self.font = pygame.font.Font(None, 28)


    @staticmethod
    def command(name):
        def decorator(func):
            func.command_name = name
            return func
        return decorator

    def console_draw(self, screen):
        if not self.opened:
            return

        pygame.draw.rect(screen, (20, 20, 20), (0, 0, screen.get_width(), 60))
        text = self.font.render("> " + self.input, True, 'white')
        screen.blit(text, (10, 15))

    def handle_event(self, event):
        match event.key:
            case pygame.K_RETURN:
                self.execute(self.input)
                self.input = ""

            case pygame.K_BACKSPACE:
                self.input = self.input[:-1]

            case _:
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
            print("Error executing command:", e)

    def toggle(self):
        self.opened = not self.opened

class ConsoleCommands:
    def __init__(self, debug):
        self.units = None
        self.world_time = None
        self.debug = debug
        self.spawner = None


    def register_commands(self, console):
        for name in dir(self):
            method = getattr(self, name)

            command_name = getattr(
                method, 'command_name', None
            )

            if command_name is not None:
                console.commands[command_name] = method

    def print_current_position(self, trigger_phrase):
        if trigger_phrase == 'player':
            print(f"Player position: {self.units.player.position}")
            return

        if not self.units.enemies:
            print("Enemies not found")
            return

        for i, enemy in enumerate(self.units.enemies):
            commands = {
                'sur': f"Slot [{i}]: {enemy.surround_slot}",
                'enemy': F"Enemy [{i}]: {enemy.position}"
            }

            result = commands.get(trigger_phrase)

            if result is not None:
                print(result)

    @staticmethod
    def get_real_name(name):
        return config.NAMES.get(name, name)

    @staticmethod
    def get_stat(stat):
        stats = {
            'hp': 'current_health',
            'att': 'attack',
            'def': 'defence',
            'dodge': 'dodge'
        }
        return stats.get(stat, stat)

    @staticmethod
    def get_position(target):
        targets = {
            'smith': BUILDINGS['undershift_blacksmith']['threshold']['player_pos']['exit']
        }
        return targets.get(target)

    #! NOTE: dev commands

    @Console.command("debug")
    def toggle_debug(self, *flags):
        options = {
            '-f': 'enabled',
            '-s': 'show_polygon',
            '-g': 'show_surround',
            '-p': 'polygon_editor'
        }

        if not flags:
            flags = ('-f',)

        if '-all' in flags:
            flags = tuple(flag for flag in options if flag not in flags)

        for flag in flags:
            attr = options.get(flag)

            if attr is None:
                print(f"Unknown debug flag: {flag}")
                continue

            setattr(self.debug, attr, not getattr(self.debug, attr))


    @Console.command("polygon")
    def toggle_polygon_editor(self):
        if self.debug.enabled:
            self.debug.polygon_editor = not self.debug.polygon_editor
            return
        print("polygon editor can be toggled when debug is enabled")

    @Console.command("show")
    def toggle_show(self):
        if self.debug.enabled:
            self.debug.show_polygon = not self.debug.show_polygon
        else:
            print("show can be toggled when debug is enabled")

    @Console.command("grop_up")
    def toggle_points(self):
        if self.debug.enabled:
            self.debug.show_surround = not self.debug.show_surround
        else:
            print("points can be toggled when debug is enabled")

    @Console.command("spawn")
    def spawn(self, name, count=1):
        if name == 'Priscilla' or name == 'Player':
            print("Cannot spawn player as enemy")
            return

        real_name = self.get_real_name(name)

        if real_name not in UNITS:
            print(f"Unknown unit: {name}")
            return

        try:
            count = int(count)
        except ValueError:
            print(f"Invalid count: {count}")
            return

        if not 1 <= count <= 100:
            print('Count must be between 1 and 100')
            return

        for _ in range(count):
            new_x = random.randint(
                int(self.units.player.position.x - 100),
                int(self.units.player.position.x + 100)
            )
            new_y = random.randint(
                int(self.units.player.position.y - 100),
                int(self.units.player.position.y + 100)
            )

            self.spawner.add_record(Enemy, real_name, (new_x, new_y), 'enemies')

    @Console.command('pos')
    def debug_print(self, target='player'):
        self.print_current_position(target)

    @Console.command("tp")
    def teleport(self, target=None, x=None):
        if target is None:
            raise TypeError("Укажи цель или координаты")

        if x is not None:
            self.units.player.position.update(int(target), int(x))
            return

        position = self.get_position(target)

        if position is None:
            raise ValueError(f"Unknown teleport target: {target}")

        self.units.player.position.update(position)

    @Console.command('killall')
    def  killall(self):
        self.units.enemies.clear()

    @Console.command('ai')
    def ai(self):
        for i, enemy in enumerate(self.units.enemies):
            print(
                f"{i}: {enemy.unit_type}"
                f"state={enemy.state}"
                f"slot={enemy.surround_slot}"
            )

    @Console.command("set")
    def set_stat(self, target, stat, num):
        num = max(0, int(num))
        if target == 'player':
            self.units.player.stats[self.get_stat(stat)] = num
            return
        for enemy in self.units.enemies:
            enemy.stats[self.get_stat(stat)] = num

    @Console.command('time')
    def game_time(self, set_time=None):
        if set_time is None:
            print(
                'day', self.world_time.get_day(),
                "hour", self.world_time.get_hour(),
                "minute", self.world_time.get_minute()
            )
        else:
            self.world_time.set_time(set_time)
            print(
                'day', self.world_time.get_day(),
                "hour", self.world_time.get_hour(),
                "minute", self.world_time.get_minute()
            )

    @Console.command("run")
    def run(self):
        self.teleport('smith')
        self.toggle_debug('-f', '-s')