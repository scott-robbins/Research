import tkinter as tk
import tkMessageBox
import backend

HEIGHT = 650
WIDTH = 800


def mode(cmd, node, b):
    if cmd == 'quit':
        tkMessageBox.showinfo("COMMAND", "** Exiting!! **")
        exit(0)
    b.delete(0, 'end')

    print 'Executing < ' + cmd + ' >'
    uname, pword = backend.get_creds(node)
    reply = backend.ssh_command(node,uname,pword,cmd,True)
    data = uname+'@'+node+':~$' + reply
    text = tk.Text(commands)
    text.insert(tk.INSERT, data)
    text.insert(tk.END, '\n')
    text.pack()

    return data


NODES = backend.NODES
local, peers = backend.initialize(NODES)

root = tk.Tk()
# APPLICATION
canvas = tk.Canvas(root, height=HEIGHT,width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='bg.png')
background_label = tk.Label(root,image=background_image)
background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff')  # Nicer Colors
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

# Use lambda for button press
# command=Lambda: function(entry.get())

window = tk.Frame(root, bg='#ec5151', bd=3)
window.place(x=WIDTH/2, y=HEIGHT/14, relx=0.1, rely=0.1, relwidth=0.275, relheight=0.5)

commands = tk.Label(window,font=('Courier', 10))
commands.place(relwidth=1,relheight=1)

# List Box:
Lb1 = tk.Listbox(root,highlightcolor='yellow')
Lb1.insert(1, "Reboot")
Lb1.insert(2, "Connect")
Lb1.insert(3, "Query")
Lb1.insert(4, "Command")
Lb1.insert(5, "Disconnect")
Lb1.insert(6, "Quit")
Lb1.place(x=WIDTH/9,y=HEIGHT/2,relwidth=0.2,relheight=0.3)

label = tk.Label(frame, text='Command Window', bg='#ec5151')
label.grid(row=0, column=2, padx=WIDTH/5)

i = 0
for peer in peers:
    B = tk.Button(frame, text=peer, command=lambda: mode(e.get(), peer, e), bg='gray')
    B.grid(row=i, column=0)
    e = tk.Entry(frame, font=12, bd=1)
    e.grid(row=i, column=1)
    i += 1

# B1 = tk.Button(frame, text="NODE 1", command=lambda: mode0(e1.get(),e1), bg='gray')
# B1.grid(row=0, column=0)
#
# B2 = tk.Button(frame, text="NODE 2", command=lambda: mode1(e2.get(),e2), bg='gray')
# B2.grid(row=1, column=0)
#
# e1 = tk.Entry(frame, font=12, bd=1)
# e1.grid(row=0, column=1)
#
# e2 = tk.Entry(frame, font=12, bd=1)
# e2.grid(row=1, column=1)

root.mainloop()
# EOF

