import torch
from net import Net
from input import get_input
import os
import random

nn = Net()
nn.load_state_dict(torch.load('50all'))

def show(img):
    print((len(img[0])+2) * '+ ')
    for row in img:
        print('+', *[' ' if x == 0 else 'X' for x in row], '+')
    print((len(img[0])+2) * '+ ')
        

def letter(arr, count=1):
    maxes = [0 for i in range(count)]
    indexes = [0 for i in range(count)]

    for i, x in enumerate(arr):
        if x > min(maxes):
            indexes[maxes.index(min(maxes))] = i
            maxes[maxes.index(min(maxes))] = x


    return ['ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i] for i in indexes], maxes

cmds = ['']
while True:

    if cmds[0] == '':
        info = True if '-info' in cmds else False
        fn = random.choice(os.listdir('../genLetts_py/data'))
        img = get_input('../genLetts_py/data/' + fn)
        show(img)
        guess = letter(nn(img.unsqueeze(0).unsqueeze(0))[0], count=3)
        #print('guess:', *[guess[0][i] + ': ' + str(guess[1][i].item()) for i in range(len(guess[0]))])
        if info:
            print(*[str(guess[0][i]) + ': ' + str(guess[1][i].item()) for i in range(len(guess[0]))])
        print('GUESS:', guess[0][guess[1].index(max(guess[1]))], 'TRUE:', fn[0])

    elif cmds[0] == 'acc':
        info = True if '-info' in cmds else False
        try:
            if len(cmds) == 1 or cmds[1][0] == '-':
                num = 100
            else:
                num = int(cmds[1])
            acc = 0
            for i in range(num):
                fn = random.choice(os.listdir('../genLetts_py/data'))
                img = get_input('../genLetts_py/data/' + fn)
                guess = letter(nn(img.unsqueeze(0).unsqueeze(0))[0])
                #print('guess:', *[guess[0][i] + ': ' + str(guess[1][i].item()) for i in range(len(guess[0]))])
                acc += int(guess[0][0] == fn[0])
                if info and guess[0][0] != fn[0]:
                    print('WRONG!! guessed', guess[0][0], 'instead of', fn[0], '!')
            print(acc, 'correct out of', num, 'tries!', 'Accuracy:', str(acc/num*100) + '%')

        except TypeError:
            print('after acc must follow an integer')
            

    elif cmds[0] == 'let':
        try:
            if len(cmds) == 1:
                num = 100
            else:
                num = int(cmds[1])
            times = {}
            correct = {}
            acc = 0

            for i in range(num):
                fn = random.choice(os.listdir('../genLetts_py/data'))
                img = get_input('../genLetts_py/data/' + fn)
                guess = letter(nn(img.unsqueeze(0).unsqueeze(0))[0])
                #print('guess:', *[guess[0][i] + ': ' + str(guess[1][i].item()) for i in range(len(guess[0]))])
                acc += int(guess[0][0] == fn[0])
                correct[fn[0]] = correct.get(fn[0], 0) + int(guess[0][0] == fn[0])
                times[fn[0]] = times.get(fn[0], 0) + 1

            print(*[str(key) + ': ' + str(correct[key]) + ' out of ' + str(times[key])
                        + '! Acc: ' + str(correct[key]/times[key]*100) + '%' for key in sorted([key for key in times])], sep='\t')
            print('TOTAL:', acc, 'correct out of', num, 'tries!', 'Accuracy:', str(acc/num*100) + '%')

        except TypeError:
            print('after let must follow an integer')

    elif cmds[0] == 'quit':
        break
        
    else:
        print('''     command must be "" for a visualized trial
    or "acc" + a number to show accuracy rates
    or "let" + a number to show accuracy letterwise''')

    cmds = input('command: ').split(' ')