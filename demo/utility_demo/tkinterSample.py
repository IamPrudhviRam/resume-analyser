import tkinter as tk

root = tk.Tk()
#
# # setting the windows size
# root.geometry("600x400")
#
# # declaring string variable
# # for storing name and password
# name_var = tk.StringVar()
# passw_var = tk.StringVar()
#
#
# # defining a function that will
# # get the name and password and
# # print them on the screen
# def submit():
#     name = name_entry.get()
#     password = passw_var.get()
#
#     print("The name is : " + name)
#     print("The password is : " + password)
#
#     name_var.set("")
#     passw_var.set("")
#
#
# # creating a label for
# # name using widget Label
# name_label = tk.Label(root, text='Username',
#                       font=('calibre',
#                             10, 'bold'))
#
# # creating a entry for input
# # name using widget Entry
# name_entry = tk.Entry(root,
#                       textvariable=name_var, font = ('calibre', 10, 'normal'))
#
# # creating a label for password
# passw_label = tk.Label(root,
#                        text='Password',
#                        font=('calibre', 10, 'bold'))
#
# # creating a entry for password
# passw_entry = tk.Entry(root,
#                        textvariable=passw_var,
#                        font=('calibre', 10, 'normal'),
#                        show='*')
#
# # creating a button using the widget
# # Button that will call the submit function
# sub_btn = tk.Button(root, text='Submit',
#                     command=submit)
#
# # placing the label and entry in
# # the required position using grid
# # method
# name_label.grid(row=0, column=0)
# name_entry.grid(row=0, column=1)
# passw_label.grid(row=1, column=0)
# passw_entry.grid(row=1, column=1)
# sub_btn.grid(row=2, column=1)

# performing an infinite loop
# for the window to display
S = tk.Scrollbar(root)
T = tk.Text(root, height=3, width=50)
S.pack(side=tk.RIGHT, fill=tk.Y)
T.pack(side=tk.LEFT, fill=tk.Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = """HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished."""
T.insert(tk.END, quote)

root.mainloop()