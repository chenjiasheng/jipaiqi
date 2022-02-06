from tkinter import *
from jipaiqi import CARDS, CARD_NUMS
COL_NAMES = [''] + CARDS
COL_NAMES[COL_NAMES.index('Joker')] = '王'

ROWS = 5
COLS = len(CARDS) + 1

rows = []
for i in range(ROWS):
    cols = []
    for j in range(COLS):
        e = Entry(relief=GROOVE,
                  width=4,
                  font="Helvetica 22 bold",
                  justify="center",
                  bg="#1E6FBA",
                  fg="yellow",
                  disabledbackground="#1E6FBA",
                  disabledforeground="yellow",
                  highlightthickness=1,
                  bd=0)
        e.grid(row=i, column=j, sticky=NSEW)
        if i == 0:
            e.insert(END, COL_NAMES[j])
        elif i == ROWS - 1:
            if j == 0:
                e.insert(END, '剩余')
            else:
                e.insert(END, CARD_NUMS[j - 1])
        else:
            if j == 0:
                players = ['对家', '上家', '下家']
                e.insert(END, players[i - 1])

            else:
                e.insert(END, '0')
        e["state"] = DISABLED
        cols.append(e)
    rows.append(cols)


from jipaiqi import JiPaiQi
jipaiqi = JiPaiQi()
root = Tk()

def update_ui():
    for i in range(1, ROWS):
        for j in range(1, COLS):
            e = rows[i][j]
            e["state"] = NORMAL
            if i == ROWS - 1:
                e.delete(0, END)
                e.insert(END, jipaiqi.remain_cards[j-1])
            else:
                indices = [0, 1, 3]
                e.delete(0, END)
                e.insert(END, jipaiqi.out_cards[indices[i-1]][j-1])
            e["state"] = DISABLED
update_ui()

def task():
    has_update = jipaiqi.run()
    if has_update:
        update_ui()
    root.after(100, task)
root.after(100, task)

mainloop()