
from datetime import date
from datetime import datetime
from operator import is_not
from random import randint
from time import sleep
from unicodedata import name
import pandas as pd
from dataclasses import make_dataclass


pd.options.mode.chained_assignment = None  # aşağıdaki uyarıyı almamak için koydum bu satırı.
""" A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  talimat_tahtasi_sats_satis["kumule_talimat"][i]=talimat_tahtasi_sats_satis["talimat_buyuklugu"][i]
z:/PythonNT/Fiyat_tahtasi.py:121: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  talimat_tahtasi_sats_satis["kumule_talimat"][i]=talimat_tahtasi_sats_satis["talimat_buyuklugu"][i] + talimat_tahtasi_sats_satis["kumule_talimat"][i+1]
z:/PythonNT/Fiyat_tahtasi.py:136: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  talimat_tahtasi_sats_alis["kumule_talimat"][i]=talimat_tahtasi_sats_alis["talimat_buyuklugu"][i]
z:/PythonNT/Fiyat_tahtasi.py:138: SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame

See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
  talimat_tahtasi_sats_alis["kumule_talimat"][i]=talimat_tahtasi_sats_alis["talimat_buyuklugu"][i] + talimat_tahtasi_sats_alis["kumule_talimat"][i-1]
 """

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

    def set_usd_bakiye(self, usd_bakiye):
        self.usd_bakiye = usd_bakiye        
    def set_sats_bakiye(self, sats_bakiye):
        self.sats_bakiye = sats_bakiye 

    def get_usd_bakiye(self):
        return self.usd_bakiye
    def get_sats_bakiye(self):
        return self.sats_bakiye 

    def sats_bakiye_artir(self,miktar):
        self.sats_bakiye = self.sats_bakiye + miktar
    def usd_bakiye_artir(self,miktar):
        self.usd_bakiye = self.usd_bakiye + miktar
    def sats_bakiye_azalt(self,miktar):
        self.sats_bakiye = self.sats_bakiye - miktar
    def usd_bakiye_azalt(self,miktar):
        self.usd_bakiye = self.usd_bakiye - miktar

    def bakiye(self):
        print(str(self.name) + " usd bakiye: " + str(self.usd_bakiye) + " sats bakiye " + str(self.sats_bakiye))

    def usd_al(self, miktar=0 , fiyat=1):
        self.usd_bakiye = self.usd_bakiye + miktar/fiyat
        self.sats_bakiye = self.sats_bakiye - miktar*fiyat
    def sats_al(self, miktar=0, fiyat=1):
        self.usd_bakiye = self.usd_bakiye - miktar/fiyat
        self.sats_bakiye = self.sats_bakiye + miktar*fiyat
        

    def egilim_degistir(self, egilim=0):
        self.niyet=self.niyet+egilim*self.karakter

    def __str__(self):
        return ("Benim Adım : " +str(self.name) +"."+ " USD bakiyem: " + str(self.usd_bakiye) +" Sats bakiyem: " + str(self.sats_bakiye) +"\n")
    #   return ("USD: " + str(self.usd_bakiye) +"\nSats: " + str(self.sats_bakiye))

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

    # kümüle talimat hesabı lazım olana dek aşağıdaki alanı kapatıyorum

    """ talimat_tahtasi_sats_satis["kumule_talimat"] = pd.Series(dtype='int')             
    for i in reversed(range(len(talimat_tahtasi_sats_satis))):                            
        if i == (len(talimat_tahtasi_sats_satis)-1):
            talimat_tahtasi_sats_satis["kumule_talimat"][i]=talimat_tahtasi_sats_satis["talimat_buyuklugu"][i]
        else:
            talimat_tahtasi_sats_satis["kumule_talimat"][i]=talimat_tahtasi_sats_satis["talimat_buyuklugu"][i] + talimat_tahtasi_sats_satis["kumule_talimat"][i+1]


    talimat_tahtasi_sats_alis["kumule_talimat"] = pd.Series(dtype='int')
    for i in range( len(talimat_tahtasi_sats_alis) ):                
        if i == 0:
            talimat_tahtasi_sats_alis["kumule_talimat"][i]=talimat_tahtasi_sats_alis["talimat_buyuklugu"][i]
        else:
            talimat_tahtasi_sats_alis["kumule_talimat"][i]=talimat_tahtasi_sats_alis["talimat_buyuklugu"][i] + talimat_tahtasi_sats_alis["kumule_talimat"][i-1] """


    min_satis_talimat_id=0
    max_alis_talimat_id=0

    min_satis_talimat_id = talimat_tahtasi_sats_satis.iloc[-1]["talimat_id"] 
    max_alis_talimat_id = talimat_tahtasi_sats_alis.iloc[0]["talimat_id"]  

    ''' 
    print("min_satis_talimat_id")
    print(min_satis_talimat_id)
    print("max_alis_talimat_id")
    print(max_alis_talimat_id)
    print("talimat_aktif_flag")
    '''
    

    # aktif_talimat_listele()

    if  ( (globals()[max_alis_talimat_id].talimat_fiyati < globals()[min_satis_talimat_id].talimat_fiyati)) == False :

        """ globals()[max_alis_talimat_id].info()
        globals()[min_satis_talimat_id].info() """
        
        """ print(" *********** TALİMAT FİYATALARI EŞİT ************ ")
        globals()[max_alis_talimat_id].info()
        globals()[min_satis_talimat_id].info()
        print(" *********** TALİMAT FİYATALARI EŞİT ************ ") """
        tahta_isle()

def tahta_isle():
    print(" ******************* tahta işleniyor *********************** ")
     
    satis = talimat_tahtasi_sats_satis.iloc[-1]
    alis = talimat_tahtasi_sats_alis.iloc[0]
    
    alis_miktari = talimat_tahtasi_sats_alis.iloc[0]["talimat_miktari"]
    satis_miktari = talimat_tahtasi_sats_satis.iloc[-1]["talimat_miktari"]

    """ print("alis_miktari")
    print(alis_miktari)

    print("satis_miktari")
    print(satis_miktari) """


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
        # if (len(talimat_listesi)>1):
        #    tahta_guncelleme()                 # esas sorun sıralama ile ilgili galiba. bu komut en az 1 alış 1 satış emri olmadığında hata veriyor            
        talimat_listesi.append(talimat_id)                      # bunu en kısa zamanda self ile eşitlemeye çalışacağız.

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
        
        """ print(" *********** güncellenen talimat bilgileri aşağıda ****************** ")
        self.info()
        print(" *********** güncellenen talimat bilgileri yukarıda ****************** ") """

        
         
        
        '''

        # talimat miktarını güncelle
        # azalan talimata göre oyuncunun bakiyesini güncelle
        # tahta güncelle

        print("talimat miktari düştü")''' 



marketMaker = Oyuncu(name="marketMaker", usd_bakiye=100000, sats_bakiye=100000, niyet=0)
nt1 = Oyuncu(name="nt1", usd_bakiye=10000, sats_bakiye=10000, niyet=0)
nt2 = Oyuncu(name="nt2", usd_bakiye=10000, sats_bakiye=10000, niyet=0)

for i in range(3,20):
    globals() [f"nt{i}"] = Oyuncu(name=f"nt{i}", usd_bakiye=10000, sats_bakiye=10000, niyet=0)
    


tlmt0 = Talimat(talimat_id="tlmt0", talimat_sahibi="marketMaker", talimat_mali= "sats_alis" , talimat_miktari=50000, talimat_fiyati=1 )
tlmt1 = Talimat(talimat_id="tlmt1", talimat_sahibi="marketMaker", talimat_mali= "sats_satis" , talimat_miktari=50000, talimat_fiyati=100 )
""" tlmt2 = Talimat(talimat_id="tlmt2", talimat_sahibi="nt2", talimat_mali= "sats_satis" , talimat_miktari=20, talimat_fiyati=30 )
tlmt3 = Talimat(talimat_id="tlmt3", talimat_sahibi="nt3", talimat_mali= "sats_satis" , talimat_miktari=20, talimat_fiyati=10 )
tlmt4 = Talimat(talimat_id="tlmt4", talimat_sahibi="nt3", talimat_mali= "sats_alis" , talimat_miktari=10, talimat_fiyati=20 )
tlmt5 = Talimat(talimat_id="tlmt5", talimat_sahibi="nt3", talimat_mali= "sats_alis" , talimat_miktari=15, talimat_fiyati=30 )
tlmt6 = Talimat(talimat_id="tlmt6", talimat_sahibi="nt5", talimat_mali= "sats_satis" , talimat_miktari=20, talimat_fiyati=10 )
tlmt7 = Talimat(talimat_id="tlmt7", talimat_sahibi="nt4", talimat_mali= "sats_alis" , talimat_miktari=25, talimat_fiyati=20 )
tlmt8 = Talimat(talimat_id="tlmt8", talimat_sahibi="nt5", talimat_mali= "sats_satis" , talimat_miktari=25, talimat_fiyati=20 )
tlmt9 = Talimat(talimat_id="tlmt9", talimat_sahibi="nt1", talimat_mali= "sats_alis" , talimat_miktari=10, talimat_fiyati=1 )
tlmt10 = Talimat(talimat_id="tlmt10", talimat_sahibi="nt5", talimat_mali= "sats_satis" , talimat_miktari=10, talimat_fiyati=100 ) """


for i in range(100):
    for oyuncu in oyuncu_listesi:
        if (oyuncu=="marketMaker")==False:
            globals() [oyuncu].analiz_et()
            globals() [oyuncu].islem_yap()
            tahta_guncelleme


aktif_talimat_listele()
kapanan_talimat_listele() 

oyuncu_listele() 


print(fiyat_serisi)

import matplotlib.pyplot as plt

plt.plot(fiyat_serisi)
  
plt.show()
