import random
import arcade
import arcade.key as keys
import operator

SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(arcade.Sprite):
    def update(self):
        self.center_x += 10


class Bot(arcade.Sprite):
    def update(self):
        self.center_x += 0.1


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, 'Математическая игра')
        self.player_list = None
        self.bot_list = None
        self.player_sprite = None
        self.bot_sprite = None
        self.input_result = ''
        self.example = ''
        arcade.set_background_color(arcade.color.ALMOND)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.bot_list = arcade.SpriteList()

        self.player_sprite = Player('sprites\car.png', SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.bot_sprite = Bot('sprites\\botcar.png', SPRITE_SCALING_PLAYER)
        self.bot_sprite.center_x = 50
        self.bot_sprite.center_y = 120
        self.bot_list.append(self.bot_sprite)
        self.example = self.generate_example()

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.bot_list.draw()
        arcade.draw_text(self.example+self.input_result, 50, 500, arcade.color.AFRICAN_VIOLET, 25, bold=True)
        #arcade.draw_text(self.example+' '+self.input_result, 400, 500, arcade.color.AFRICAN_VIOLET, 25, bold=True)

    def update(self, delta_time):
        self.bot_list.update()
        if self.input_result == '10':
            self.player_list.update()

    def on_key_press(self, key, key_modifiers):
        if key == keys.BACKSPACE:
            self.input_result = self.input_result[:-1]
        elif key == keys.RETURN:
            self.example = self.generate_example()
            self.input_result = ''
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
        operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            ':': operator.truediv
        }
        example = ''
        args = [random.randint(1, 100) for _ in range(count_args)]
        for i, arg in enumerate(args):
            '''
            if len(args) == 4:
                if i in (0, 1, 2) and '(' not in example:
                    if random.randint(0, 1):
                        example += '('
            '''


            operand = random.choice(list(operations.keys()))
            example += f'{arg} {operand} '
            '''
            if len(args) == 4:

                if i in (1, 2) and '(' in example and ')' not in example:
                    if random.randint(0, 1):
                        example = example[:-2]+' )'+example[-2]
                elif i == 3 and '(' in example and ')' not in example:
                    example = example[:-3]+') '+example[-2]
            '''
        
        example = example[:-2]
        example += '= '
        
        return example
        
        


    def calc_result(self):
        pass
        
def main():
    window = MyGame()
    window.set_update_rate(1/80)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()