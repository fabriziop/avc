#!/usr/bin/python


from Tkinter import * 			# Tk interface

root = Tk()
root.title('AVC Tk showcase example')

button1 = Button(root,text='button',name='boolean1__button1')
button1.grid(row=1,column=1,columnspan=3)
print button1.cget('state')
mainloop()			# run Tk event loop until quit

#### END

