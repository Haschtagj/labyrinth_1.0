"""this module uses all another to be functional
so please don't delete third parts of this project
"""
from datas import load_data
from utils import question
from datas import main


def start():
    """this function starts one existence or not existence party
    :return:
    """
    score = 0
    live = 7
    while True:
        player = load_data()  # award the load data definition function
        # for more informationcle
        if player:  # The load_data function can return a NoneType Object
            # so we verify that it is not a None object
            print('<<<', player)
            while True:
                main(live, player, score)
                # main represent the main function
                # using all existing one
                break
            break
        else:
            break


if __name__ == '__main__':
    start()
    answer = question('is\'t cool? (y/n) >> '.title(), ('y', 'n'))
    if answer == 'y':
        try:
            with open('labyrinth/stats/enjoy.txt') as enjoy:
                tmp = enjoy.readlines()
                for line in tmp:
                    print(line)
        except FileNotFoundError:
            print('File or directory not found')
    else:
        print('Je ferai de mon mieux la prochaine fois!')
