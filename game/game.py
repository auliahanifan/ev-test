class Game:

    moves = {
            'up': 'a', 
            'down': 'b',
            'right': 'c'
            }

    user_position = {'x': 1, 'y': 4}
    treasure_position = {'x': 1, 'y': 4}

    way = '.' # it called clear path
    obs = '#' # it called obs
    user = 'X'

    map_condition = [
        [obs, obs, obs, obs, obs, obs, obs, obs],
        [obs, way, way, way, way, way, way, obs],
        [obs, way, obs, obs, obs, way, way, obs],
        [obs, way, way, way, obs, way, obs, obs],
        [obs, way, obs, way, way, way, way, obs],
        [obs, obs, obs, obs, obs, obs, obs, obs],
        ]
    
    welcome_message = "---> WELCOME TO TREASURE HUNT <---"

    def welcome(self):
        print(self.welcome_message)
        
    def show_map(self):
        for key_y, val_y in enumerate(self.map_condition):
            for key_x, val_x in enumerate(val_y):

                not_end = (key_x != (len(val_y) - 1) )
                user_in_same_coordinate = ((self.user_position['x'] == key_x) & (self.user_position['y'] == key_y))
               
                if (user_in_same_coordinate):
                    if not_end:
                        print(self.user, end='')
                    else:
                        print(self.user) 

                elif not_end:
                    print(val_x, end="")
                else:
                    print(val_x)

    def start(self):
        self.welcome()
        self.show_map()
