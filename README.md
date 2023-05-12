# microbit-code-samples
過去にMicro:bitを使用した課題にて作成したプログラムです

## 動作環境
- Micro:bit × 2

- PC (Windows10)

- Tera Term

- [Mu Editor](https://codewith.mu/)

## 使用方法
1. Mu Editorを使用しコントローラーとなるMicro:bit(B)を接続し、microbit_B.pyを書き込む
2. 同じ手順でもう一方のMicro:bit(A)を接続し、microbit_A.pyを書き込む
3. プログラム起動後、Tera Termを使用してMicro:bit(A)とシリアル通信を行いPC上に画面を出力させる
4. Micro:bit(B)を操作し、ゲームを行う

## ゲームについて
- Micro:bitを上下左右方向に傾けて操作します
- Micro:bitの各ボタンを押した時の挙動は以下の通りです
  - Aボタン : ゲームをやり直します(マップは再生成されます)
  - Bボタン : ゲームとプログラムを終了します
- 表示される意味か以下の通りです
  - 「S」 : スタート
  - 「G」 : ゴール
  - 「V」 : プレイヤー
  - 「#」 : 壁
  - 「 」 : 道
- ゴールにたどり着いた場合は5秒後に自動的に新しいゲームが開始されます

# License
This software is released under the MIT License, see LICENSE.