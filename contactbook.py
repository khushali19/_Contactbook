from tkinter  import *
from tkinter import ttk

import sqlite3



conn = sqlite3.connect('contactdb.sqlite')
cur = conn.cursor()

#Make some fresh tables using executescript()
cur.executescript('''
DROP TABLE IF EXISTS Contacts;

CREATE TABLE Contacts (
     id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
     fname    TEXT UNIQUE,
     lname    TEXT,
     ph_no  TEXT UNIQUE,
     email   TEXT UNIQUE
);

''')


class Sample(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        Frame.pack(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
        
class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        Label(self, text="!! WELCOME TO CONTACT BOOK !!", pady=30, font="Arial").grid(row=0, column=10)
        vi =  Button(self, text="View Contact list ", padx=84, bg="#7e1be4", fg="black", pady=30, font="Arial", activebackground="#ccbc9b", command=lambda: master.switch_frame(ViewPage))
        vi.grid(row=50, column=10)
        
        ins = Button(self, text="Insert Contact ", padx=84, pady=30, bg="#b54a71", fg="black", font="Arial", activebackground="#ccbc9b", command=lambda: master.switch_frame(InsertPage))
        ins.grid(row=100, column=10)
        
        dele = Button(self, text="Delete Contact ", padx=84, pady=30, bg="#7e1be4", fg="black", font="Arial", activebackground="#ccbc9b", command=lambda: master.switch_frame(DeletePage))
        dele.grid(row=150, column=10)
        
        quitbt = Button(self, text="Click here to QUIT !! ", padx=84, pady=30, bg="#ccbc9b", fg="black", font="Arial", activebackground="#ccbc9b", command=self.quit)
        quitbt.grid(row=200, column=10)

    
        

class ViewPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        
        sqlstr = "SELECT * FROM Contacts"
        cur.execute(sqlstr)
        rows = cur.fetchall()
        
        
        frm = Frame(self)
        frm.grid(row=10, column=0)
        tv = ttk.Treeview(frm, column=(1, 2, 3, 4, 5), show="headings", height="10")
        tv.pack()
        
        tv.heading(1, text="Id")
        tv.heading(2, text="First Name")
        tv.heading(3, text="Last Name")
        tv.heading(4, text="Phone Number")
        tv.heading(5, text="Email Id")
        
        for i in rows:
            tv.insert("", 'end', values=i)
            
        
        Button(self, text="Go to Main Menu ", padx=20, pady=20, bg="#ca9735", fg="black", font="Arial", activebackground="#ccbc9b", command=lambda: master.switch_frame(StartPage)).grid(row=100, column=0)
        
        


class InsertPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        first = StringVar()
        last = StringVar()
        phno = StringVar()
        
        mail = StringVar()
        status = StringVar()
        
        Label(self, text="Enter the First Name : ").grid(row=0, column=10)
        fna = Entry(self, textvariable=first, width=50, borderwidth=10, bg="#ccbc9b")
        fna.grid(row=1, column=10, columnspan=5)
        
        Label(self, text="Enter the Last Name : ").grid(row=50, column=10)
        lna = Entry(self, textvariable=last, width=50, borderwidth=10, bg="#ccbc9b")
        lna.grid(row=51, column=10, columnspan=5)
        
        Label(self, text="Enter the mobile number : ").grid(row=100, column=10)
        no = Entry(self, textvariable=phno, width=50, borderwidth=10, bg="#ccbc9b")
        no.grid(row=101, column=10, columnspan=5)
        
        
        Label(self, text="Enter the email address : ").grid(row=150, column=10)
        em = Entry(self, textvariable=mail, width=50, borderwidth=10, bg="#ccbc9b")
        em.grid(row=151, column=10, columnspan=5)
        
        Label(self, text='', textvariable=status, pady=20, padx=20, font="Arial").grid(row=170, column=10)
        
        def myins():
            
            cur.execute("INSERT INTO Contacts (fname, lname, ph_no, email) VALUES ('%s', '%s', '%s', '%s')"%(first.get(), last.get(), phno.get(), mail.get()))
            conn.commit()
            status.set("Contact added successfully :) ")
            
                  
        Button(self, text="Add Contact ", padx=20, pady=20, bg="#9f97c9", fg="black", font="Arial", activebackground="#ccbc9b", command=myins).grid(row=160, column=10)
        Button(self, text="Go to Main Menu ", padx=20, pady=20, bg="#ca9735", fg="black", font="Arial", activebackground="#ccbc9b", command=lambda: master.switch_frame(StartPage)).grid(row=160, column=11)
        
        
class DeletePage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        delfna = StringVar()
        dellna = StringVar()
        stats = StringVar()
        
        Label(self, text="Enter the First Name : ").grid(row=0, column=10)
        fna = Entry(self, textvariable=delfna, width=50, borderwidth=10, bg="#ccbc9b")
        fna.grid(row=1, column=10, columnspan=5)
       
        Label(self, text="Enter the Last Name : ").grid(row=50, column=10)
        fna = Entry(self, textvariable=dellna, width=50, borderwidth=10, bg="#ccbc9b")
        fna.grid(row=51, column=10, columnspan=5)
        
        Label(self, text='', textvariable=stats, pady=20, padx=20, font="Arial").grid(row=110, column=10)
        
        
        def mydele():
            
            cur.execute("DELETE FROM Contacts where fname='%s'"%(delfna.get()))
            conn.commit()
            stats.set("Contact deleted successfully :| ")
            
        Button(self, text="Delete Contact ", padx=20, pady=20, bg="#9f97c9", fg="black", font="Arial", activebackground="#ccbc9b", command=mydele).grid(row=100, column=10)
        Button(self, text="Go to Main Menu ", padx=20, pady=20, bg="#ca9735", fg="black", font="Arial", activebackground="#ccbc9b", command=lambda: master.switch_frame(StartPage)).grid(row=100, column=11)
        
       
       
        
if __name__ == "__main__":
    root = Tk()
    root.title("Contact Book")
    root.geometry("1000x500")
    app = Sample(root)
    root.mainloop()

conn.close()
