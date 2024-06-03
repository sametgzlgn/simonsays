import tkinter as tk
import ttkbootstrap as ttk
import random
import threading
import time
import sys
import simpleaudio as sa
from ttkbootstrap.constants import *
from PIL import Image,ImageTk
from tkinter.messagebox import showinfo

kombo = 0
can = 3
buton_bilgileri = [[Image.open("res/img/kirmizi.png"),Image.open("res/img/kirmizi-glow.png"),sa.WaveObject.from_wave_file("res/snd/do.wav")],
                   [Image.open("res/img/sari.png"),Image.open("res/img/sari-glow.png"),sa.WaveObject.from_wave_file("res/snd/re.wav")],
                   [Image.open("res/img/mavi.png"),Image.open("res/img/mavi-glow.png"),sa.WaveObject.from_wave_file("res/snd/mi.wav")],
                   [Image.open("res/img/yesil.png"),Image.open("res/img/yesil-glow.png"),sa.WaveObject.from_wave_file("res/snd/fa.wav")]
                   ]
anahtarlar = {0:buton_bilgileri[0],1:buton_bilgileri[1],2:buton_bilgileri[2],3:buton_bilgileri[3]}
sekans = []
cevaplar = []
cevap_sirasi = False
YANLIS = sa.WaveObject.from_wave_file("res/snd/yanlis.wav")

def sekans_olustur():
    global sekans
    eklenecek_sayi = random.randint(0,len(buton_bilgileri) - 1)
    sekans.append(eklenecek_sayi)

def sekans_baslat():
    global cevaplar,cevap_sirasi,kombo,durum
    if can == 0:
        sys.exit()
    durum["text"] = "Bekleyin."
    cevap_sirasi = False
    cevaplar = []
    kombo = 0
    for i in sekans:
        glow = ImageTk.PhotoImage(anahtarlar[i][1])
        normal = ImageTk.PhotoImage(anahtarlar[i][0])
        labellar[i].image = glow
        labellar[i]["image"] = glow
        anahtarlar[i][2].play()
        time.sleep(1)
        labellar[i].image = normal
        labellar[i]["image"] = normal
        time.sleep(0.3)
    cevap_sirasi = True
    durum["text"] = "Sıra sizde."
def kontrol(snyl):
    global cevaplar,sekans,cevap_sirasi,kombo,can,durum,can_lbl
    if can == 0:
        sys.exit()
    if cevap_sirasi:
        durum["text"] = "Sıra sizde."
        cevaplar.append(snyl)
    anahtarlar[cevaplar[len(cevaplar) - 1]][2].play()
    if sekans[:len(cevaplar)] == cevaplar:
        kombo += 1
    else:
        YANLIS.play()
        time.sleep(1)
        can -= 1
        cevap_sirasi = False
        threading.Thread(target=sekans_baslat).start()
    if kombo == len(sekans) and cevap_sirasi:
        sekans_olustur()
        time.sleep(1)
        threading.Thread(target=sekans_baslat).start()
    can_lbl["text"] = "Can: {}".format(can)

def yardim(event=None):
    showinfo("Simon Says","Gösterilen sekansı ezberleyip yön tuşları ile tekrar etmeye çalışın. Her doğru tekrarlamada sekans bir artarak devam eder. 3 defa yanlış yapmanız halinde oyun biter.")

pencere = tk.Tk()
width,height = round(pencere.winfo_screenwidth() * 0.7),round(pencere.winfo_screenheight() * 0.7)
pencere.title("Simon Says")
pencere.geometry("{}x{}".format(width,height))
mavi_lbl_tk = ImageTk.PhotoImage(buton_bilgileri[2][0])
yesil_lbl_tk = ImageTk.PhotoImage(buton_bilgileri[3][0])
kirmizi_lbl_tk = ImageTk.PhotoImage(buton_bilgileri[0][0])
sari_lbl_tk = ImageTk.PhotoImage(buton_bilgileri[1][0])
lbl_mavi = ttk.Label(image=mavi_lbl_tk)
lbl_mavi.pack(side=TOP,pady=15)
lbl_yesil = ttk.Label(image=yesil_lbl_tk)
lbl_yesil.pack(side=BOTTOM,pady=20)
lbl_kirmizi = ttk.Label(image=kirmizi_lbl_tk)
lbl_kirmizi.pack(side=LEFT,padx=20)
lbl_sari = ttk.Label(image=sari_lbl_tk)
lbl_sari.pack(side=RIGHT,padx=15)
labellar = {0:lbl_kirmizi,1:lbl_sari,2:lbl_mavi,3:lbl_yesil}
durum = ttk.Label(text="Bekleyin...",font="Arial 15 bold")
durum.place(x=round(width * 0.5) - 50,y=round(height * 0.5))
can_lbl = ttk.Label(text="Can: {}".format(can))
can_lbl.place(x=round(width * 0.9),y=round(height * 0.01))
sekans_olustur()
threading.Thread(target=sekans_baslat).start()

pencere.bind("<Left>",lambda event:kontrol(0))
pencere.bind("<Up>",lambda event:kontrol(2))
pencere.bind("<Right>",lambda event:kontrol(1))
pencere.bind("<Down>",lambda event:kontrol(3))
pencere.bind("<c>",lambda event:sys.exit())
pencere.bind("<h>",yardim)

pencere.mainloop()
