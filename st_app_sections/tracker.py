import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from IPython.display import HTML
import datetime 
import pytz


__all__ = ["tracker"]





def tracker():
    st.markdown("<h1 style='text-align: center; '>Tracker players </h1>", unsafe_allow_html=True)
    tz = pytz.timezone("Brazil/East")
    time_now=datetime.datetime.now(tz).time()
    pesquisa = st.sidebar.text_input("Coloque seu nick para pesquisa")
    # st.write(current_time)
#  image = Image.open('assets/Ilustracao_Sem_Titulo.png')
#     col1, col2, col3 = st.columns([3,5.5,1])
#     with col1:
#         st.write("")

#     with col2:
#         st.image(image,width=250)

#     with col3:
#         st.write("")


    lista_server=["BR1","EUW1","JP1","KR","NA1",'OC1']

    server = st.selectbox('Escolha um server?',lista_server)
    result=''.join([i for i in server if not i.isdigit()])

    def actual_ladder(server):    
        lista_cha=requests.get(f"https://{server}.api.riotgames.com/tft/league/v1/challenger?api_key=RGAPI-68951cc5-0345-4a6e-af85-d9e541ec159c").json()
        lista_gm=requests.get(f"https://{server}.api.riotgames.com/tft/league/v1/grandmaster?api_key=RGAPI-68951cc5-0345-4a6e-af85-d9e541ec159c").json()
        lista_m=requests.get(f"https://{server}.api.riotgames.com/tft/league/v1/master?api_key=RGAPI-68951cc5-0345-4a6e-af85-d9e541ec159c").json()

        for entrie in lista_gm['entries']:
            lista_cha['entries'].append(entrie)
        for entrie in lista_m['entries']:
            lista_cha['entries'].append(entrie)

        nick=[]
        for i in range(len(lista_cha["entries"])):
            nick.append(lista_cha['entries'][i]["summonerName"])

        lp=[]
        for i in range(len(lista_cha["entries"])):
            lp.append(lista_cha['entries'][i]["leaguePoints"])
            
        games=[]
        for i in range(len(lista_cha["entries"])):
            games.append(lista_cha["entries"][i]["wins"]+lista_cha["entries"][i]["losses"])


        df=pd.DataFrame(lp,nick).reset_index().rename(columns={"index":"Nick",0:"League Points"})
        df["Daily Games"]=0
        df["Games"] = games
        df=df.sort_values("League Points",ascending=False).reset_index(drop=True)
        # df.to_csv(f'data/dia_ant{server}.csv',index_label=False) 
        # time.sleep(2) 
        return df

    def day_ladder(server):

               
        df=actual_ladder(server)
        dia_ant = pd.read_csv(f"data/dia_ant{server}.csv")
        
        dfa=df.merge(dia_ant,how="left",on="Nick")
        parcial=pd.DataFrame()
        # st.write(dfa)
        parcial["Nick"]=dfa["Nick"]
        parcial["League Points"]=dfa["League Points_x"]
        parcial["Total Games"]=dfa["Games"]
        parcial["Daily League Points"]=dfa["League Points_x"]-dfa["League Points_y"]
        parcial["Daily Games"]=dfa["Games"]-dfa["Total Games"]
        parcial=parcial.sort_values("Daily League Points",ascending=False).reset_index(drop=True)
        parcial.sort_values(['Daily League Points', 'League Points'], ascending=[False, False], inplace=True)
        lolchess=[]
        moba=[]
        for nick in parcial.Nick:
                lolchess.append(f"https://lolchess.gg/profile/{result}/{nick}")
                # moba.append(f"https://app.mobalytics.gg/pt_br/tft/profile/{result}/{nick}/overview")
        parcial["lolchess"]=lolchess
        # parcial["mobalytics"]=moba
        parcial.sort_values(['Daily League Points','League Points'],ascending=[True,True])
        parcial=parcial.fillna(0)
        parcial.iloc[:,1:-2] = parcial.iloc[:,1:-2].astype(int)
        parcial.reset_index(drop=True,inplace=True)
        parcial.index+=1




        parcial.to_csv(f"data/parcial{server}.csv",index=False)
        return parcial,dfa

    def reset_day(server):
        dia_ant=pd.read_csv(f'data/dia_ant{server}.csv')
        dfa=pd.read_csv(f'data/parcial{server}.csv')
        dia_ant=dfa
        dia_ant = dia_ant.to_csv(f"data/dia_ant{server}.csv")
        return

    if st.button("Atualizar ladder"): 

        with open('data/count.txt',"r") as f:
            contents = f.read()
        count=int(contents.split("=")[-1])
        count=count+1
        with open(f'data/count.txt',"w") as f:
            f.write(f'count={count}')   
        # try:
        parcial,dfo = day_ladder(server)
        
        st.write(parcial[parcial["Nick"]==pesquisa].rename(columns={'Nick':'Nick',
                                        'League Points':'Pontos de Liga',
                                        'Total Games': 'Total de Jogos',
                                        'Daily League Points':'Total de Pontos de Liga',
                                        'Daily Games': 'Jogos Diários'}))
        st.write(parcial.rename(columns={'Nick':'Nick',
                                        'League Points':'Pontos de Liga',
                                        'Total Games': 'Total de Jogos',
                                        'Daily League Points':'Total de Pontos de Liga',
                                        'Daily Games': 'Jogos Diários'}))
        # except:
        #     st.error(f'A Api para o servidor {server} da riot está com problemas')
       
    with open('data/count.txt',"r") as f:
        contents = f.read()
        count=int(contents.split("=")[-1])
    with open('data/current_time.txt',"r") as f:
        current_time = f.read()
        current_time=current_time.split("=")[-1]
    st.sidebar.write(f"O programa foi usado {count} vezes no dia de hoje")              
    st.sidebar.write(f"O programa foi atualizado em {current_time} dia de ontem") 
    
    senha= st.sidebar.text_input("Admin")
   
    if senha == "12345":    
        if st.button("Atualizar o dia"):
            with open(f'data/count.txt',"r") as f:
                contents = f.read()
            count=int(contents.split("=")[-1])
            count=0
            
            with open(f'data/count.txt',"w") as f:
                f.write(f'count={count}')
            current_time = time_now.strftime("%H:%M")
            with open(f'data/current_time.txt',"w") as f:
                f.write(f'current_time={current_time}')
            for servers in lista_server:
                try:
                    day_ladder(servers)
                    reset_day(servers)
                    st.success('Pontos diários foram resetados.')
                    st.balloons()
                except:
                    pass
      
            
if __name__ == "__main__":
    tracker()