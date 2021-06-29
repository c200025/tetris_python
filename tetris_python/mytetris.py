from tkinter import Frame, Tk, PhotoImage, Label
from tkinter import ttk
from random import randrange
import sys
import os
boxs = []
lengthX = 10
lengthY = 23
for v in range(lengthX):
    boxs.append([])
    for s in range(lengthY):
        boxs[v].append(0)

hidey = 3

keepbox = []
nextbox = []
next2box = []
for v in range(4):
    nextbox.append([])
    keepbox.append([])
    next2box.append([])
    for s in range(4):
        nextbox[v].append(0)
        keepbox[v].append(0)
        next2box[v].append(0)

shapes = [0], [[0, 0], [1, 0], [0, 1], [1, 1]], [[1, 0], [2, 0], [0, 1], [1, 1]], [[0, 0], [0, 1], [1, 1], [1, 2]], [[0, 0], [1, 0], [1, 1], [2, 1]], [[1, 0], [0, 1], [1, 1], [0, 2]], [[0, 0], [1, 0], [2, 0], [1, 1]], [[1, 0], [0, 1], [1, 1], [1, 2]], [[1, 0], [0, 1], [1, 1], [2, 1]], [[0, 0], [0, 1], [1, 1], [0, 2]], [[0, 0], [
    0, 1], [0, 2], [1, 2]], [[0, 0], [1, 0], [2, 0], [0, 1]], [[0, 0], [1, 0], [1, 1], [1, 2]], [[0, 1], [1, 1], [2, 1], [2, 0]], [[1, 0], [1, 1], [0, 2], [1, 2]], [[0, 0], [0, 1], [1, 1], [2, 1]], [[0, 0], [1, 0], [0, 1], [0, 2]], [[0, 0], [1, 0], [2, 0], [2, 1]], [[0, 0], [0, 1], [0, 2], [0, 3]], [[0, 0], [1, 0], [2, 0], [3, 0]]


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


score = 0

keepShape = 0
nowShape = 0

stop = 0
keepUse = 0  # 0は未使用
noDrop = 0
nokey = 0
lastHole = randrange(lengthX)
enemyBlock = 0


root = Tk()
Myimgs = [PhotoImage(file=resource_path("gray.gif")), PhotoImage(file=resource_path("green.gif")), PhotoImage(file=resource_path("blue.gif")), PhotoImage(file=resource_path("pink.gif")), PhotoImage(
    file=resource_path("purple.gif")), PhotoImage(file=resource_path("red.gif")), PhotoImage(file=resource_path("yellow.gif")), PhotoImage(file=resource_path("cyan.gif")), PhotoImage(file=resource_path("lavender.gif")), PhotoImage(file=""), PhotoImage(file=resource_path("black.gif"))]


def config_load():
    global cnf, datalist, defaultSpeed, maxSpeed, maxScore, enemy_on
    cnf = []
    f = open('config.txt', 'r')
    datalist = f.readlines()
    for i in range(len(datalist)):
        cnf.append(datalist[i].split(','))
    f.close()

    defaultSpeed = int(cnf[0][1])  # テトリミノが落ちる最初の速度
    maxSpeed = int(cnf[1][1])  # テトリミノが落ちる速度の上限
    maxScore = int(cnf[2][1])  # 最高スコア
    enemy_on = bool(int(cnf[3][1]))  # お邪魔ブロックを出すか


def newGame():
    config_load()
    global score, speed, keepShape, nextShape, next2Shape, stop, noDrop, lastHole, enemyBlock
    stop = 0
    score = 0
    speed = defaultSpeed
    noDrop = 0
    keepShape = 0
    lastHole = randrange(lengthX)
    enemyBlock = 0
    nextShape = random()
    while(True):
        next2Shape = random()
        if(next2Shape != nextShape):
            break
    root.after_cancel(id)
    for v in range(len(keepbox)):
        for d in range(len(keepbox[v])):
            keepbox[v][d] = 0
            nextbox[v][d] = 0
            next2box[v][d] = 0
    for v in range(len(boxs)):
        for d in range(len(boxs[v])):
            boxs[v][d] = 0
    pushPiece()
    showScore(0)
    label_maxScore.config(text=str(maxScore))

    root.after(speed, ref)


def create():
    global labels
    labels = []
    for v in range(lengthX):
        labels.append([])
        for d in range(lengthY-hidey):
            labels[v].append(ttk.Label(Main_frame))
            labels[v][d].place(x=20*v, y=20*d)

    global keeplabels, nextlabels, next2labels
    keeplabels = []
    nextlabels = []
    next2labels = []
    for v in range(len(keepbox)):
        keeplabels.append([])
        nextlabels.append([])
        next2labels.append([])
        for d in range(len(keepbox[v])):
            keeplabels[v].append(ttk.Label(keep_frame))
            keeplabels[v][d].place(x=20*v, y=20*d)
            nextlabels[v].append(ttk.Label(next_frame))
            nextlabels[v][d].place(x=20*v, y=20*d)
            next2labels[v].append(ttk.Label(next2_frame))
            next2labels[v][d].place(x=20*v, y=20*d)


def imgChoice(num):
    if(num == 0):
        Myimg = Myimgs[0]  # default
    elif(num == 1):
        Myimg = Myimgs[1]  # o
    elif(num == 2 or num == 3):
        Myimg = Myimgs[2]  # s
    elif(num == 4 or num == 5):
        Myimg = Myimgs[3]  # Z
    elif(num >= 6 and num <= 9):
        Myimg = Myimgs[4]  # T
    elif(num >= 10 and num <= 13):
        Myimg = Myimgs[5]  # L
    elif(num >= 14 and num <= 17):
        Myimg = Myimgs[6]  # 7
    elif(num == 18 or num == 19):
        Myimg = Myimgs[7]  # -
    elif(num == 20):
        Myimg = Myimgs[10]
    elif(num == 25):
        Myimg = Myimgs[8]  # gohst
    elif(num == 30):
        Myimg = Myimgs[0]  # delete line
    return Myimg


def showgame():
    for v in range(len(labels)):
        for d in range(len(labels[v])):
            Myimg = imgChoice(boxs[v][d+hidey])
            labels[v][d].config(image=Myimg)

    for v in range(len(keepbox)):
        for d in range(len(keepbox[v])):
            Myimg = imgChoice(keepbox[v][d])
            keeplabels[v][d].config(image=Myimg)
            Myimg = imgChoice(nextbox[v][d])
            nextlabels[v][d].config(image=Myimg)
            Myimg = imgChoice(next2box[v][d])
            next2labels[v][d].config(image=Myimg)
    label_enemy.config(text=str(enemyBlock))


def showNext():
    for i in shapes[nextShape]:
        shapex = i[0]
        shapey = i[1]
        nextbox[shapex][shapey] = nextShape

    for i in shapes[next2Shape]:
        shapex = i[0]
        shapey = i[1]
        next2box[shapex][shapey] = next2Shape


def onPiece(m, mox, moy):
    for i in shapes[m]:
        shapex = i[0]
        shapey = i[1]
        movex = mox + shapex
        movey = moy + shapey
        if(movex >= lengthX or movex < 0 or movey >= lengthY or movey < 0):
            return -1  # ますの範囲外
        if(boxs[movex][movey] != 0 and boxs[movex][movey] < 25):
            return -2  # ブロックが置かれてる
    return 1


def setGhost(m, mox, moy):
    for i in range(moy, lengthY+1):
        ind = i
        ok = onPiece(m, mox, ind)
        if(ok <= -1):
            showGhost(m, mox, ind-1)
            return


def deleteGhost():
    for v in range(len(labels)):
        for d in range(len(labels[v])):
            if(boxs[v][d+hidey] == 25):
                boxs[v][d+hidey] = 0


def showGhost(m, mox, moy):
    for i in shapes[m]:
        shapex = i[0]
        shapey = i[1]
        movex = mox + shapex
        movey = moy + shapey
        boxs[movex][movey] = 25


def showPiece(m, mox, moy):
    for i in shapes[m]:
        shapex = i[0]
        shapey = i[1]
        movex = mox + shapex
        movey = moy + shapey
        boxs[movex][movey] = m


def deletePiece(m, mox, moy):
    for i in shapes[m]:
        shapex = i[0]
        shapey = i[1]
        movex = mox + shapex
        movey = moy + shapey
        boxs[movex][movey] = 0


def move(m, mox, moy, direction):
    global x, y
    littlex = 0
    littley = 0
    if(direction == 2):
        littley = 1

    if(direction == 6):
        littlex = 1

    if(direction == 4):
        littlex = -1

    deletePiece(m, mox, moy)

    if(direction == 8):
        return

    for i in shapes[m]:
        shapex = i[0]
        shapey = i[1]
        movex = mox + shapex + littlex
        movey = moy + shapey + littley
        if(movex >= lengthX or movex < 0 or movey >= lengthY or movey < 0):
            showPiece(m, mox, moy)
            return
        num = boxs[movex][movey]
        if(num < 25 and num > 0):
            showPiece(m, mox, moy)
            return
    showPiece(m, mox+littlex, moy+littley)
    x = mox+littlex
    y = moy+littley


def change(num):
    piece = num

    global nowShape
    if(num == 0):
        num = num  # default
    elif(num == 1):
        num = num  # o
    elif(num == 2 or num == 3):
        num += 1
        if(num > 3):
            num = 2  # s
    elif(num == 4 or num == 5):
        num += 1
        if(num > 5):
            num = 4  # Z
    elif(num >= 6 and num <= 9):
        num += 1
        if(num > 9):
            num = 6  # T
    elif(num >= 10 and num <= 13):
        num += 1
        if(num > 13):
            num = 10  # L
    elif(num >= 14 and num <= 17):
        num += 1
        if(num > 17):
            num = 14  # 7
    elif(num == 18 or num == 19):
        num += 1
        if(num > 19):
            num = 18  # I
    deletePiece(piece, x, y)
    deleteGhost()

    check = onPiece(num, x, y)
    if(check == -1):
        o = smallMovePiece(num, x, y)
        if(o == -1):
            num = piece
        showPiece(num, x, y)
    elif(check == -2):
        num = piece
        showPiece(piece, x, y)
    nowShape = num


def smallMovePiece(m, mox, moy):
    for i in shapes[m]:
        shapex = i[0]
        shapey = i[1]
        movex = mox + shapex
        movey = moy + shapey
        if(movex >= lengthX):
            sw = movex-9
            movex -= sw
            global x
            x = mox-sw
        if(movey >= lengthY):
            sw = movey-lengthY+1
            movey -= sw
            global y
            y = moy-sw

    num = onPiece(m, x, y)
    if(num <= -1):
        x = mox
        y = moy
        return -1


def destroyBoard():
    children = Main_frame.winfo_children()
    for child in children:
        child.destroy()


def pushPiece():
    global x, y, nowShape, nextShape, next2Shape, keepUse, noKey
    x = 4
    y = 0
    keepUse = 0
    nowShape = nextShape
    nextShape = next2Shape
    noKey = 0
    while(True):
        next2Shape = random()
        if(next2Shape != nextShape):
            break
    for v in range(len(nextbox)):
        for d in range(len(nextbox[v])):
            nextbox[v][d] = 0
            next2box[v][d] = 0
    if(keepShape > 0):
        for i in shapes[keepShape]:
            shapex = i[0]
            shapey = i[1]
            keepbox[shapex][shapey] = keepShape
    showNext()


def random():
    num = randrange(1, 15)
    if(num >= 1 and num <= 2):
        num = 1  # o
    elif(num >= 3 and num <= 4):
        num = 2  # s
    elif(num >= 5 and num <= 6):
        num = 4  # Z
    elif(num >= 7 and num <= 8):
        num = 6  # T
    elif(num >= 9 and num <= 10):
        num = 10  # L
    elif(num >= 11 and num <= 12):
        num = 14  # 7
    elif(num >= 13 and num <= 14):
        num = 18  # I
    if(nowShape == num):
        num = random()
    return num


def checkLine():
    line = 0
    for v in range(lengthY-hidey):
        dot = 0
        for d in range(lengthX):
            if(boxs[d][lengthY-1-v] != 0 and boxs[d][lengthY-1-v] < 25):
                dot += 1
        if(dot == lengthX):
            line += 1
            for d in range(lengthX):
                boxs[d][lengthY-1-v] = 30
    showScore(line)
    return line


def dropLine(line):
    for v in range(line):
        for v in range(lengthY-hidey):
            chaos = 0
            for d in range(lengthX):
                if(boxs[d][lengthY-1-v] == 30 or boxs[d][lengthY-1-v] == 0):
                    chaos += 1
            if(chaos == lengthX):
                for d in range(lengthX):
                    boxs[d][lengthY-1-v] = boxs[d][lengthY-2-v]
                    boxs[d][lengthY-2-v] = 0


def showScore(num):
    global score
    lin = 0
    sc = score
    if(num == 4):
        lin = 6000
    elif(num == 3):
        lin = 4000
    elif(num == 2):
        lin = 2500
    elif(num == 1):
        lin = 1000
    score = sc + lin
    global speed
    sw = int(score/10000)
    speed = defaultSpeed-(sw*50)
    if(speed < maxSpeed):
        sw = int((defaultSpeed-maxSpeed)/50)
        speed = maxSpeed
    tex = "Level:"+str(sw+1)

    label_score.config(text=str(score))
    label_level.config(text=str(tex))
    label_speed.config(text="Speed:"+str(speed))


def gameover():
    global noKey
    label_key.config(text="game over")
    noKey = 1
    for v in range(len(labels)):
        for d in range(len(labels[v])):
            if(boxs[v][d+hidey] == 0):
                Myimg = Myimgs[9]
            if(boxs[v][d+hidey] > 0):
                Myimg = Myimgs[8]
            labels[v][d].config(image=Myimg)
    root.after_cancel(id)

    if(maxScore < score):
        datalist[2] = "maxScore,"+str(score)+",\n"
    f = open('config.txt', 'w')
    f.writelines(datalist)
    f.close()


def enemyLine():
    for v in range(lengthY-hidey-1):
        chaos = hidey+v
        for d in range(lengthX):
            num = boxs[d][chaos+1]
            boxs[d][chaos] = num
    for d in range(lengthX):
        boxs[d][lengthY-1] = 20
    global lastHole
    d = randrange(lengthX)
    duplicate = randrange(0, 10)
    if(duplicate >= 3):
        d = lastHole
    lastHole = d
    boxs[d][lengthY-1] = 0


def enemyAttack():
    global enemyBlock
    enemy = enemyBlock
    num = randrange(0, 10)
    li = randrange(1, 5)
    if(num > 4):
        enemyBlock = enemy+li
    label_enemy.config(text=str(enemyBlock))


def enemyPop(li):
    global enemyBlock, lastHole
    if(enemyBlock == 0):
        lastHole = 0
    if(li == 0):
        if(enemyBlock > 0):
            enemyLine()
            enemyBlock -= 1
    elif(li > 0):
        num = enemyBlock-li
        if num < 0:
            num = 0
        enemyBlock = num


def ref():
    global id
    deletePiece(nowShape, x, y)
    deleteGhost()
    line = 0
    check = onPiece(nowShape, x, y+1)
    if(check == 1):
        setGhost(nowShape, x, y)
        if (noDrop == 0):
            move(nowShape, x, y, 2)
        showPiece(nowShape, x, y)
    elif(check <= -1):
        showPiece(nowShape, x, y)
        if(y < hidey):
            if(-1 >= onPiece(nowShape, x, y)):
                gameover()
                return
        line = checkLine()
        if(enemy_on):
            enemyPop(line)
        pushPiece()
    showgame()
    dropLine(line)
    id = root.after(speed, ref)


def showkeep(m, mox, moy):
    deleteGhost
    deletePiece(m, mox, moy)
    global keepShape
    num = keepShape
    keepShape = m
    for v in range(len(keepbox)):
        for d in range(len(keepbox[v])):
            keepbox[v][d] = 0
    for i in shapes[keepShape]:
        shapex = i[0]
        shapey = i[1]
        keepbox[shapex][shapey] = keepShape
        if(keepUse == 1):
            keepbox[shapex][shapey] = 25
    global x, y
    x = 4
    y = 0
    global nowShape
    if(num == 0):
        pushPiece()
        return
    nowShape = num


def Key(e):
    tex = e.char
    global id, stop, noDrop, defaultSpeed, noKey, speed
    if(stop == 0):
        if(noKey == 0):
            if e.char == "a":
                tex = "a or A"
                noDrop = 1
                move(nowShape, x, y, 4)
            elif e.char == "s":
                tex = "s or S"
                move(nowShape, x, y, 2)
            elif e.char == "d":
                tex = "d or D"
                noDrop = 1
                move(nowShape, x, y, 6)
            elif e.char == "w":
                tex = "w or W"
                noDrop = 1
                deletePiece(nowShape, x, y)
                change(nowShape)
            elif e.char == "t":
                tex = "t or T"
                noDrop = 1
                noKey = 1
                for i in range(lengthY-hidey):
                    deletePiece(nowShape, x, y)
                    num = onPiece(nowShape, x, y)
                    if(num == 1):
                        move(nowShape, x, y, 2)
                    elif(num <= -1):
                        showPiece(nowShape, x, y)
                        break
            elif e.char == "q":
                tex = "q or Q"
                global keepUse
                if(keepUse == 0):
                    keepUse = 1
                    showkeep(nowShape, x, y)
    if e.char == "n":
        tex = "n or N"
        newGame()
    elif e.char == "p":
        if stop == 0:
            root.after_cancel(id)
            stop = 1
            tex = "stop"
        elif stop == 1:
            id = root.after(speed, ref)
            stop = 0
            tex = "restart"
    elif e.char == "1":
        enemyAttack()
        tex = "enemy_attack"
    label_key.config(text=tex)
    noDrop = 0
    if(noKey == 0):
        deleteGhost()
        deletePiece(nowShape, x, y)
        setGhost(nowShape, x, y)
        showPiece(nowShape, x, y)
        showgame()


if __name__ == '__main__':

    root.title("tetris")
    root.geometry("450x440")
    root.resizable(False, False)

    left_frame = ttk.Frame(root, padding=0, width=200,
                           height=400)

    Main_frame = ttk.Frame(root, padding=20, width=240,
                           height=440, relief="solid")

    right_frame = ttk.Frame(root, padding=0, width=200,
                            height=400)

    left_frame.pack(anchor="n", side="left")
    Main_frame.pack(anchor="n", side="left")
    right_frame.pack(anchor="n", side="left")

    keep_frame = ttk.Frame(left_frame, padding=10, width=105,
                           height=100, relief='solid')
    tutorial_frame = ttk.Frame(left_frame, padding=10, width=105,
                               height=350, relief='solid')
    keep_frame.pack(anchor="w", side="top")
    tutorial_frame.pack(anchor="s", side="top")

    labelK = ttk.Label(
        tutorial_frame, text="A,D: 左右移動\nW: 回転\nT: 落下\nQ: ホールド\nN: New Game   \nP: 停止/解除\n1: お邪魔攻撃")
    labelK.pack(side="bottom")

    enemy_frame = ttk.Frame(left_frame, padding=10, width=200,
                            height=100, relief='solid')
    enemy_frame.pack(anchor="w", side="top")
    label2 = ttk.Label(enemy_frame, text="  お邪魔ブロック  ")
    label2.pack(side="top")
    label_enemy = ttk.Label(enemy_frame, text="0")
    label_enemy.pack(side="bottom")

    next_frame = ttk.Frame(right_frame, padding=10, width=105,
                           height=100, relief='solid')
    next2_frame = ttk.Frame(right_frame, padding=10, width=105,
                            height=100, relief='solid')
    bottom_frame = ttk.Frame(right_frame, padding=10, width=200,
                             height=100, relief='solid')
    score_frame = ttk.Frame(right_frame, padding=10, width=200,
                            height=100, relief='solid')
    next_frame.pack(anchor="w", side="top")
    next2_frame.pack(anchor="w", side="top")
    score_frame.pack(anchor="w", side="bottom")
    bottom_frame.pack(anchor="w", side="bottom")

    label2 = ttk.Label(bottom_frame, text="---入力したキー--")
    label_key = ttk.Label(bottom_frame, text="")
    label_key.pack(side="bottom")
    label2.pack(side="top")

    label_level = ttk.Label(score_frame, text="Level:1")
    label_level.pack(side="top")
    label_speed = ttk.Label(score_frame, text="")
    label_speed.pack(side="top")
    label3 = ttk.Label(score_frame, text="------score-----")
    label_score = ttk.Label(score_frame, text=str(score))
    label3.pack(side="top")
    label_score.pack(side="top")

    label3 = ttk.Label(score_frame, text="----highscore---")
    label_maxScore = ttk.Label(score_frame, text="")
    label3.pack(side="top")
    label_maxScore.pack(side="top")

    root.bind("<Key>", Key)
    create()
    newGame()
    label_speed.config(text="Speed:"+str(speed))

    root.mainloop()
