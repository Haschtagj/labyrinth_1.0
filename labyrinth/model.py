import re

from utils import playground_choice
from utils import playground_generator


class Player:
    def __init__(self, name: str='', card: str='',
                 last_score: int=0, new_score: int=0):
        self.__name = name
        self.__card = card
        self.__last_score = last_score
        self.__new_score = new_score

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def card(self):
        return self.__card

    @card.setter
    def card(self, card):
        self.__card = card

    @property
    def last_score(self):
        return self.__last_score

    @last_score.setter
    def last_score(self, last_score):
        self.__last_score = last_score

    @property
    def new_score(self):
        return self.__new_score

    @new_score.setter
    def new_score(self, new_score):
        self.__new_score = new_score

    def __repr__(self):
        return str({"name": self.name,
                    "card": self.card,
                    "last_score": self.last_score,
                    "new_score": self.new_score})


class Labyrinth:
    def __init__(self, path, playground):
        self.path = path
        self.road = playground

    def __repr__(self):
        return 'card: {}\n{}'.format(self.path, self.road)

    def get_road(self):
        return self.road


# decorator for update the position of th robot
def auto_update_robot_pos(cl):
    """Update the positions x and y"""

    instance = {}  # create a dictionary, which will contain the unique
    # object robot for a given party

    def get_instance(*args):

        if cl not in instance:
            instance[cl] = cl(*args)
        # args[1].road, args[1] is a Labyrinth object and has an attribute
        # called road which return a list of string. each string representing
        # one part of the road
        for pos, line in enumerate(args[1].road):
            if instance[cl].form in line:
                tmp = [elt for elt in line]
                instance[cl].x = tmp.index(instance[cl].form)
                instance[cl].y = pos
        return instance[cl]
    return get_instance


@auto_update_robot_pos
class Robot:
    def __init__(self, name, labyrinth: Labyrinth):
        self.labyrinth = labyrinth
        self.name = name
        self.form = 'X'
        self.y = 0
        self.x = 0
        self.bonus = 0

    def move_on_x(self, x: int, k='h'):
        """Manage the movement on x axis of the road"""

        # in a first time, we initialize one pattern which correspond
        # to the place where the robot can be moved
        # this place must begin with one or more space at the end or start
        pattern = r'(?P<ro>[\s]+[i|\.]*[{}])'.format(self.form) if k == 'h'\
            else r'(?P<ro>[{}][i|\.]*[\s]+)'.format(self.form)
        # we get the actual x position of the robot pn the road
        actual_line_pos = self.labyrinth.road[self.y]
        # we verify if on this road we have our pattern
        match = re.search(pattern, actual_line_pos)
        # if true
        if match:
            # we require it (the place where the robot can be moved)
            road_str = match.group('ro')
            # split the given line in differents parts to
            # form one ease list string for managing the no road variable
            # will contain all what not the possible place where the robot
            # can be moved
            no_road = str(actual_line_pos).split(sep=road_str)
            # create a list of all presents characters in the raod_str
            road = [elt for elt in road_str]
            # get the index of the robot
            x_ = road.index(self.form)
            # remove the robot on the list of road to replaced it according
            # to which key (h or l) the user has pressed
            self.form = road.pop(x_)
            # the new position where the robot is: is the last position
            # minus the given movement number
            # if the given number exced the lenght of the road then the robot_
            # is placed to the position 0
            new_x = (x_ - x) if x < len(road) else 0
            # insert the robot at the new given position
            road.insert(new_x, self.form)
            # rejoin the road to form a string representing the new place
            # where the robot can be moved on
            road_str = ''.join(road)
            # replace the road_str where it was at the first time that we
            # split all the given line
            new_road = road_str.join(no_road)
            # replace the last line in the road attribute of labyrinth
            # with the  new creted one
            self.labyrinth.road[self.y] = new_road
            # self.x = new_x
            self.x = self.labyrinth.road[self.y].index(self.form)
        else:
            print('>>> No data', match)

    def move_forward(self, new_x: int):
        self.move_on_x(new_x)

    def move_backward(self, new_x):
        new_x = -new_x
        self.move_on_x(new_x, k='l')

    def move_on_y(self, y_):
        """Manage the movement on y axis of the road"""
        # we get the line where the robot is
        init_y = [elt for elt in self.labyrinth.road[self.y]]
        # set the las line where the robot wont to go
        final_y = [elt for elt in self.labyrinth.road[self.y + y_]]
        # get the exact value of the index of robot in the init line
        x = init_y.index(self.form)
        # get the char on the final line with the same index than the robot
        final_char = final_y[x]
        # if the final char is in this given tuple of char then the robot can
        # be moved without problem (live decrease)
        if final_char in (' ', '%', 'i', '.'):
            self.bonus = 5 if final_char == '%' or final_char == 'i' else 0
            final_y[x] = self.form
            init_y[x] = ' '
            self.labyrinth.road[self.y + y_] = ''.join(final_y)
            self.labyrinth.road[self.y] = ''.join(init_y)
            self.y += y_

    def move_down(self, new_y=1):
        self.move_on_y(new_y)

    def move_up(self, new_y=-1):
        self.move_on_y(new_y)

    def __repr__(self):
        return '<Robot: {}> x = {} ; y = {}'.format(self.name, self.x, self.y)

    def print_card(self):
        for line in playground_generator(self.labyrinth.road):
            print(line)

    def is_end(self):
        """To verify if the robot is at the exit zone of the road"""
        # the end is reprented by this pattern
        pattern = r'(?P<end>X>>)'
        # get the actual y position of the robot
        actual_y_pos = self.y
        # get this line in the end_line variable
        end_line = self.labyrinth.road[actual_y_pos]
        # verify if we have a match
        match = re.search(pattern, end_line)
        # if True, we print the win message
        if match:
            print('\nYou Win!!!\n'.title())
            return True
        else:
            return False


if __name__ == '__main__':
    name_, playground_ = playground_choice()
    labyrinth_ = Labyrinth(name_, playground_)
    robot_ = Robot('Mac', labyrinth_)
    print(robot_)
    robot_.move_forward(12)
    robot_.print_card()
    print(robot_)
    robot_.move_down()
    robot_.print_card()
    print(robot_)
