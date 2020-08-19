import re

mezu_ezabatuak=0
i=0

def remove_emoji(string): #StackOverflow
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f92e" #Emoticono de Nagore
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def Egilea(frase):
    e=re.compile(r'([A-Z]\w+(\s\w+)?)(\s+)?(,)?(\s+)?2020$') # 2020ren aurrean dagoen hitza lortu
    if e.search(frase)== None:  #Egia izango da elkarrizketa denean orduan azkeneko ':' edo '-' baino lehen egongo da
        elkar=re.compile(r'(.+)?([A-Z]\w+(\s\w+)?):') #Hasieratik azkeneko izeneraino aztertu
        if elkar.search(frase)!= None:
            d=elkar.sub(r'\2',elkar.search(frase).group())

            return d
        else:
            print(frase)
            return 'Errorea'
    else:
        i=e.sub(r'\1',e.search(frase).group())# Goian lortutako zatitik (e.search....) bakarrik lehenengo parentesia gelditu (izena)
        return i

urtea=re.compile(r'2020') # Zertan fijatu behar den
zuzenketa=re.compile(r'\*') # * duten mezuak kontuan hartzeko

with open('datuak.txt','rb') as f_open: #byte moduan irakurri errorea ekiditeko
    byte = f_open.read()

z=remove_emoji(byte.decode('utf-8')) #Funtziora pasa  str moduan  eta emojirik gabe itzuli

Output = open('Output.txt','w') #Bukaerako fitxategia sortu

b=z.split('m. -') #- ren bitartez zaititu

c = ['KAGADAK:'] #Kagadak zeintzuk diren
e = ['Zeinek egin du?']
f = ['Idazleak']
g = ['Idazle ezberdinak']
errepikatua = False

extra=re.compile(r'(2020).+',re.DOTALL) # 2020 tik atzera dagoena aztertu (re.DOTALL enter ta hutsunek kontuan izateko)
enter=re.compile(r'\n') #Mezuen barneko enterrak kentzeko

for item in range(len(b)):

    b[item]=extra.sub(r'\1',b[item]) #2020 mantendu soilik b listatik
    b[item]=enter.sub(r' ',b[item]) #enterrak kendu
    if urtea.search(b[item]) == None and zuzenketa.search(b[item]) == None: #Egiaztatu urtea edo zuzenketak dakazten
        mezu_ezabatuak=mezu_ezabatuak+1
        
    elif urtea.search(b[item])!=None:
        
        idaz=re.compile(r'^(\s+)?(Unai (Telletxea)?|Ander|Jaion|Aizpi|Anne K|Idoia|La PeliRosa|Eñaut|Garaaaa|Goiburu|Nagore ADE |Leire Amona|Txapel)?(\:)?') #Idazleen lista
        idazle=idaz.search(b[item]).group()
        idazle=idaz.sub(r'\2',idazle)
        b[item]=idaz.sub(' ',b[item])

        c.append(b[item]) #Listara gehitu

        artista=Egilea(b[item])

        for pertsona in range(len(g)): #Begiratu Egilea egileen listan dagoen edo ez
            if g[pertsona] == artista:
                errepikatua=True

        if errepikatua==False: #Errepikatua EZ badago gehitu listara
            g.append(artista)
        errepikatua =False
        e.append(artista)#Egilea bilatu

        f.append(idazle)
                 
    else:
        c[i]=c[i]+' '+zuzenketa.search(b[item]).group() #Aurreko mezuarekin batera jarri

for ordena in range(len(g)):
    for cagada in range(len(c)):
        if g[ordena]==e[cagada]: # Egileen lista jarraituz denak errepasatu, ordena mantendu ahal izateko
            Output.write(e[cagada])
            Output.write('\n')
            Output.write(c[cagada])
            Output.write('          Bidaltzailea: ')
            Output.write(f[cagada])
            Output.write('\n\n')

Output.write('Mensajes eliminados: ')
Output.write(str(mezu_ezabatuak))

import numpy as np
import pandas as pd

Contactos='Txapel|Unai Telletxea|Ander|Jaion|Aizpi|Anne K|Idoia|La PeliRosa|Eñaut|Garaaaa|Goiburu|Nagore ADE |Leire Amona'.split('|')
Taula=pd.DataFrame(None,g,Contactos) #Bidaltzilea:Zutabe ; Kagada:Errenkada
Taula=Taula.fillna(0)

for x in range(len(c)-1): #Kagada guztietatik koordenatuak atera
    x=x+1
    Taula[f[x]][e[x]]=Taula[f[x]][e[x]]+1

Taula.loc['Totala']=Taula.sum(axis=0)
Taula.sort_values(by='Totala',axis=1,inplace=True,ascending=False)

Output.write('\n\n')
Output.write(Taula.to_string())

Output.write('\n\n')

d=[] #Errepikapenak gordetzeko array
for i in range(len(g)): #Kagada egile bakoitzeko
    d.append(0)         #Balioa gordetzeko toki bat sortu
    for j in range(len(e)): #Frase guztiak errepasatu
        if g[i]==e[j]:
            d[i]=d[i]+1

kontagailua= pd.Series(data=d,index=g).sort_values(ascending=False)
print(kontagailua)
Output.write(kontagailua.to_string())
Output.close()

import matplotlib.pyplot as plt

plt.rcdefaults()
plt.pie(d,labels=g)
plt.show()




