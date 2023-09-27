import random
from enum import Enum
from typing import Optional
import arcade
import arcade.key as keys
import operator

SPRITE_SCALING_PLAYER = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_MOVEMENT_SPEED = 7
BOT_MOVEMENT_SPEED = 10
ACCELERATION = 30
DECELERATION = 20

DISTANCE_TO_CHANGE_TEXTURE = 0.5


class GameState(Enum):
    MENU = 1
    GAME = 2


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER
        self.idle_texture = (arcade.load_texture('sprites/car.png'))
        self.run_texture = []
        for i in range(1, 9):
            self.run_texture.append(arcade.load_texture(f'sprites/car{i}.png'))

        self.cur_texture = 0
        self.texture = self.idle_texture

        self.hit_box = self.texture.hit_box_points
        self.x_odometer = 0
                            
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.x_odometer += dx
        if self.x_odometer > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.run_texture[self.cur_texture]


class Bot(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER
        self.idle_texture = (arcade.load_texture('sprites/carbot.png'))
        self.run_texture = []    
        for i in range(1, 9):
            self.run_texture.append(arcade.load_texture(f'sprites/carbot{i}.png'))
        self.cur_texture = 0
        self.texture = self.idle_texture

        self.hit_box = self.texture.hit_box_points
        self.x_odometer = 0
                            
    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
        self.x_odometer += dx
        if self.x_odometer > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.run_texture[self.cur_texture]


class Bordur(arcade.Sprite):

    def update(self):
        self.center_x -= 5
        if self.center_x < -25:
            self.center_x = SCREEN_WIDTH+25


class Line(arcade.Sprite):

    def update(self):
        self.center_x -= 5
        if self.center_x < -100:
            self.center_x = SCREEN_WIDTH+100


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, 'Математическая игра')
        self.player_list = None
        self.bot_list = None
        self.player_sprite = None
        self.bot_sprite = None
        self.input_result = ''
        self.example = ''
        self.example_result = None
        self.result_color = arcade.color.RED
        self.result_message = ''
        self.game_state = GameState.MENU
        arcade.set_background_color(arcade.color.ALMOND)
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]
        self.bordur_sprite = None
        self.bordur_list = None
        self.line_sprite = None
        self.line_list = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bot_list = arcade.SpriteList()
        self.bordur_list = arcade.SpriteList()
        self.line_list = arcade.SpriteList()

        self.player_sprite = Player()
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_list.append(self.player_sprite)

        self.bot_sprite = Bot()
        self.bot_sprite.center_x = 50
        self.bot_sprite.center_y = 160
        self.bot_list.append(self.bot_sprite)
        self.example = self.generate_example()
        self.physics_engine = arcade.PymunkPhysicsEngine()
        self.physics_engine.add_sprite(
            self.player_sprite,
            max_horizontal_velocity=30
        )
        self.physics_engine.add_sprite(
            self.bot_sprite,
            max_horizontal_velocity=30
        )

        for i in range(18):
            bordur = Bordur('sprites/bordur.png', 0.5)
            bordur.center_x = i*50
            bordur.center_y = 200
            self.bordur_list.append(bordur)

        for i in range(5):
            line = Line('sprites/line.png', 0.5)
            line.center_x = i*200
            line.center_y = 100
            self.line_list.append(line)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(400, 100, 800, 200, arcade.color.DIM_GRAY)
        self.player_list.draw()
        self.bot_list.draw()
        self.bordur_list.draw()
        self.line_list.draw()
        arcade.draw_text(
            self.example+self.input_result,
            50,
            500,
            arcade.color.AFRICAN_VIOLET,
            25,
            bold=True
        )
        arcade.draw_text(
            self.result_message,
            400,
            300,
            self.result_color,
            25,
            bold=True,
            anchor_x='center'
        )

    def on_update(self, delta_time):
        self.physics_engine.step()

        if self.game_state == GameState.GAME:

            self.bordur_list.update()
            self.line_list.update()

            player_physics_object = self.physics_engine.get_physics_object(
                self.player_sprite
            )
            bot_physics_object = self.physics_engine.get_physics_object(
                self.bot_sprite
            )
            if player_physics_object.body.velocity[0] > PLAYER_MOVEMENT_SPEED:
                self.physics_engine.apply_force(
                    self.player_sprite, (-DECELERATION, 0)
                )
            if bot_physics_object.body.velocity[0] > BOT_MOVEMENT_SPEED:
                self.physics_engine.apply_force(
                    self.bot_sprite, (-DECELERATION, 0)
                )
            
            if self.player_sprite.center_x >= 700:
                self.setup()
                self.game_state = GameState.MENU

            if self.bot_sprite.center_x >= 700:
                self.setup()
                self.game_state = GameState.MENU

    def on_key_press(self, key, key_modifiers):
        if self.game_state == GameState.MENU:
            if key == keys.SPACE:
                self.game_state = GameState.GAME
                self.physics_engine.apply_impulse(
                    self.player_sprite, (PLAYER_MOVEMENT_SPEED, 0)
                )
                self.physics_engine.apply_impulse(
                    self.bot_sprite, (BOT_MOVEMENT_SPEED, 0)
                )
        if self.game_state == GameState.GAME:
            if key == keys.BACKSPACE:
                self.input_result = self.input_result[:-1]
            elif key == keys.RETURN:
                try:
                    result = float(self.input_result)
                except ValueError:
                    result = 0
                if result == self.calc_example(self.example):
                    self.physics_engine.apply_impulse(
                        self.player_sprite, (ACCELERATION, 0)
                    )
                    self.result_message = 'Правильно'
                    self.result_color = arcade.color.GO_GREEN
                else:
                    self.physics_engine.apply_impulse(
                        self.bot_sprite, (ACCELERATION, 0)
                    )
                    self.result_message = 'Не правильно'
                    self.result_color = arcade.color.RED

                self.input_result = ''
                self.example = self.generate_example()

            else:
                if key in (
                    keys.KEY_0,
                    keys.KEY_1,
                    keys.KEY_2,
                    keys.KEY_3,
                    keys.KEY_4,
                    keys.KEY_5,
                    keys.KEY_6,
                    keys.KEY_7,
                    keys.KEY_8,
                    keys.KEY_9,
                ):
                    self.input_result += chr(key)

    def generate_example(self):
        count_args = random.randint(2, 4)
        count_oper = random.randint(1, 3)
        operations = (
            '+',
            '-',
            '*',
            '/',
        )

        example = ''

        exp_list = []
        for _ in range(count_oper):
            a = 0
            b = 0
            operator = random.choice(operations)
            
            if operator == '/':
                a = random.randint(1, 25)
                b = random.randint(2, 10)
                c = a * b
                a = c
            elif operator == '*':
                a = random.randint(1, 100)
                if a > 50:
                    b = random.randint(1, 5)
                elif a > 25 and a <= 50:
                    b = random.randint(1, 10)
                elif a > 10 and a <= 25:
                    b = random.randint(1, 20)
                else:
                    b = random.randint(1, 100)
            elif operator == '-':
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                if b > a:
                    a, b = b, a
            elif operator == '+':
                a = random.randint(1, 100)
                if a > 50:
                    b = random.randint(1, 50)
                elif a > 25 and a <= 50:
                    b = random.randint(1, 25)
                elif a > 10 and a <= 25:
                    b = random.randint(1, 10)
                else:
                    b = random.randint(1, 100)

            exp_list.append(f'{a} {operator} {b}')

            example = exp_list[0]
            for i in range(1, len(exp_list)-1):
                value_1 = eval(exp_list[i-1])
                value_2 = eval(exp_list[i])
                operator = random.choice(operations)
                example += operator + exp_list[i]







        #example = ' '.join(exp_list)

        '''
        args = [random.randint(1, 100) for _ in range(count_args)]
        for i, arg in enumerate(args):
            
            if len(args) == 4:
                if i in (0, 1, 2) and '(' not in example:
                    if random.randint(0, 1):
                        example += '('
           


            operand = random.choice(list(operations.keys()))
            example += f'{arg} {operand} '
           
            if len(args) == 4:

                if i in (1, 2) and '(' in example and ')' not in example:
                    if random.randint(0, 1):
                        example = example[:-2]+' )'+example[-2]
                elif i == 3 and '(' in example and ')' not in example:
                    example = example[:-3]+') '+example[-2]
            '''

        #example = example[:-2]
        example += '= '

        return example

    def calc_example(self, example: str,):
        temp = example.replace(':', '/').replace(' ', '').replace('=', '')
        result = eval(temp)
        return result


def main():
    window = MyGame()
    window.set_update_rate(1/80)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
