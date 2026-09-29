import json
import os

import requests
from bs4 import BeautifulSoup


def busca_poke_dados(poke_name):
    """Função que faz uma raspagem no site pokemn.db e devolve 
        os dados do pokemon passado como parametro"""

    #Raspagem
    url = f'https://pokemondb.net/pokedex/{poke_name}'
    urlEgg = f'https://pokemondb.net/pokedex/{poke_name}/egg'
    urlDescription = f'https://www.pokemon.com/br/pokedex/{poke_name}'
    site = requests.get(url)
    egg=requests.get(urlEgg)
    desc = requests.get(urlDescription)
    soup = BeautifulSoup(site.content,'html.parser')
    soup2 = BeautifulSoup(egg.content,'html.parser')
    soup3 = BeautifulSoup(desc.content, 'html.parser')
    
    hps = soup.find_all('table', class_ ='vitals-table') 
    hps2 = soup.find_all('a', class_ ='type-icon') #tipo
    hps3 = soup.find_all('span', class_ ='infocard-lg-data text-muted') #evolution
    hps4 = soup.find_all('span', class_ ='infocard infocard-arrow') #requiredLevel
    hps5 = soup3.find_all('div', class_='version-descriptions')
    poke_description =''
    for i in range(len(hps5)):
        poke_description+=hps5[i].get_text().replace('\n','')
        poke_description = poke_description.replace('    ','').strip()
    
    #------------------------------------------------------------------------------
    #resolvendo o caso da evolução
    evolve=''
    try:
        lastEvolve = hps3[len(hps3)-1].get_text().split()[1].lower()
        atualEvolve = poke_name
        crawledEvolve =hps3[1].get_text().split()[1].lower() 
        if lastEvolve in atualEvolve:
            evolve = 'This is the last evolution'
        elif crawledEvolve in atualEvolve:
            evolve = lastEvolve.upper()
        else:
            evolve = crawledEvolve.upper()
    except:
        pass

    #-----------------------------------------
    #Raspagem para os egg moves
    hps5 = soup2.find('nav', class_='panel panel-nav')
    egg_move_list = []
    try:
        lista_eggs = hps5.findChildren()
        for i in lista_eggs:
            if i.get_text() not in 'Egg moves' and '\n' not in i.get_text():
                if i.get_text() not in egg_move_list:
                    egg_move_list.append(i.get_text())
    except:
        pass
    #----------------------------------------------------------------------------------------
    #raspagem dos learnmoves
    
    
    
    
    #Aqui acabamos de encontrar os egg moves
    
#--------------------------------------------------------------------------------------
    # daqui pra baixo faço acesso a uma api para conseguir os dados de moveset mais facil
    
    url =f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
    cha = requests.get(url).text
    dados = json.loads(cha)
    move_list = []
   
    for i in range (len(dados['moves'])):
        name = dados['moves'][i]['move']['name']
        required_level = int(dados['moves'][i]['version_group_details'][0]['level_learned_at'])
        if required_level==0:
            continue
        else:
            move_list.append(name)
            move_list.append(required_level)

            #Aqui acabamos de encontrar o moveset
#--------------------------------------------------------------------------------------
    #conseguindo as habilidades (Abilities)
    
    a_tags = soup.select('table.vitals-table  a[href*="/ability/"]')
    abilities=[]
    for a in a_tags:
        abilities_text = a.get_text()
        abilities.append(abilities_text)
#-----------------------------------------------------------------------------------
#Aprendendo os learn moves
    learn_moves= soup.find_all('div',class_='span-lg-6' )
    for div in learn_moves:
            h3 = div.find('h3')
            if h3 and h3.get_text() == "Moves learnt by TM":
                learn_moves_bruto = div.select ('div.resp-scroll table.data-table tbody tr td.cell-name a.ent-name ')
                
    learn_moves_list=[]            
    for i in learn_moves_bruto:
        learn_moves_list.append(i.get_text())
#_______________________________________________________________________________________
#conseguindo os egg groups:
    a_tags = soup.select('table.vitals-table tbody td a[href*="/egg-group/"]')
    egg_groups=[]
    for a in a_tags:
        group =  a.get_text()
        if group not in egg_groups:
            egg_groups.append(group)

#__________________________________________________________________________________________
    #transposição dos dados para uma lista
    full_text=[]
    for i in range(len(hps)):
        if hps[i].get_text()!='\n':
            full_text.append(f'{hps[i].get_text()}\n') 
 
    #Criação do dicionario que será retornado com os dados 
    data = {
        'NOME':poke_name.upper(),
        'HP':'', 
        'ATK':'', 
        'DEF':'', 
        'SPEED':'', 
        'SP.ATK' :'', 
        'SP.DEF':'',
        'EXPERIENCE':'',
        'EVOLVE': evolve, 
        'TIPO':hps2[0].get_text().upper(), 
        'CHANCE':'', 
        'ABILITIES':abilities,
        'REQUIREDLEVELEVOLVE':required_level, 
        'MOVESSET':move_list, 
        'LEARNMOVESTM':learn_moves_list,
        'EGGGROUPS':egg_groups,
        'EGGMOVES':  egg_move_list if len(egg_move_list)!=0  else f'{poke_name.upper()} does not have any egg moves.',
        'DESCRIPTION':poke_description
        }
    
    
    if evolve:
        try:
            if len(hps4)==1:
                data['REQUIREDLEVELEVOLVE']=int(hps4[0].get_text().replace(')',' ').split()[1])
            else:
                data['REQUIREDLEVELEVOLVE']=int(hps4[1].get_text().replace(')',' ').split()[1])
        except:
            text_level= hps4[0].get_text().replace('(','').replace(')','')   
            if 'stone'in text_level.lower() :
                data['REQUIRED_ITEM'] = f'ITEM.{text_level.split()[1].upper()}_{text_level.split()[2].upper()}'
                data['REQUIREDLEVELEVOLVE'] = 1
            else:
                text_level = hps4[1].get_text().replace('(','').replace(')','')
                if 'stone'in text_level.lower() :
                    data['REQUIRED_ITEM'] = f'ITEM.{text_level.split()[1].upper()}_{text_level.split()[2].upper()}'
                    data['REQUIREDLEVELEVOLVE'] = 1
                else:
                    data['REQUIREDLEVELEVOLVE']=0
            
        
    #separando os dados brutos num arquivo de texto
    for i in range(len(full_text)):
        if i ==1 or i==3:   
            with open(f'bruto{i}.txt','w')as bruto:
                bruto.writelines(full_text[i])
            
    with open('bruto3.txt','r')as bruto:
        b= bruto.readlines()
        #Filtrando os dados necessários e passando para o dicionario
        for i in range(len(b)):
            if "HP" in b[i]  :
                data['HP']=int(b[i+1])
            elif "Attack" in b[i]  :
                data['ATK']=int(b[i+1])
            elif "Defense" in b[i]  :
                data['DEF']=int(b[i+1])
            elif "Sp. Atk" in b[i]  :
                data['SP.ATK']=int(b[i+1])
            elif "Sp. Def" in b[i]  :
                data['SP.DEF']=int(b[i+1])
            elif "Speed" in b[i]  :
                data['SPEED']=int(b[i+1])
    with open('bruto1.txt','r')as bruto:
        b= bruto.readlines()
        for i in range(len(b)):
            if 'Base Exp.'in b[i]:
                data['EXPERIENCE'] = int(b[i+1])
            elif 'Catch rate' in b[i]:
                # Garante que há pelo menos 3 linhas após 'Catch rate'
                if i+2 < len(b):
                    valor = ''.join(filter(str.isdigit, b[i+2]))
                    if valor:
                        data['CHANCE'] = int(valor)
                    else:
                        data['CHANCE'] = 0
                else:
                    data['CHANCE'] = 0

    

    #retornando o dicionario                
    return data
#____________________________________________________________________________________________________



# pokemons = [
#     'pikachu', 
#     # 'charmander',
#     # 'bulbasaur',
#     # 'ivysaur',
#     # 'blastoise',
    # 'metapod',
#     # 'ekans',
#     # 'turtwig',
#     # 'vulpix',
    # 'aerodactyl',
    # 'torterra'
    # ]
 
# #vamos passar um laço 'for' para printar os dados de cada um:
# for i in pokemons:
#     print(f'{busca_poke_dados(i)}\n\n\n')
    

