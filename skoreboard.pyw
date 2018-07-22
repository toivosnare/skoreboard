'''
Skoreboard
Toivo Snåre
20.2.2018
'''

from time import time, sleep
from datetime import datetime
from threading import Thread
from tkinter import *
from os import system
from PIL import ImageTk

class Kello(Thread):
    def __init__(self, f, mins, secs):
        Thread.__init__(self)
        self.t = 1 / f
        self.mins = mins
        self.secs = secs
        self.aika = 60 * mins.get() + secs.get()
        self.stopped = True
        self.quit = False

    def run(self):
        while not self.quit:
            viime = time()
            while not self.stopped:
                nyt = time()
                delta = nyt - viime
                viime = nyt
                self.aika -= delta
                if self.aika <= 0:
                    self.aika = 0
                    self.stop_()
                mins, secs = divmod(self.aika, 60)
                self.mins.set(int(mins))
                self.secs.set(int(secs))
                with open("Aika.txt", "w") as f:
                    f.write(str("%02d" % int(mins)) + ":" + str("%02d" % int(secs)))
                sleep(self.t)
            sleep(self.t)

    def start_(self):
        self.stopped = False
        ikkuna.title("Skoreboard - start")
        button_vaihto.config(image=pause)
        button_vaihto.image = pause


    def stop_(self):
        self.stopped = True
        ikkuna.title("Skoreboard - stop (" + str(self.aika) + ")")
        print(self.aika)
        button_vaihto.config(image=play)
        button_vaihto.image = play

def lopeta():
    print("lopetetaan")
    kello.stop_()
    kello.quit = True
    kello.join()
    ikkuna.title("Skoreboard - lopetetaan")
    ikkuna.destroy()

def tallenna():
    if kello.stopped:
        kello.aika = 60 * aika_min.get() + aika_sec.get()
    # print(kello.aika)
    muuttujat = [[nimi_A.get(), "Joukkue A"],
                 [lyh_A.get(), "Lyhenne A"],
                 [pisteet_A.get(), "Pisteet A"],
                 [nimi_B.get(), "Joukkue B"],
                 [lyh_B.get(),"Lyhenne B"],
                 [pisteet_B.get(), "Pisteet B"],
                 [jakso.get(), "Jakso"],
                 [str("%02d" % aika_min.get()) + ":" + str("%02d" % aika_sec.get()), "Aika"]]
    for m in muuttujat:
        with open(m[1] + ".txt", "w") as f:
            f.write(str(m[0]))
    ikkuna.title("Skoreboard - tallennettu (" + str(datetime.fromtimestamp(time()).strftime('%H:%M:%S')) + ")")
    print("tallennettu")

def vaihda():
    if kello.stopped:
        kello.start_()
    else:
        kello.stop_()

def reset():
    nimi_A.set("Joukkue A")
    lyh_A.set("JOA")
    pisteet_A.set(0)
    nimi_B.set("Joukkue B")
    lyh_B.set("JOB")
    pisteet_B.set(0)
    jakso.set(1)
    aika_min.set(10)
    aika_sec.set(0)
    kello.stop_()
    kello.aika = 60 * aika_min.get() + aika_sec.get()
    ikkuna.title("Skoreboard")
    print("reset")

# Muuttujat
versio = "v1.0.7"
ikkuna = Tk()
nimi_A = StringVar()
lyh_A = StringVar()
pisteet_A = IntVar()
nimi_B = StringVar()
lyh_B = StringVar()
pisteet_B = IntVar()
jakso = IntVar()
aika_min = IntVar()
aika_sec = IntVar()
kello = Kello(5, aika_min, aika_sec)
pause = ImageTk.PhotoImage(file="pause.png")
play = ImageTk.PhotoImage(file="play.png")
bg1 = 'gray32'
bg2 = 'gray20'
fg1 = 'gray80'
fg2 = 'LightBlue3'
bd = 1
bbg = 'gray48'
font1 = 'Arial 22'
font2 = 'Arial 8'

#Binds
ikkuna.bind("<F1>", lambda e: pisteet_A.set(pisteet_A.get() + 1))
ikkuna.bind("<F2>", lambda e: pisteet_A.set(pisteet_A.get() + 2))
ikkuna.bind("<F3>", lambda e: pisteet_A.set(pisteet_A.get() + 3))
ikkuna.bind("<F4>", lambda e: pisteet_A.set(pisteet_A.get() - 1))
ikkuna.bind("<F5>", lambda e: pisteet_B.set(pisteet_B.get() + 1))
ikkuna.bind("<F6>", lambda e: pisteet_B.set(pisteet_B.get() + 2))
ikkuna.bind("<F7>", lambda e: pisteet_B.set(pisteet_B.get() + 3))
ikkuna.bind("<F8>", lambda e: pisteet_B.set(pisteet_B.get() - 1))
ikkuna.bind("<F11>", lambda e: kello.start_())
ikkuna.bind("<F12>", lambda e: kello.stop_())
ikkuna.bind("<Return>", lambda e: tallenna())
ikkuna.bind("<space>", lambda e: vaihda())
ikkuna.bind("<Control-BackSpace>", lambda e: reset())

# Widgetit
entry_nimi_A = Entry(ikkuna, width=15, textvariable=nimi_A, font=font1, bg=bg2, fg=fg1, bd=bd)
entry_lyh_A = Entry(ikkuna, width=4, textvariable=lyh_A, font=font1, bg=bg2, fg=fg1, bd=bd)
spinbox_pisteet_A = Spinbox(ikkuna, from_=0, to=999, width=4, textvariable=pisteet_A, font="Arial 22", bg=bg2, fg=fg1, bd=bd, buttonbackground=bbg)
entry_nimi_B = Entry(ikkuna, width=15, textvariable=nimi_B, font=font1, bg=bg2, fg=fg1, bd=bd)
entry_lyh_B = Entry(ikkuna, width=4, textvariable=lyh_B, font=font1, bg=bg2, fg=fg1, bd=bd)
spinbox_pisteet_B = Spinbox(ikkuna, from_=0, to=999, width=4, textvariable=pisteet_B, font=font1, bg=bg2, fg=fg1, bd=bd, buttonbackground=bbg)
spinbox_jakso = Spinbox(ikkuna, from_=0, to=999, width=4, textvariable=jakso, font=font1, bg=bg2, fg=fg1, bd=bd, buttonbackground=bbg)
spibox_aika_min = Spinbox(ikkuna, from_=0, to=999, width=4, textvariable=aika_min, font=font1, bg=bg2, fg=fg1, bd=bd, buttonbackground=bbg)
spibox_aika_sec = Spinbox(ikkuna, from_=0, to=59, width=4, textvariable=aika_sec, font=font1, bg=bg2, fg=fg1, bd=bd, buttonbackground=bbg)
button_vaihto = Button(ikkuna, text="Pause/Play", command=vaihda, font=font1, bg=bg2, fg=fg1, bd=bd)
button_tallenna = Button(ikkuna, text="Tallenna", command=tallenna, font=font1, bg=bg2, fg=fg1, bd=bd)
label_pisteet_A = Label(ikkuna, text="F1-F4", font=font2, bg=bg1, fg=fg2, bd=bd)
label_pisteet_B = Label(ikkuna, text="F5-F8", font=font2, bg=bg1, fg=fg2, bd=bd)
label_aika = Label(ikkuna, text="Välilyönti", font=font2, bg=bg1, fg=fg2, bd=bd)
label_tallenna = Label(ikkuna, text="Enter", font=font2, bg=bg1, fg=fg2, bd=bd)
label_versio = Label(ikkuna, text=versio, font=font2, bg=bg1, fg=fg2, bd=bd)
label_jakso = Label(ikkuna, text="Jakso", font=font2, bg=bg1, fg=fg2, bd=bd)
label_aika_min = Label(ikkuna, text="min", font=font2, bg=bg1, fg=fg2, bd=bd)
label_aika_sec = Label(ikkuna, text="sec", font=font2, bg=bg1, fg=fg2, bd=bd)

# Asettelu ruudukkoon
entry_nimi_A.grid(column=0, row=0, columnspan=2, sticky="SE", padx=20, pady=(20, 0))
entry_lyh_A.grid(column=0, row=1, sticky="NE")
spinbox_pisteet_A.grid(column=1, row=1, sticky="NW")
entry_nimi_B.grid(column=2, row=0, columnspan=2, sticky="SW", padx=20, pady=(20, 0))
entry_lyh_B.grid(column=2, row=1, sticky="NE")
spinbox_pisteet_B.grid(column=3, row=1, sticky="NW")
spinbox_jakso.grid(column=0, row=4, sticky="SW", padx=(20, 0))
spibox_aika_min.grid(column=1, row=4, sticky="SE")
spibox_aika_sec.grid(column=2, row=4, sticky="SW")
button_vaihto.grid(column=1, row=6, columnspan=2, sticky="N", ipadx=50, ipady=15)
button_tallenna.grid(column=3, row=6, sticky="NE", padx=(0, 20), pady=(0, 20))
label_pisteet_A.grid(column=1, row=2, sticky="NW", padx=(20, 0), pady=(0, 10))
label_pisteet_B.grid(column=3, row=2, sticky="NW", padx=(20, 0), pady=(0, 10))
label_aika.grid(column=1, row=5, columnspan=2, sticky="S", padx=(25, 30))
label_tallenna.grid(column=3, row=5, sticky="S", padx=(0, 0))
label_versio.grid(column=0, row=6, sticky="SW")
label_jakso.grid(column=0, row=3, sticky="SW", padx=(20, 0))
label_aika_min.grid(column=1, row=3, sticky="SE", padx=(0,68))
label_aika_sec.grid(column=2, row=3, sticky="SW")

ikkuna.protocol("WM_DELETE_WINDOW", lopeta)
ikkuna.resizable(False, False)
ikkuna.configure(background=bg1)
reset()
kello.start()
ikkuna.mainloop()
