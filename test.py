from tkinter import *
from tkmacosx import CircleButton

root = Tk()
B0 = CircleButton(root, text='Button')
B0.grid(row=0)
B1 = CircleButton(root, text='Button', bg='#ADEFD1',
            fg='#00203F', borderless=1)
B1.grid(row=0, column=1)
B2 = CircleButton(root, text='Button', bg='#E69A8D',
            fg='#5F4B8B', borderless=1,
            activebackground=('#AE0E36', '#D32E5E'),
            activeforeground='#E69A8D')
B2.grid(row=0, column=2)
root.mainloop()