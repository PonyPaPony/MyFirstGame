import random
import pygame
from data.units import UNITS
from spawner import spawn_creature
from Enemy import Enemy

class DevConsole:
    def __init__(self):
        self.commands = {}

        self.opened = False
        self.input = ''

        self.font = pygame.font.Font(None, 28)

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

    def register(self, name, function):
        self.commands[name] = function

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
    def __init__(self, player, enemies, debug_render):
        self.player = player
        self.enemies = enemies
        self.debug = debug_render

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

    def toggle_debug(self):
        self.debug.enabled = not  self.debug.enabled

    def teleport(self, x, y):
        x, y = int(x), int(y)
        self.player.pos.update(x, y)

    def print_current_coordinates(self, trigger_phrase):
        for enemy in self.enemies:
            commands = {
                'player': f"Player: {self.player.pos}",
                'sur': f"Enemy surround point: {enemy.surround_slot}",
                'enemy': f"Enemy: {enemy.pos}"
            }

            print(commands.get(trigger_phrase))

    def get_real_name(self, name):
        names = {
            'sword': 'goblin_swordman',
            'archer': 'goblin_archer',
        }
        return names.get(name, name)

    def debug_print(self, target='player'):
        self.print_current_coordinates(target)

    def run_t(self, number=1, name='goblin_swordman'):
        real_name = self.get_real_name(name)
        self.teleport(500, 500)
        self.debug_print('player')
        self.spawn(real_name , number)
        self.teleport(800, 800)
        self.debug_print('enemy')