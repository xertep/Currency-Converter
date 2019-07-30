#! /usr/bin/env python

from tkinter import *
from tkinter import scrolledtext
import tkinter.ttk as ttk

root = Tk()
root.title("Currency Converter")

root.geometry("250x700+1500+50")

try:
    root.iconbitmap('currency.ico')
except:
    pass


statusbar = Label(root, text="Created by Peter Hruška", bd=1, relief=SUNKEN, anchor=W, padx=5)
statusbar.pack(side=BOTTOM, fill=X)

#photoHruska = PhotoImage(file='O:\\Hruska\\Python\\pearBW_mini.png')
#obrazokHruska = Label(root, image=photoHruska, anchor=E)
#obrazokHruska.pack(side=BOTTOM, fill=X)

topbar = Label(root, text="Exchange Rates", bd=1, relief=FLAT, anchor=W, padx=5)
topbar.config(justify=LEFT)
topbar.config(font=("Arial black", 16))
topbar.pack(side=TOP, fill=X)

gridokno = Frame(root)
gridokno.pack(side=TOP, fill=BOTH, expand=True)



import requests

stranka = "https://api.exchangeratesapi.io/latest"
stranka_api = requests.get(stranka)


exchange_rates = (stranka_api.json())["rates"]
meny_vsetky = []
for k in exchange_rates:
    if k not in ["CZK", "EUR", "USD"]:
        meny_vsetky.append(k)
meny_vsetky.sort()
meny_vsetky.insert(0, "USD")
meny_vsetky.insert(0, "EUR")
meny_vsetky.insert(0, "CZK")


label_mnozstvo = Label(gridokno, text="Množstvo: ")
label_mnozstvo.grid(row=0, column=0, sticky=W, padx=5)

label_meny = Label(gridokno, text="Mena: ")
label_meny.grid(row=0, column=0, sticky=W, padx=150)

entry_mnozstvo = Entry(gridokno)
entry_mnozstvo.grid(row=1, column=0, sticky=W, padx=5)
entry_mnozstvo.focus()


mn = StringVar(gridokno)
mn.set('CZK')

combo_meny = ttk.Combobox(gridokno, textvariable=mn, values=meny_vsetky)
combo_meny.config(width=6)
combo_meny.grid(row=1, column=0, columnspan=1, sticky=W, padx=150)


text_1 = scrolledtext.ScrolledText(gridokno, width=25, height=34, borderwidth=2)
text_1.grid(row=3, column=0, rowspan=1, columnspan=1, padx=5, pady=6, sticky=N+W)


def convert(event=None):
    text_1.delete(1.0,END)
    
    if entry_mnozstvo.get() != "":
        mnozstvo = float(entry_mnozstvo.get())
    else:
        mnozstvo = 0
    mena = str(mn.get())

    if mena == "EUR":
        text_1.insert(END, "EUR: " + str('{0:,.2f}'.format(mnozstvo).replace(",", " ").replace(".", ",")) + "\n")
        for m in meny_vsetky:
            if m != "EUR":
                text_1.insert(END, m + ": " + str('{0:,.2f}'.format(float(exchange_rates[m]) * (mnozstvo)).replace(",", " ").replace(".", ",")) + "\n")
                text_1.tag_add("grey", "4.0", END)
                text_1.tag_config("grey", foreground="darkgrey")
    else:
        text_1.insert(END, "EUR: " + str('{0:,.2f}'.format(mnozstvo * (1 / float(exchange_rates[mena]))).replace(",", " ").replace(".", ",")) + "\n")
        for m in meny_vsetky:
            if m != "EUR":
                text_1.insert(END, m + ": " + str('{0:,.2f}'.format(float(exchange_rates[m]) * (mnozstvo * (1 / float(exchange_rates[mena])))).replace(",", " ").replace(".", ",")) + "\n")
                text_1.tag_add("grey", "4.0", END)
                text_1.tag_config("grey", foreground="darkgrey")

root.bind('<Return>', convert)
        

#robButton = Button(gridokno, text="Convert", width=28, command=lambda: (text_1.delete(1.0,END),convert()))
robButton = Button(gridokno, text="Convert", width=28, command=convert)
robButton.grid(row=2, column=0, sticky=W, padx=5, pady=5)

root.mainloop()



