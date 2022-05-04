
from datetime import date, datetime
from random import randint
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.mode.chained_assignment = None  

fiyat_serisi=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
fiyat_sats_usd = fiyat_serisi[-1]

oyuncu_listesi = []
talimat_listesi=[] 
talimat_tahtasi_sats_satis=[]
talimat_tahtasi_sats_alis=[]

class Oyuncu: 
    def __init__(self, name, usd_bakiye=1, sats_bakiye=1, niyet=0, karakter=0, riskrate=1, vizyon=1): 
        self.name = str(name)
        self.usd_bakiye = usd_bakiye
        self.sats_bakiye = sats_bakiye
        self.niyet = niyet  
        karakter = randint(-1,1)
        if karakter==0 : karakter = randint(-1,1)
        if karakter==0 : karakter = randint(-1,1)
        self.karakter=karakter                      
        riskrate = randint(1,10)
        self.riskrate=riskrate
        vizyon = randint(1,15)
        self.vizyon=vizyon
        oyuncu_listesi.append(self.name)  


    def to_dict(self):        
        return {
            'oyuncu_isim':  self.name,
            'oyuncu_usd_bakiye':  self.usd_bakiye,
            'oyuncu_sats_bakiye':  self.sats_bakiye,
            'oyuncu_niyet': self.niyet,
            'oyuncu_karakter': self.karakter,
            'oyuncu_riskrate': self.riskrate, 
            'oyuncu_vizyon': self.vizyon 
        } 

    def sats_bakiye_artir(self,miktar):
        self.sats_bakiye = self.sats_bakiye + miktar
    def usd_bakiye_artir(self,miktar):
        self.usd_bakiye = self.usd_bakiye + miktar
    def sats_bakiye_azalt(self,miktar):
        self.sats_bakiye = self.sats_bakiye - miktar
    def usd_bakiye_azalt(self,miktar):
        self.usd_bakiye = self.usd_bakiye - miktar

    def egilim_degistir(self, egilim=0):
        self.niyet=self.niyet + egilim*self.karakter

    def analiz_et(self):
        
        if (fiyat_serisi[-1] > fiyat_serisi[-1-self.vizyon]):
            self.egilim_degistir(1)
            # print(str(self.name) + " eğilimim " + str(self.niyet) +" alırım")
        
        else:
            self.egilim_degistir(-1)
            # print(str(self.name) + " eğilimim " + str(self.niyet) +" satarım")

    def islem_yap(self):

        tlmt_counter = len(talimat_listesi)+1      

        if (self.niyet >1 ): 
            globals() [f"tlmt{tlmt_counter}"] = Talimat(talimat_id = f"tlmt{tlmt_counter}", talimat_sahibi=self.name, talimat_mali= "sats_alis" , talimat_miktari=(10*self.riskrate), talimat_fiyati=(fiyat_serisi[-1]+self.niyet)) 
            

        elif (self.niyet<-1):
            globals() [f"tlmt{tlmt_counter}"] = Talimat(talimat_id = f"tlmt{tlmt_counter}", talimat_sahibi=self.name, talimat_mali= "sats_satis" , talimat_miktari=(10*self.riskrate), talimat_fiyati=(fiyat_serisi[-1]+self.niyet))  
            
        
        tahta_guncelleme()





def oyuncu_listele():
    global oyuncu_tahtasi 
    oyuncu_tahtasi=pd.DataFrame.from_records([globals() [oyuncu].to_dict() for oyuncu in oyuncu_listesi]) 
    print("******************* Oyuncu Tahtasi *******************")
    print(oyuncu_tahtasi)
    
def tahta_guncelleme():
    global talimat_tahtasi_sats_satis, talimat_tahtasi_sats_alis, talimat_listesi

    talimat_tahtasi=pd.DataFrame.from_records([globals() [talimat].to_dict() for talimat in talimat_listesi])    
    talimat_tahtasi=talimat_tahtasi[talimat_tahtasi.talimat_aktif_flag==True]

    talimat_tahtasi_sats_satis = talimat_tahtasi[talimat_tahtasi.talimat_mali=="sats_satis"]
    talimat_tahtasi_sats_satis.sort_values( ["talimat_fiyati", "talimat_zamani"], inplace=True, ignore_index=True, ascending=False)

    talimat_tahtasi_sats_alis = talimat_tahtasi[talimat_tahtasi.talimat_mali=="sats_alis"]
    talimat_tahtasi_sats_alis.sort_values( ["talimat_fiyati", "talimat_zamani"], inplace=True, ignore_index=True, ascending=False)

    min_satis_talimat_id=0
    max_alis_talimat_id=0

    min_satis_talimat_id = talimat_tahtasi_sats_satis.iloc[-1]["talimat_id"] 
    max_alis_talimat_id = talimat_tahtasi_sats_alis.iloc[0]["talimat_id"]  

    if  ( (globals()[max_alis_talimat_id].talimat_fiyati < globals()[min_satis_talimat_id].talimat_fiyati)) == False :
        tahta_isle()

tahta_isle_counter=0
def tahta_isle():
    global tahta_isle_counter
    tahta_isle_counter +=1 

    print(f" ******* {tahta_isle_counter} ************ tahta işleniyor *********************** ")
     
    satis = talimat_tahtasi_sats_satis.iloc[-1]
    alis = talimat_tahtasi_sats_alis.iloc[0]
    
    alis_miktari = talimat_tahtasi_sats_alis.iloc[0]["talimat_miktari"]
    satis_miktari = talimat_tahtasi_sats_satis.iloc[-1]["talimat_miktari"]

    if (alis_miktari > satis_miktari):
        globals() [satis.talimat_id].talimat_guncelle(0)
        globals() [alis.talimat_id].talimat_guncelle((alis_miktari-satis_miktari))
        tahta_guncelleme()

    elif (alis_miktari < satis_miktari):
        globals() [alis.talimat_id].talimat_guncelle(0)
        globals() [satis.talimat_id].talimat_guncelle((satis_miktari-alis_miktari))
        tahta_guncelleme()

    elif (alis_miktari == satis_miktari):
        globals() [satis.talimat_id].talimat_guncelle(0)
        globals() [alis.talimat_id].talimat_guncelle(0)
        tahta_guncelleme()
    
    
    print(" ******************* TAMAM tahta işleme TAMAM *********************** ")

def kapanan_talimat_listele():
    global kapanan_talimalar
    kapanan_talimalar=pd.DataFrame.from_records([globals() [s].to_dict() for s in talimat_listesi])    
    kapanan_talimalar=kapanan_talimalar[kapanan_talimalar.talimat_aktif_flag==False]
    print(" ---------------------------------- kapanan talimatlar listesi")
    print(kapanan_talimalar)

def aktif_talimat_listele():
    print(" ---------------------------------- talimat_tahtasi_sats_satis")
    print(talimat_tahtasi_sats_satis)
    print(" ---------------------------------- talimat_tahtasi_sats_alis")
    print(talimat_tahtasi_sats_alis)


class Talimat: 


    def __init__(self, talimat_id, talimat_zamani=date, talimat_sahibi="kim", talimat_mali="", talimat_miktari=0, talimat_fiyati=0 ):
        self.talimat_id=talimat_id
        self.talimat_zamani=datetime.now()
        self.talimat_sahibi=talimat_sahibi
        self.talimat_mali=talimat_mali
        self.talimat_miktari=talimat_miktari
        self.talimat_fiyati=talimat_fiyati
        self.talimat_buyuklugu=talimat_fiyati*talimat_miktari
        self.talimat_aktif_flag=True           
        talimat_listesi.append(talimat_id)                      

        if self.talimat_mali == "sats_satis" :
            globals() [self.talimat_sahibi].sats_bakiye_azalt(self.talimat_miktari)

        if self.talimat_mali == "sats_alis" :
            globals() [self.talimat_sahibi].usd_bakiye_azalt(self.talimat_miktari)

    def to_dict(self):        
        return {
            'talimat_zamani':  self.talimat_zamani,
            'talimat_id':  self.talimat_id,
            'talimat_sahibi': self.talimat_sahibi,
            'talimat_mali': self.talimat_mali,
            'talimat_miktari': self.talimat_miktari,
            'talimat_fiyati': self.talimat_fiyati,
            'talimat_buyuklugu': self.talimat_buyuklugu,
            'talimat_aktif_flag': self.talimat_aktif_flag
        } 

    def info(self):
        print(" talimat info  ************************")
        print("\n" + " talimat id :" + self.talimat_id +"\n"+ " zaman :" + str(self.talimat_zamani) +"\n"+ " sahibi :" + self.talimat_sahibi +"\n"+ " talimat malı :" + self.talimat_mali +"\n"+ " miktari :" + str(self.talimat_miktari) +"\n"+ " fiyati :" + str(self.talimat_fiyati) +"\n"+ " aktif flag :" + str(self.talimat_aktif_flag))    
       


    def talimat_guncelle(self, talimat_miktari_guncel):
        
        talimat_miktari_old = self.talimat_miktari
        self.talimat_miktari = talimat_miktari_guncel
        
        if self.talimat_miktari==0:
            self.talimat_aktif_flag=False          
        
        degisen_miktar = talimat_miktari_old - talimat_miktari_guncel

        if self.talimat_mali=="sats_satis" :
            globals() [self.talimat_sahibi].usd_bakiye_artir(degisen_miktar*self.talimat_fiyati)
            globals() [self.talimat_sahibi].sats_bakiye_azalt(degisen_miktar) 
            globals() [self.talimat_sahibi].niyet=0 
        if self.talimat_mali=="sats_alis" :
            globals() [self.talimat_sahibi].sats_bakiye_artir(degisen_miktar*self.talimat_fiyati)
            globals() [self.talimat_sahibi].usd_bakiye_azalt(degisen_miktar) 
            globals() [self.talimat_sahibi].niyet=0 


        fiyat_serisi.append(self.talimat_fiyati)
        



marketMaker = Oyuncu(name="marketMaker", usd_bakiye=100000, sats_bakiye=100000, niyet=0)
nt1 = Oyuncu(name="nt1", usd_bakiye=10000, sats_bakiye=10000, niyet=0)
nt2 = Oyuncu(name="nt2", usd_bakiye=10000, sats_bakiye=10000, niyet=0)

for i in range(3,30):
    globals() [f"nt{i}"] = Oyuncu(name=f"nt{i}", usd_bakiye=100, sats_bakiye=100, niyet=0)
    


tlmt0 = Talimat(talimat_id="tlmt0", talimat_sahibi="marketMaker", talimat_mali= "sats_alis" , talimat_miktari=50000, talimat_fiyati=1 )
tlmt1 = Talimat(talimat_id="tlmt1", talimat_sahibi="marketMaker", talimat_mali= "sats_satis" , talimat_miktari=50000, talimat_fiyati=100 )

### OYUNCU KARAKTER DAĞITIMI ###
riskrate = np.random.normal(5, 5, len(oyuncu_listesi))  
rrcounter=0
for oyuncu in oyuncu_listesi: 
    globals()[oyuncu].riskrate = riskrate[rrcounter]    
    rrcounter +=1

karakter = np.random.normal(0, 0.5 , len(oyuncu_listesi))  
kkcounter=0
for oyuncu in oyuncu_listesi: 
    globals()[oyuncu].karakter = karakter[kkcounter]    
    kkcounter +=1

oynvizyon = np.random.normal(7, 6, len(oyuncu_listesi))  
oynvizyon_counter=0
for oyuncu in oyuncu_listesi: 
    globals()[oyuncu].vizyon = int(oynvizyon[oynvizyon_counter])    
    oynvizyon_counter +=1

oynniyet = np.random.normal(0, 5, len(oyuncu_listesi))  
oynniyet_counter=0
for oyuncu in oyuncu_listesi: 
    globals()[oyuncu].niyet = int(oynniyet[oynniyet_counter])    
    oynniyet_counter +=1

def grafik_goster():
        plt.plot(fiyat_serisi) 
        plt.pause(0.0001)
        plt.clf()


for i in range(3):
    for oyuncu in oyuncu_listesi:
        if (oyuncu=="marketMaker")==False:
            globals() [oyuncu].analiz_et()
            globals() [oyuncu].islem_yap()
            sleep(0.001)
            tahta_guncelleme() 
            grafik_goster() 



aktif_talimat_listele()
kapanan_talimat_listele() 
oyuncu_listele() 
print(fiyat_serisi)
plt.plot(fiyat_serisi) 
plt.show() 
