import pandas as pd
from itertools import islice
import sprites as sp

WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32
FPS = 60

TEXT_LAYER = 5
PLAYER_LAYER = 4
ITEM_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3

special_item = ['v', 'k', 'j', 'u', 'd', 'x']


RED = (255, 0, 0)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (189, 252, 201)
WHITE = (255,255,255)
ORANGE = (255,165,0)

tilemap = [
    '141114114114111411114111411141',
    '13131BBaaBBBBBBBBB131131112141', 
    '13322B.....b....cB141411121111', 
    '12123Bd.......P..B411213412111', 
    '13131B..........eB444111311311', 
    '11212Bf..........B444131111121', 
    '41111BBBBBggBBBBBBBBBBBBBBBBB1', 
    '4BBBBB.h...........B...w....B1', 
    '1B.................m.......xB1', 
    '1B......i.....j....m.......vB1',
    '1B..........k......B........B1',
    '4BBBBBB............BBBBBBBBBB1', 
    '1Bp...B............n........B4', 
    '1B....o............n.......sB1',
    '1B....o............B....t...B4',
    '1Bq..rB............B..u.....B1',
    '1BBBBBBBBBBllBBBBBBBBBBBBBBBB1',
    '11141112222..33331111411111411'
        ]

label_dict = {
    "a" : "bedroom_window",
    "b" : "photo_frame",
    "c" : "bed_bedroom",
    "d" : "safe_deposit_box",
    "e" : "desk",
    "f" : "closet",
    "g" : "door",
    "h" : "refrigerator",
    "i" : "couch",
    "j" : "television",
    "k" : "playstation",
    "l" : "door",
    "m" : "door",
    "n" : "door",
    "o" : "door",
    "p" : "plug",
    "q" : "switchboard",
    "r" : "carton",
    "s" : "bed_kidroom",
    "t" : "tin_box",
    "u" : "puzzle",
    "v" : "tub",
    "w" : "toilet",
    '1' : 'grass',
    '2' : 'flower1',
    '3' : 'flower2',
    '4' : 'flower3',
    'x' : 'faucet'
        }

list_item = {
    "a" : 0,
    "b" : 0,
    "c" : 0,
    "d" : 0,
    "e" : 0,
    "f" : 0,
    "g" : 0,
    "h" : 0,
    "i" : 0,
    "j" : 0,
    "k" : 0,
    "l" : 0,
    "m" : 0,
    "n" : 0,
    "o" : 0,
    "p" : 0,
    "q" : 0,
    "r" : 0,
    "s" : 0,
    "t" : 0,
    "u" : 0,
    "v" : 0,
    "w" : 0,
    'x' : 0
}

def get_description(label):
        f = open('items.csv', encoding='utf-8-sig', mode='r')
        dict = {}
        index = f.readline().strip().split(',')
        label_lst = []
        for line in islice(f, 0, None):
            inp = [t for t in line.strip().split(',')]
            dict[inp[0]] = inp[1:]
            label_lst += [inp[0]]

        df = pd.DataFrame.from_dict(dict, orient='index')
        df.index = label_lst
        df.columns = index[1:]

        # 保險箱    
        if label == 'd': 
            while True:
                num = str(input("請輸入4位密碼:"))
                if num == "0526":
                    if list_item['d'] == 1:
                        chat = df.at[label_dict[label], 'description_condition_2']
                        break
                    else:
                        chat = df.at[label_dict[label], 'description_condition_1']
                        list_item['d'] = 1
                        break
                else:
                    chat = f"密碼錯誤，請重新輸入"
                    break

        elif list_item[label] == 0:
            chat = df.at[label_dict[label], 'description_condition_1']
            list_item[label] = 1

        elif list_item[label] == 1 or list_item[label] == 2:
            if label not in special_item:
                chat = df.at[label_dict[label], 'description_condition_2']
                list_item[label] = 2
            else:
                # special_item = ['v', 'k', 'j', 'u', 'd', 'x']
                # 浴缸
                if label == 'v':
                    if list_item['p'] == 1 or list_item['p'] == 2:  # 有沒有塞子
                        if list_item['x'] == 2:  # 水龍頭打開
                            chat = df.at[label_dict[label], 'description_condition_3']
                        else:
                            chat = df.at[label_dict[label], 'description_condition_2']
                            list_item[label] = 2
                    else:
                        chat = df.at[label_dict[label], 'description_condition_1']

                # 水龍頭
                if label == 'x':
                    if list_item['v'] == 2:
                        chat = df.at[label_dict[label], 'description_condition_2']
                        list_item[label] = 2
                    else:
                        chat = df.at[label_dict[label], 'description_condition_1']
                
                # PS
                if label == 'k':
                    if list_item['q'] >= 1:
                        chat = df.at[label_dict[label], 'description_condition_2']
                        list_item[label] = 2
                    else:
                        chat = df.at[label_dict[label], 'description_condition_1']

                # 電視
                if label == 'j':
                    if list_item['k'] >= 2:
                        chat = df.at[label_dict[label], 'description_condition_2']
                        list_item[label] = 2
                    else:
                        chat = df.at[label_dict[label], 'description_condition_1']

                # 拼圖
                if label == 'u':
                    if list_item['f'] >= 1 and list_item['i'] >= 1 and list_item['t'] >= 1 and list_item['r'] >= 1:
                        chat = df.at[label_dict[label], 'description_condition_2']
                        list_item[label] = 2
                    else:
                        chat = df.at[label_dict[label], 'description_condition_1']

        return chat