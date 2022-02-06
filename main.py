import parse_cards
import numpy as np
import wscreenshot
import time
import cv2
import os

INIT = 0
WAIT = 1
RUN = 2
END = 3
DEBUG = False
WINTEXT = '天天爱掼蛋'

class DEBUGWS:
    def __init__(self):
        self.d = 'images5'
        img_files = os.listdir(self.d)
        self.img_files = sorted(img_files)
        # self.images = [cv2.imread(os.path.join(d, f)) for f in img_files]
        self.index = 0

    def screenshot(self):
        fname = os.path.join(self.d, self.img_files[self.index])
        img = cv2.imread(fname)
        self.index += 5
        self.index %= len(self.img_files)
        return fname.split('.')[0], img


class JiPaiQi:
    def __init__(self, is_debug=False):
        self.is_debug=is_debug
        self.status = WAIT
        self.prev_who = None
        self.who = None
        self.ws = None
        self.my_cards = None
        self.remain_cards = {}
        self.start_timestamp = 'temp'

        self.init()

    def init(self):
        self.prev_who = None
        self.who = None
        self.ws = None
        self.my_cards = None
        self.remain_cards = {
            'A': 8,
            '2': 8,
            '3': 8,
            '4': 8,
            '5': 8,
            '6': 8,
            '7': 8,
            '8': 8,
            '9': 8,
            '10': 8,
            'J': 8,
            'Q': 8,
            'K': 8,
            'Joker': 4
        }

        if self.is_debug:
            self.ws = DEBUGWS()
            self.start_timestamp = self.ws.img_files[0].split('.')[0]
        else:
            while True:
                try:
                    self.ws = wscreenshot.Screenshot(WINTEXT)
                except Exception:
                    time.sleep(1)
                    continue
                print('ws created.')
                break
            self.start_timestamp = str(int(time.time() * 10))
        if not os.path.exists(self.start_timestamp):
            os.mkdir(self.start_timestamp)
        self.status = INIT
        print('-----------------init---------------')

    def run(self):
        if not DEBUG:
            timestamp = str(int(time.time()))
            img = self.ws.screenshot()
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(self.start_timestamp, timestamp+'.png'), img_gray)
        else:
            timestamp, img = self.ws.screenshot()
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        if self.status == INIT:
            is_game_start = parse_cards.parse_game_start(img_gray)
            if is_game_start:
                self.status = WAIT
                print(timestamp, 'game_start')
                return
            else:
                time.sleep(0.01)
                return
        elif self.status == WAIT:
            res = parse_cards.parse_clock(img_gray)
            if not res:
                time.sleep(0.01)
                return
            else:
                direct_num, is_start_clock = res
                if not is_start_clock:
                    print(timestamp, 'error: is_start_clock False', timestamp)
                self.who = direct_num
                self.status = RUN
                self.my_cards = parse_cards.parse_big_cards(img_gray)
                self.my_cards = [x[2] for x in self.my_cards]
                self.my_cards = sorted(self.my_cards)
                for card in self.my_cards:
                    self.remain_cards[card[1:]] -= 1
                print(timestamp, 'start_clock', self.my_cards, self.remain_cards)
                return
        elif self.status == RUN:
            if parse_cards.parse_game_start(img_gray):
                self.init()
                return
            res = parse_cards.parse_clock(img_gray)
            if not res:
                time.sleep(0.01)
                return
            else:
                direct_num, is_start_clock = res
                self.prev_who, self.who = self.who, direct_num
                if self.prev_who != self.who:
                    # todo: "不出" 与解析失败的区别
                    cards = parse_cards.parse_small_cards(img_gray, self.prev_who)
                    cards = [x[2] for x in cards]
                    cards = sorted(cards)
                    for card in cards:
                        self.remain_cards[card[1:]] -= 1
                    print(timestamp, self.prev_who, cards, self.remain_cards)
                else:
                    time.sleep(0.01)
                    return


if __name__ == '__main__':
    jipaiqi = JiPaiQi()
    while True:
        jipaiqi.run()
