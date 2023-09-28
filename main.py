import random
from enum import Enum
from typing import Optional
import arcade
import arcade.key as keys

SPRITE_SCALING_PLAYER = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PLAYER_MOVEMENT_SPEED = 3
BOT_MOVEMENT_SPEED = 5
ACCELERATION = 30
DECELERATION = 20

DISTANCE_TO_CHANGE_TEXTURE = 0.5


class GameState(Enum):
    MENU = 1
    GAME = 2
    END = 3


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


class Shadow(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.scale = SPRITE_SCALING_PLAYER
        self.shadow_texture = (arcade.load_texture('sprites/shadow.png'))
        self.texture = self.shadow_texture
        self.alpha = 180
        self.hit_box = self.texture.hit_box_points


class Bordur(arcade.Sprite):
    def update(self):
        self.center_x -= 5
        if self.center_x < -25:
            self.center_x = SCREEN_WIDTH + 25


class Line(arcade.Sprite):
    def update(self):
        self.center_x -= 5
        if self.center_x < -100:
            self.center_x = SCREEN_WIDTH + 100


class Finish(arcade.Sprite):
    def update(self):
        self.center_x -= 5
        if self.center_x < -100:
            self.center_x = SCREEN_WIDTH + 100


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
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.physics_engine = Optional[arcade.PymunkPhysicsEngine]
        self.bordur_sprite = None
        self.bordur_list = None
        self.line_sprite = None
        self.line_list = None
        self.finish_sprite = None
        self.finish_list = None
        self.coeff_deceleration = 0
        self.timer = None
        self.total_time = None
        self.mount = None
        self.mount_x = None
        self.mount_list = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bot_list = arcade.SpriteList()
        self.bordur_list = arcade.SpriteList()
        self.line_list = arcade.SpriteList()
        self.finish_list = arcade.SpriteList()

        self.mount_far_1 = arcade.create_polygon(
            [
                (-400, 200),
                (200, 450),
                (600, 200),
            ],
            (214, 170, 126)
        )
        self.mount_far_2 = arcade.create_polygon(
            [
                (0, 200),
                (450, 550),
                (800, 200),
            ],
            (214, 170, 126)
        )
        self.mount_far_3 = arcade.create_polygon(
            [
                (400, 200),
                (650, 600),
                (1000, 200),
            ],
            (214, 170, 126)
        )
        self.mount_far_4 = arcade.create_polygon(
            [
                (600, 200),
                (900, 500),
                (1200, 200),
            ],
            (214, 170, 126)
        )
        self.mount_far_list = arcade.ShapeElementList()
        self.mount_far_list.append(self.mount_far_1)
        self.mount_far_list.append(self.mount_far_2)
        self.mount_far_list.append(self.mount_far_3)
        self.mount_far_list.append(self.mount_far_4)

     
        self.mount_1 = arcade.create_polygon(
            [
                (-400, 100),
                (200, 350),
                (600, 100),
            ],
            arcade.color.ALMOND
        )
        self.mount_2 = arcade.create_polygon(
            [
                (0, 100),
                (600, 450),
                (1000, 100),
            ],
            arcade.color.ALMOND
        )
        self.mount_3 = arcade.create_polygon(
            [
                (600, 100),
                (800, 400),
                (1200, 100),
            ],
            arcade.color.ALMOND
        )
        self.mount_4 = arcade.create_polygon(
            [
                (800, 100),
                (1200, 250),
                (1600, 100),
            ],
            arcade.color.ALMOND
        )
        self.mount_list = arcade.ShapeElementList()
        self.mount_list.append(self.mount_1)
        self.mount_list.append(self.mount_2)
        self.mount_list.append(self.mount_3)
        self.mount_list.append(self.mount_4)
        
        self.timer = ''
        self.total_time = 0.0
        self.player_sprite = Player()
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 70
        self.player_shadow = Shadow()
        self.player_shadow.center_x = 50
        self.player_shadow.center_y = 32
        self.player_list.append(self.player_shadow)
        self.player_list.append(self.player_sprite)
        self.example = ''
        self.result_message = 'Нажмите пробел для запуска'
        self.result_color = arcade.color.GO_GREEN
        self.bot_sprite = Bot()
        self.bot_sprite.center_x = 50
        self.bot_sprite.center_y = 160
        self.bot_shadow = Shadow()
        self.bot_shadow.center_x = 50
        self.bot_shadow.center_y = 122
        self.player_list.append(self.bot_shadow)
        self.bot_list.append(self.bot_sprite)
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

        for i in range(8):
            finish = Finish('sprites/finish.png', 0.25)
            finish.center_x = 825
            finish.center_y = i*25
            self.finish_list.append(finish)

    def on_draw(self):
        arcade.start_render()
        self.mount_far_list.draw()
        self.mount_list.draw()
        arcade.draw_rectangle_filled(400, 100, 800, 200, arcade.color.DIM_GRAY)
        self.bordur_list.draw()
        self.line_list.draw()
        self.finish_list.draw()
        self.player_list.draw()
        self.bot_list.draw()

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
        arcade.draw_text(
            self.timer,
            600,
            500,
            arcade.color.GO_GREEN,
            25,
            bold=True
        )

    def on_update(self, delta_time):
        self.physics_engine.step()

        self.player_shadow.center_x = self.player_sprite.center_x
        self.bot_shadow.center_x = self.bot_sprite.center_x

        if self.game_state == GameState.GAME:

            self.mount_list.center_x -= 0.1
            self.mount_far_list.center_x -= 0.05
            self.total_time += delta_time
            minutes = int(self.total_time) // 60
            seconds = int(self.total_time) % 60
            seconds_100s = int((self.total_time - seconds) * 100)
            self.timer = f'{minutes:02d}:{seconds:02d}:{seconds_100s:02d}'

            self.bordur_list.update()
            self.line_list.update()

            if (self.player_sprite.center_x >= 650
               or self.bot_sprite.center_x >= 650):
                self.finish_list.update()

            player_physics_object = self.physics_engine.get_physics_object(
                self.player_sprite
            )
            bot_physics_object = self.physics_engine.get_physics_object(
                self.bot_sprite
            )
            if player_physics_object.body.velocity[0] > PLAYER_MOVEMENT_SPEED:
                self.physics_engine.apply_force(
                    self.player_sprite,
                    (-(DECELERATION - self.coeff_deceleration), 0)
                )
            if bot_physics_object.body.velocity[0] > BOT_MOVEMENT_SPEED:
                self.physics_engine.apply_force(
                    self.bot_sprite,
                    (-DECELERATION, 0)
                )

            if self.player_sprite.center_x >= self.finish_list.sprite_list[0].center_x:
                self.game_state = GameState.END
                self.result_message = 'Вы победили! Нажмите Esc'
                self.result_color = arcade.color.GO_GREEN

            if self.bot_sprite.center_x >= self.finish_list.sprite_list[0].center_x:
                self.result_message = 'Вы проиграли! Нажмите Esc'
                self.result_color = arcade.color.RED
                self.game_state = GameState.END

        if self.game_state == GameState.END:
            player_physics_object = self.physics_engine.get_physics_object(
                self.player_sprite
            )
            bot_physics_object = self.physics_engine.get_physics_object(
                self.bot_sprite
            )
            if player_physics_object.body.velocity[0] > 0:
                self.physics_engine.apply_force(
                    self.player_sprite,
                    (-5, 0)
                )
            if bot_physics_object.body.velocity[0] > 0:
                self.physics_engine.apply_force(
                    self.bot_sprite,
                    (-5, 0)
                )

    def on_key_press(self, key, key_modifiers):
        if self.game_state == GameState.MENU:
            if key == keys.SPACE:
                self.result_message = ''
                self.example = self.generate_example()
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
                    self.coeff_deceleration = (
                        len(
                            self.example
                            .replace('+', '')
                            .replace('*', '')
                            .replace(':', '')
                            .replace('-', '')
                            .replace('=', '')
                            .split()
                        )
                    )
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
        #if self.game_state == GameState.END:
        if key == keys.ESCAPE:
            self.game_state = GameState.MENU
            self.setup()


    def generate_example_list(self, exemple_list, size):
        print(exemple_list)
        operations = (
            '+',
            '-',
            '*',
            '/',
        )
        operator = random.choice(operations)
        if not exemple_list:

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
                    b = random.randint(1, 15)
                else:
                    b = random.randint(1, 20)
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

            exemple_list = [str(a), operator, str(b)]
        else:
            if operator == '+':
                a = eval(''.join(exemple_list))
                if a > 50:
                    b = random.randint(1, 50)
                elif a > 25 and a <= 50:
                    b = random.randint(1, 25)
                elif a > 10 and a <= 25:
                    b = random.randint(1, 10)
                else:
                    b = random.randint(1, 100)
                exemple_list += [operator, str(b)]
            elif operator == '-':
                a = eval(''.join(exemple_list))
                b = random.randint(0, a)
                if b:
                    exemple_list += [operator, str(b)]
            elif operator == '*':
                if exemple_list[-2] != '*':
                    if exemple_list[-2] == '-':
                        print(exemple_list[:-2])
                        a = eval(''.join(exemple_list[:-2]))
                        c = int(a / int(exemple_list[-1]))
                        b = random.randint(0, c)
                        if b:
                            exemple_list += [operator, str(b)]
                    else:
                        a = int(exemple_list[-1])
                        if a > 50:
                            b = random.randint(1, 5)
                        elif a > 25 and a <= 50:
                            b = random.randint(1, 10)
                        elif a > 10 and a <= 25:
                            b = random.randint(1, 15)
                        else:
                            b = random.randint(1, 20)
                        exemple_list += [operator, str(b)]
            elif operator == '/':
                if exemple_list[-2] not in '/*':
                    a = int(exemple_list[-1])
                    b = random.randint(2, 10)
                    c = a * b
                    a = c
                    if a < 100:
                        exemple_list[-1] = str(a)
                        exemple_list += [operator, str(b)]


        
        size += -1
        if size > 0:
            return self.generate_example_list(exemple_list, size)
        else:
            return exemple_list


    def generate_example(self):
        count_oper = random.randint(1, 3)

        example = ''
        example_list = []

        example_list = self.generate_example_list(example_list, count_oper)

        example = ' '.join(example_list)
      
        example += ' = '

        return example.replace('/',':')

    def calc_example(self, example: str,):
        print('exm', example)
        temp = example.replace(':', '/').replace(' ', '').replace('=', '')
        result = eval(temp)
        print('res', result)
        return result


def main():
    window = MyGame()
    window.set_update_rate(1/80)
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
