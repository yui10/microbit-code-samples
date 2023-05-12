from time import sleep  #ライブラリのインポート
import winsound
import serial
import random
from collections import deque
import os
com = serial.Serial("COM3", 9600, timeout=1)  #初期設定(COMポートを開く)

INIT_X = 1
INIT_Y = 1

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
#プレイヤーの向き制御用
aspe = [">", "V", "<", "^"]
arrow_x = [1, 0, -1, 0]
arrow_y = [0, 1, 0, -1]


class Labyrinth:
    WIDTH_SIZE = 19
    """マップの横幅"""
    HEIGT_SIZE = 19
    """マップの縦幅"""
    def __init__(self, x=1, y=1) -> None:
        self.base_map = [[1] * (self.WIDTH_SIZE + 2)
                         for j in range(self.HEIGT_SIZE + 2)]
        """マップ"""

        self.init_x, self.init_y = x, y
        """スタートの座標"""

        self.gx, self.gy = -1, -1
        """ゴールの座標"""

    def start(self):
        """
        ゲームの初期化処理を行う"""
        #マップの初期化処理を行う
        self.base_map = self.create_map()
        self.gx, self.gy = self.BFS()
        #ゴールの設定
        self.base_map[self.gy][self.gx] = 3

    def create_map(self):
        """
        マップの生成"""
        #空のマップを生成
        map = [[1] * (self.WIDTH_SIZE + 2) for j in range(self.HEIGT_SIZE + 2)]
        map[self.init_y][self.init_x] = 2  #初期位置
        queue = [(self.init_x, self.init_y)]  #キューを設定
        while queue:
            item = queue.pop()  #取り出し
            array = list(range(4))  #リスト生成とシャフル
            random.shuffle(array)
            for i in array:
                x2 = item[0] + dx[i] * 2  #穴を開ける先の座標
                y2 = item[1] + dy[i] * 2
                if not (1 <= x2 <= self.WIDTH_SIZE):  #範囲ないか
                    continue
                elif not (1 <= y2 <= self.HEIGT_SIZE):
                    continue
                if map[y2][x2] != 1:  #道などではないか
                    continue
                for j in range(1, 3):  #穴(通路)を開ける
                    map[item[1] + dy[i] * j][item[0] + dx[i] * j] = 0
                queue.append((x2, y2))  #移動後の座標を入れる
        return map

    def BFS(self):
        """
        幅優先探索を使用して開始位置からもっとも遠い場所を求める"""
        queue = deque([(self.init_x, self.init_y, 0)])  #初期値
        _gx, _gy = self.init_x, self.init_y
        max_dist = 0
        #探索済みかを判別するためのマップ
        check_map = [[0] * (self.WIDTH_SIZE + 2)
                     for j in range(self.HEIGT_SIZE + 2)]
        check_map[self.init_y][self.init_x] = 1
        while len(queue) > 0:
            _x, _y, _t = queue.popleft()  #キューから取得
            for i in range(4):  #4方向に移動
                xx = _x + dx[i]
                yy = _y + dy[i]
                if not (1 <= xx <= self.WIDTH_SIZE):  #範囲内か
                    continue
                elif not (1 <= yy <= self.HEIGT_SIZE):
                    continue
                if self.base_map[yy][xx] != 0:  #通路であるか
                    continue
                if check_map[yy][xx] == 0:  #未探索の場所か
                    _t += 1  #ターン数を加算
                    check_map[yy][xx] = _t  #探索済みにする
                    queue.append((xx, yy, _t))  #移動後の座標などをキューに追加
                    if max_dist < _t:  #最大のターンの場所であるか
                        _gx, _gy = xx, yy  #座標代入
                        max_dist = _t
        return _gx, _gy

    def show(self, now_x=-1, now_y=-1, direct=0):
        """
        マップを表示"""
        dict = {0: " ", 1: "#", 2: "S", 3: "G"}
        for i in range(self.HEIGT_SIZE + 2):
            for j in range(self.WIDTH_SIZE + 2):
                if now_x == j and now_y == i:  #プレイヤーの表示
                    print(aspe[direct], end="")
                else:  #各アイテムの表示
                    print(dict[self.base_map[i][j]], end="")
            print("")


#ゲームを開始
Game = Labyrinth(INIT_X, INIT_Y)
Game.start()
direct = 0
x, y = INIT_X, INIT_Y
Game.show()
while True:
    moji = com.readline().strip().decode('UTF-8')  #文字を受信
    if moji == 'A':
        print("A")  #受信文字が”A"のときは表示する(引き続き受信待ち)
        Game.start()  #ゲームをやり直す
    elif moji == 'B':  # 受信文字が"B"のときは終了する
        break  #ゲームを終了
    elif moji[0:2] == "XY":
        li = moji.split(',')  #移動量の取り出し
        xx = x + int(li[1])  #座標に加算する
        yy = y + int(li[2])
        if Game.base_map[yy][xx] != 1:  #壁以外であるか
            x, y = xx, yy  #移動する
            #ゴールへたどり着いたか
            if xx == Game.gx and yy == Game.gy:
                #ゲームクリアした事を表示してゲームをリセット
                os.system('cls')
                Game.show()
                print("GAME CLEAR!!!")
                winsound.Beep(1000, 1000)
                sleep(5)
                Game.start()
                x, y = INIT_X, INIT_Y
    else:
        continue
    os.system('cls')  #コンソールをクリアする
    Game.show(x, y, 1)  #マップの表示