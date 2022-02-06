from tkinter import Tk, CENTER, NO, Frame
from tkinter import ttk
card_names = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'Joker')

root = Tk()
root.title('PythonGuides')
root.geometry('1300x300')
root['bg'] = '#AC99F2'

frame = Frame(root)
frame.pack()
table = ttk.Treeview(frame)

keys = ('Player',) + card_names
table['columns'] = keys
table.column("#0", width=0, stretch=NO)
table.column("Player", anchor=CENTER, width=80)
for k in keys:
    table.column(k, anchor=CENTER, width=80)
table.heading("#0", text="", anchor=CENTER)
for k in keys:
    table.heading(k, text=k, anchor=CENTER)

table.insert(parent='', index='end', iid=0, text='', values =(0,) + (8,) * 14)
table.pack()


def task():
    print("hello")
    root.after(2000, task)  # reschedule event in 2 seconds

root.after(2000, task)

root.mainloop()