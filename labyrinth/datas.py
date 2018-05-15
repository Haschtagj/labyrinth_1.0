"""This module serves all necessary useful functions

for data retrieving.
"""
import pickle

from model import Labyrinth
from model import Player
from model import Robot
from utils import help_player
from utils import playground_choice
from utils import question
from utils import score_update
import sys
import os


def load_data():
    """Ask to load the player's data

    if the user is not in the stat dir, it will be created on saving
    else the function loads the founded one in the dir stat or quit the
    program
    in the case that user hits 3
    Returns
    -------
    Player
        object which represent the current player.
    """
    while True:
        print(' ROBOT_C '.center(20, '*'))
        answer = question(
            '1) continue\n2) new\n3) quit\n4) help\n >> ',
            ('1', '2', '3', '4'))
        # question: this function is a basic function to looping a question as
        # far as an answer in the tuple is founded
        if answer == '3':  # if 3 we exit the program
            break
        if answer == '4':  # if 4 we print user guide
            help_player()
        if answer not in ('3', '4'):  # if not 3 or 4
            # we ask the name of the current player
            p_name = input('Enter your user name:: ')
            # then try to load it from a user dir
            # this function bellow return one boolean and
            # a player which have been founded if the boolean
            # is true
            exist, player = player_from_file(p_name)
            # the error that will be printed if the file is not founded
            err = '<<< {}.stat: No such file or directory was found'\
                .format(p_name)
            # if the answer was 1 and the returned boolean is true,
            if answer == '1' and exist:
                print('<<< last data for {} loaded'
                      .format(player.name))
                # we return the loaded user
                return player
            # else
            elif answer == '2' and not exist:
                # we print an error
                print(err)
                # then prevent the current user that a new user with the
                # given name will be created
                print('<<< A player with the name {} '
                      'will be created on saving'.format(player.name))
                # we return the new created player
                # it will be saved after the first party
                return player
            elif answer == '2' and exist:
                print('<<< last data for {} loaded'
                      .format(player.name))
                # we return the loaded user
                return player
            else:
                print(err)


def main(live, player, score):
    """Start the game with all retrieving data

    live, player and score but also card and so on
    Parameters.
    ----------
    live : int
        Represent the number of chance of the
        current user.
    player : Player
        Represent the player itself.
    score : int
        Represent the score of the current user.
    """
    # this function bellow returns the chosen playground and it name
    name_, playground_ = playground_choice()
    if name_ != '' and playground_ != '':
        # these data are given to a Labyrinth object for new instance
        labyrinth_ = Labyrinth(name_, playground_)
        # then we configure the parameter card in the Player object
        # we set the name of the card
        player.card = name_
        # then create a Robot object with the new created Labyrinth
        robot_ = Robot('Mac', labyrinth_)
        # we use the robot's method print_card to print the current playground
        robot_.print_card()
        while live:  # we loop
            # the retrieve the initials robot's positions
            old_x, old_y = robot_.x, robot_.y
            # print the current data for the current party
            print('\n# card = {}\nscore = {}\nlive = {}\nrobot: {}\n'
                  .format(player.card, score, live, robot_).title())
            # the function is_end verify if the condition to win the game
            # are true and returns a boolean which confirm that
            if robot_.is_end():
                # if it's true wwe ask to save the party
                answer = question('Save this part? (y/n) ', ('y', 'n'))
                # if yes, we saved it
                if answer == 'y':
                    # set the new value for the current player
                    # last_score and also new_score
                    player.last_score = player.last_score + score
                    player.new_score = score
                    print(player)
                    # by calling the save_data_player function
                    save_data_player(player)
                    break
                else:  # if the answer is not y then we just print the current
                    # data for the current user!
                    player.last_score = player.last_score + score
                    player.new_score = score
                    print(player)
                    break
            # in the case that the condition to win are not true,
            # we ask to the user to hit one key movement to move the
            # robot
            answer = input(' move key:: ')
            if answer == '4':  # if 4 print user guide
                live = live
                help_player()
            if len(answer) >= 2:
                if answer[0] == 'h':
                    robot_.move_forward(int(answer[1:]))
                    robot_.print_card()
                    f = live, old_x, old_y, robot_, score
                    live, score = score_update(*f)
                elif answer[0] == 'l':
                    robot_.move_backward(int(answer[1:]))
                    robot_.print_card()
                    f = live, old_x, old_y, robot_, score
                    live, score = score_update(*f)
            if len(answer) == 1:
                if answer[0] == 'j':
                    robot_.move_down()
                    robot_.print_card()
                    f = live, old_x, old_y, robot_, score
                    live, score = score_update(*f)
                elif answer[0] == 'k':
                    robot_.move_up()
                    robot_.print_card()
                    f = live, old_x, old_y, robot_, score
                    live, score = score_update(*f)


def player_from_file(user_name: str):
    """Retrieve the data of one given player,

    convert it to the Player instance and return it form usage
    :param user_name:
    :return: an boolean which is True if the user data has been founded
    or False if not and The current Player
    """
    try:
        st = 'stats/{}.stat'
        path = f'{sys.path[0] + os.sep + st}'.format(user_name)
        with open(path, 'br') as user_data:
            unpickler = pickle.Unpickler(user_data)
            player = unpickler.load()
            print('<<< Loaded!')
            return True, player
    except FileNotFoundError:
        return False, Player(name=user_name)


def save_data_player(player: Player):
    """Perform the serialization of a Player type

    to save the current data in a file named with the player_name
    and then return the current updated data
    :param player:
    :return: player
    """
    try:
        if player:
            st = 'stats/{}.stat'
            path = f'{sys.path[0] + os.sep + st}'.format(player.name)
            with open(path, 'bw')\
                    as player_data:
                pickler = pickle.Pickler(player_data)
                pickler.dump(player)
                print('<<< Saved!')
                return player
    except FileExistsError or FileNotFoundError:
        print('<<< Can not save: No such file was found')


if __name__ == '__main__':
    crd = playground_choice()  # crd = card
    if crd is not None:
        for line in crd:
            print(line)
    p = load_data()
    pl = save_data_player(p)
