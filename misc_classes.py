import os
from settings import *


class Button(object):
    def __init__(self, pos, text, font, colour, image, highlight_colour=None):   #default highlight colour is green
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.font = font
        self.colour = colour
        self.text = text
        self.highlighted = False
        self.highlight_colour = highlight_colour

        if self.text != None and self.image == None:
            self.text = self.font.render(self.text, True, self.colour)
            self.text_rect = self.text.get_rect(center=(self.x,self.y))
            self.rect = self.text_rect

        else:
            self.rect = self.image.get_rect(center=(self.x, self.y))

        self.width = self.rect.right - self.rect.left
        self.height = self.rect.top - self.rect.bottom

    def draw(self, window):
        if self.image != None:
            window.blit(self.image, self.rect)
        window.blit(self.text, self.text_rect)

        if self.highlight_colour is None:
            self.highlight_colour = GREEN

        if self.highlighted:
            pygame.draw.line(window, self.highlight_colour, (self.rect.centerx - (self.width // 2), self.rect.centery - (self.height // 2)), (self.rect.centerx + (self.width // 2), self.rect.centery - (self.height // 2)))

    def is_hovering(self, position):  #takes position of mouse from pygame.mouse.get_pos() method.
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range (self.rect.top, self.rect.bottom): #if the x position of the mouse within the horizontal boundaries of the button and the y position of the mouse within the vertical boundaries of the button and the mouse is pressed, return True as mouse currently on the button
            return True
        return False




class Pellet(object):
    def __init__(self, node):
        self.node = node
        self.colour = WHITE
        self.radius = 2
        self.pos = self.node.pos

    def draw(self, window):
        position = (self.pos.x + 8, self.pos.y + 8)
        pygame.draw.circle(window, self.colour, position, self.radius)




class Power_Pellet(Pellet):
    def __init__(self, node):
        super().__init__(node)
        self.node = node
        self.colour = WHITE
        self.radius = 6
        self.pos = self.node.pos




class Timer(object):
    def __init__(self):
        self.start_time = None
        self.nearly_up = False

    def update(self, current_time):
        if self.start_time == None:
            self.start_time = current_time

    def reset(self):
        self.start_time = None
        self.time_passed = None
        self.nearly_up = False

    def is_up(self, current_time, delay):   #SHOULD RETURN TRUE IF X TIME (in terms of ms) HAS PASSED AND FALSE OTHERWISE
        self.update(current_time)
        dt = current_time - self.start_time   #RETURNS THE TIME PASSED IN MS OR S DEPENDENT ON THE CURRENT_TIME PASSED INTO THE METHOD.

        if dt >= delay:
            self.reset()
            return True

        elif delay - dt <= 2:
            self.nearly_up = True

        return False




class Database(object):
    def __init__(self):
        self.file = 'users.txt'
        self.usernames = []
        self.passwords = []
        self.modes = []
        self.levels = []
        self.high_scores = []
        self.open()
        self.current_user = None
        self.current_index = None

    def is_empty(self):
        size = os.stat(self.file).st_size
        if size == 0:
            return True
        return False

    def reset(self):
        self.usernames = []
        self.passwords = []
        self.modes = []
        self.levels = []
        self.high_scores = []


    def read(self):
        with open(self.file, 'r') as f:
            print(list(line.split(',') for line in f))


    def open(self):
        if not self.is_empty():
            with open(self.file, mode='r') as f:
                users = list(line.split(',') for line in f)


            for user in users:
                if len(user) == 5:
                    self.usernames.append(user[0])
                    self.passwords.append(user[1])
                    self.modes.append(user[2])
                    if user[3][1:2] == '\n':
                        self.levels.append(user[3][0])   #appends a high score in the event the level is <10
                    else:
                        self.levels.append(user[3][0:1])   #scenario if level is =10

                    self.high_scores.append(user[4])

                else:
                    continue



    def register(self, username, password, confirm_password):
        if username in self.usernames:
            return "Username already exists."


        elif len(username) > 12:
            return "Username too long."


        else:
            if len(password) < 8:
                return "Password too short."


            elif password != confirm_password:
                return "Passwords do not match."


            else:
                self.usernames.append(username)
                self.passwords.append(password)
                self.modes.append('1')  #where 1=normal 2=advanced 3=special
                self.levels.append('0')
                self.high_scores.append('0')


        self.update_file()
        return "worked"


    def get_data(self, mode=None):
        data = [list(i) for i in list(zip(self.usernames, self.passwords, self.modes, self.levels, self.high_scores))]

        if mode is None:
            return data

        else:
            new_data = []
            if mode == "advanced":
                for i, user in enumerate(data):
                    if int(user[2]) == 2:
                        new_data.append(user)

                return new_data

            else:
                for i, user in enumerate(data):
                    if int(user[2]) == 1:
                        new_data.append(user)

                return new_data






    def update_file(self, logged_in=False):
        data = self.get_data()
        if logged_in == True:
            data[self.current_index] = self.current_user


        with open(self.file, mode='w') as f:
            for user in data:
                f.write(user[0] + ',' + user[1] + ',' + user[2] + ',' + user[3] + ',' + user[4] +'\n')



    def login(self, username, password):
        data = self.get_data()
        for i, user in enumerate(data):
            if username == user[0]:
                if password == user[1]:
                    self.current_index = i
                    self.current_user = user
                    return "worked"

                else:
                    return "Incorrect password."

            else:
                continue

        return "Username does not exist."



    def logout(self):
        self.current_user, self.current_index = None, None



    def get_rank_score(self, level, score):
        max_points = 4000   #ON SIMULATING, MAX_POINTS = 3180, BUT EDGE CASES HAVE EXCEEDED THIS VALUE SO THE SAFETY NET = 4000, NO EXTRA COST.
        if not level == 0:
            return ((level - 1) * max_points) + score

        else:
            return score


    def sort(self, data):
        ranks = [[user[0], user[3], user[4], self.get_rank_score(int(user[3]), int(user[4]))] for user in data]
        return merge_sort(ranks)[::-1]




    def get_leaderboard_data(self, mode):    #SEPERATE LEADERBOARDS FOR NORMAL, ADVANCED AND SPECIAL MODE.  CREATE A GRAPHICAL LEADERBOARD NEXT
        data = self.sort(self.get_data(mode))
        for user in data:
            for i, char in enumerate(user[2]):
                if char == "\n":
                    user[2] = user[2][:i]

        return data


    def update_mode(self, mode):
        if int(self.current_user[2]) < mode:
            self.current_user[2] = str(mode)

        self.update_file(logged_in=True)

    def update_level(self, level):
        if int(self.current_user[3]) < level:
            self.current_user[3] = str(level)

        self.update_file(logged_in=True)


    def update_score(self, score):
        if int(self.current_user[4]) < score:
            self.current_user[4] = str(score)

        self.update_file(logged_in=True)





def merge_sort(arr):
    i, j, k = 0, 0, 0
    if len(arr) > 1:
        midpoint = len(arr) // 2
        left_half = arr[midpoint:]
        right_half = arr[:midpoint]

        merge_sort(left_half)    #recurses to subdivide the two halves into atomic elements.
        merge_sort(right_half)

        while i < len(left_half) and j < len(right_half):   #below merges up the halves into a combined sorted array.
            if left_half[i][3] <= right_half[j][3]:  #only compares the weighted score for each user
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1


        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr









