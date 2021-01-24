import random
class Game:

    line = '----------------------------------'
    # the symbols in map
    way = '.' # it called clear path
    obs = '#' # it called obs
    user = 'X'
    treasure = '$'

    # coordinates used
    user_position = {'x': 1, 'y': 4}
    treasure_position = {'x': 1, 'y': 4}
    probable_treasure_position = []
    blind_spots = [{'x': 4, 'y': 4}, {'x': 6, 'y': 4}]
    map_condition = [
        [obs, obs, obs, obs, obs, obs, obs, obs],
        [obs, way, way, way, way, way, way, obs],
        [obs, way, obs, obs, obs, way, way, obs],
        [obs, way, way, way, obs, way, obs, obs],
        [obs, way, obs, way, way, way, way, obs],
        [obs, obs, obs, obs, obs, obs, obs, obs],
    ]
    map_hint_condition = [
        [obs, obs, obs, obs, obs, obs, obs, obs],
        [obs, way, way, way, way, way, way, obs],
        [obs, way, obs, obs, obs, way, way, obs],
        [obs, way, way, way, obs, way, obs, obs],
        [obs, way, obs, way, way, way, way, obs],
        [obs, obs, obs, obs, obs, obs, obs, obs],
    ]
    
    welcome_message = '---> WELCOME TO TREASURE HUNT <---'
    menu = '''Here are the menus, just type the number for navigation:
1. Hunt now! Enter your steps!
2. Show map hint, there are 2 probable position! :p
3. Show hint coordinates
99. Exit '''
    rules = ''

    def generate_treasure_position(self):
        ''' generate new probable position or coordinates of treasure '''

        while (len(self.probable_treasure_position) < 2):
            temp = {}
            temp['x'] = random.randint(2,7)
            temp['y'] = random.randint(1,4)

            if (self.map_hint_condition[temp['y']][temp['x']] == self.way) & (temp not in self.blind_spots):
                self.map_hint_condition[temp['y']][temp['x']] = self.treasure
                self.probable_treasure_position.append(temp)
        
        self.treasure_position = self.probable_treasure_position[0]

    def show_hint_position(self):
        print(f'The probable treasure is in: {self.probable_treasure_position}')
    
    def show_user_coordinate(self):
        print(f'Now you are in coordinate {self.user_position}')

    def welcome(self):
        ''' show welcoming! '''
        print(self.welcome_message)
        self.show_map()
        self.show_user_coordinate()
        
    def show_map(self, hint = False):
        ''' show the map with symbol from coordinate '''
        map_used = self.map_hint_condition if hint else self.map_condition
        
        for key_y, val_y in enumerate(map_used):
            for key_x, val_x in enumerate(val_y):

                not_end = (key_x != (len(val_y) - 1) )
                user_in_same_coordinate = ((self.user_position['x'] == key_x) & (self.user_position['y'] == key_y))
                
                if (user_in_same_coordinate):
                    if not_end:
                        print(self.user, end='')
                    else:
                        print(self.user) 

                elif not_end:
                    print(val_x, end='')
                else:
                    print(val_x)

    def run(self):
        ''' the menus function '''
        print(self.menu)
        x = int(input('Type your choice:'))
        print(self.line)

        if (x == 99):
            print("You're exit! Thank You!")
        
        elif (x == 1):
            self.play()
        
        elif (x == 2):
            self.show_map(hint=True)
            self.run()
        
        elif (x == 3):
            self.show_hint_position()
            self.run()
    
    def play(self):
        ''' core function of the game, calculate the steps! '''
        up = int(input('Enter steps for up:'))
        right = int(input('Enter steps for right:'))
        down = int(input('Enter steps for down:'))

         
        for i in range(up):
            self.user_position['y'] = self.user_position['y'] - 1
            if self.map_condition[self.user_position['y']][self.user_position['x']] == self.obs:
                print('Sorry! Youre over up steps!')
                self.show_map()
                return
        
        for i in range(right):
            self.user_position['x'] = self.user_position['x'] + 1
            if self.map_condition[self.user_position['y']][self.user_position['x']] == self.obs:
                self.show_map()
                print('Sorry! Youre over right steps!')
                return
        
        for i in range(down):
            self.user_position['y'] = self.user_position['y'] + 1
            if self.map_condition[self.user_position['y']][self.user_position['x']] == self.obs:
                print('Sorry! Youre over down steps!')
                self.show_map()
                return
        
        self.show_map()
        if (self.user_position == self.treasure_position):
            print('Congrats YOU WIN!')
        else:
            print(f'Sorry youre lost! The treasure is in {self.treasure_position}, youre in {self.user_position}')


    def start(self):
        ''' to start the game '''
        self.generate_treasure_position()
        self.welcome()
        self.run()
