import os
import re
import sys

def help_player():
    print('\nThe robot is an @ sign move it to the exit')
    print('use the key: H, J, K and L to move the robot')
    print('a) H to move left')
    print('b) J to move down')
    print('c) K to move up')
    print('d) L to move right')
    print('e) key:n will move it n time to the key represented direction'
          ' \reg: h3 will move it 3 time to left\n')


def question(quest: str, resp: tuple):
    """this method a question to the user and
    return an answer, which will be verified
    for using.
    """

    while True:
        answer = input(quest)[0]
        if answer in resp:
            return answer


def score_update(live, old_x, old_y, robot_, score):
    new_x = robot_.x
    new_y = robot_.y
    if old_x == new_x and old_y == new_y:
        live -= 1
    else:
        score += 1 + robot_.bonus
        robot_.bonus = 0
    return live, score


def playground_generator(data: list):
    if data is not None:
        for line_ in data:
            yield line_
    else:
        return


def list_dir_(dir_: str):
    pattern_path = r'/*(?P<name>\w*)(?P<extension>\.txt|\.stat)$'
    list_dir = []
    path_to = []
    for k, v in enumerate(os.listdir(dir_)):
        if v.endswith(re.search(pattern_path, v).group('extension')):
            path = os.path.join(dir_, v)
            list_dir.append((k, re.search(pattern_path, path).group('name')))
            path_to.append((k, path))
    sorted(list_dir)
    return list_dir, path_to


def playground_choice():
    """
    this method select on which playground the user will
    play
    :return: playground
    """
    while True:
        quest = '>>> SELECT A PLAYGROUND <<<\n'
        list_cd, path_ = list_dir_(sys.path[0] + os.sep + 'cards')
        ins = list()
        for i in list_cd:
            ins.append(str(i[0]))
            quest += '{}) {}\n'.format(i[0], i[1])
        exit_ = str(len(ins))
        ins.append(exit_)
        quest += '{}) quit\n>>> '.format(exit_)
        answer = question(quest, tuple(ins))
        if answer == exit_:
            return '', ''
        # cd = ''
        try:
            with open(path_[int(answer)][1]) as cd:
                data = cd.readlines()
                path = path_[int(answer)][1]
                return path, data
        except FileNotFoundError or FileExistsError:
            print('<<< {}: No such file or directory'
                  'for card was found'.format(cd))
