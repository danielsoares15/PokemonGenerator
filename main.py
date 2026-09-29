import json
import os
import xml.etree.ElementTree as ET
from string import Template
import shutil # Importa o módulo shutil para operações de arquivo de alto nível

# Certifique-se de que 'busca_dados_pokemon' está acessível (no mesmo diretório ou no PYTHONPATH)
from busca_dados_pokemon import busca_poke_dados


# -----------------------------------------------------------------------------------
# Funções de Suporte (extraídas do seu script anterior)
# -----------------------------------------------------------------------------------

def extrair_dados_lista(lista_str):
    """Extrai dados de uma string formatada como CSV para uma lista de dicionários."""
    linhas = lista_str.split('\n')
    resultado = []
    
    for linha in linhas:
        dados = linha.split(',')
        if len(dados) < 2: 
            continue 
        
        dicionario = {
            'name': dados[0].strip()
        }
        
        valores = [int(valor.strip()) for valor in dados[1:] if valor.strip().isdigit()]
        for i, valor in enumerate(valores):
            chave = f'id{i + 1}'
            dicionario[chave] = valor
        
        if dicionario['name']:
            resultado.append(dicionario)
    
    return resultado

def preencher_arquivo_lua(poke_search_data, poke_table_data, template_file, output_file):
    """Preenche um template .lua com os dados do Pokémon e salva."""
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Erro ao criar diretório '{output_dir}': {e}")
            return 

    with open(template_file, 'r') as file:
        template = file.read()    

    rendered_template = template.replace('name_poke', poke_search_data['NOME'].capitalize())
    rendered_template = rendered_template.replace('ELEMENT_FIRE', f'ELEMENT_{poke_search_data["TIPO"].upper()}')
    
    learn_tm=''
    if isinstance(poke_search_data.get('LEARNMOVESTM'), list):
        for move in poke_search_data['LEARNMOVESTM']:
            learn_tm+=f'TM_IDS.{move.upper()}, '
    rendered_template = rendered_template.replace('<learnTM>', learn_tm)
    
    rendered_template = rendered_template.replace('10037', str(poke_table_data.get('id7', '')))
    rendered_template = rendered_template.replace('38', str(poke_search_data.get('HP', '')))
    rendered_template = rendered_template.replace('65', str(poke_search_data.get('SPEED', '')))
    rendered_template = rendered_template.replace('41', str(poke_search_data.get('ATK', '')))
    rendered_template = rendered_template.replace('40', str(poke_search_data.get('DEF', '')))
    rendered_template = rendered_template.replace('50', str(poke_search_data.get('SP.ATK', '')))
    rendered_template = rendered_template.replace('65', str(poke_search_data.get('SP.DEF', '')))
    
    if isinstance(poke_search_data.get('EGGMOVES'), list):
        rendered_template = rendered_template.replace('<eggmoves>', ', '.join(f'"{str(x)}"' if isinstance(x, str) else str(x) for x in poke_search_data['EGGMOVES']))
    else: 
        rendered_template = rendered_template.replace('<eggmoves>', f'"{poke_search_data.get("EGGMOVES", "")}"')

    if isinstance(poke_search_data.get('MOVESSET'), list):
        rendered_template = rendered_template.replace("<move_set>", ', '.join(f'"{str(move)}"' if isinstance(move, str) else str(move) for move in poke_search_data['MOVESSET']))
    else:
        rendered_template = rendered_template.replace("<move_set>", "")
    
    if isinstance(poke_search_data.get('ABILITIES'), list):
        rendered_template = rendered_template.replace('<abilities>', ', '.join(f'"{ability}"' for ability in poke_search_data['ABILITIES']))
    else:
        rendered_template = rendered_template.replace('<abilities>', "")
    
    rendered_template = rendered_template.replace('40', str(poke_search_data.get('CHANCE', '')))
    rendered_template = rendered_template.replace('<portrait>', str(poke_table_data.get('id4', '')))
    rendered_template = rendered_template.replace('13538', str(poke_table_data.get('id3', '')))
    rendered_template = rendered_template.replace('10671', str(poke_table_data.get('id5', '')))
    rendered_template = rendered_template.replace('16037', str(poke_table_data.get('id6', '')))

    egg_groups = ''
    if isinstance(poke_search_data.get('EGGGROUPS'), list):
        for group in poke_search_data['EGGGROUPS']:
            egg_groups+=f'POKEMON_EGG_GROUP_{group.upper()}, '
    
    if poke_search_data.get("EVOLVE") and 'evolution' not in poke_search_data["EVOLVE"]:  
        required_item = poke_search_data.get('REQUIRED_ITEM', '')
        evolve_name = poke_search_data["EVOLVE"].capitalize()
        required_level = poke_search_data.get("REQUIREDLEVELEVOLVE", 0) 
        
        evolve = f'name=\"{evolve_name}\", requiredLevel={required_level}, requiredItems={{ {required_item} }}' if required_item else f'name=\"{evolve_name}\", requiredLevel={required_level}'
        rendered_template = rendered_template.replace('<evolve>', evolve)
    else:
        rendered_template = rendered_template.replace('<evolve>', '')
        
    rendered_template = rendered_template.replace('POKEMON_EGG_GROUP_FIELD', egg_groups)
    rendered_template = rendered_template.replace("<descript>", f'\"{poke_search_data.get("DESCRIPTION", "")}\"')

    with open(output_file, 'w', encoding='utf-8') as file: # Adiciona encoding para melhor compatibilidade
        file.write(rendered_template)

def preencher_arquivo_xml(poke_search_data, poke_table_data, template_file, output_file):
    """Preenche um template .xml com os dados do Pokémon e salva."""
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Erro ao criar diretório '{output_dir}': {e}")
            return 

    tree = ET.parse(template_file)
    root = tree.getroot()

    poke_name = poke_search_data['NOME'].capitalize()
    root.set('name', poke_name)
    root.set('nameDescription', f"a {poke_name}")
    root.set('shiny', poke_name)
    root.set('race', 'blood')
    root.set('experience', str(poke_search_data.get('EXPERIENCE', '')))
    root.set('speed', str(poke_search_data.get('SPEED', '')))
    root.set('manacost', '0')
    root.set('minLevel', '20')
    root.set('maxLevel', '30')
    attacks = root.find('attacks')
        
    for attack in attacks.iter('attack'):
        if attack.get('name') == 'melee':
            attack.set('attack', str(poke_search_data.get('ATK', '')))
    
    if poke_search_data.get("EVOLVE") and 'evolution' not in poke_search_data["EVOLVE"]:
        new_attack = ET.Element('attack', {'name': 'Evolve', 'interval': '15000', 'chance': '1'})
        attacks.append(new_attack)       
            
    for voice in root.iter('voice'):
        voice.set('sentence', f'{poke_name.upper()}!')
    
    for look in root.iter('look'):
        look.set('type', str(poke_table_data.get('id1', '')))
        look.set('corpse', str(poke_table_data.get('id2', '')))

    tree.write(output_file, encoding="UTF-8", xml_declaration=True)

def criar_pasta_pokemon(nome_pokemon):
    """Cria a estrutura de pastas 'pokemons/nome_pokemon/'."""
    pasta_base = "pokemons"
    caminho = os.path.join(pasta_base, nome_pokemon.lower())
    try:
        os.makedirs(caminho, exist_ok=True) 
    except OSError as e:
        print(f"Erro ao criar pasta '{caminho}': {e}")
        raise 
    return caminho

# -----------------------------------------------------------------------------------
# Funções para as Opções do Menu
# -----------------------------------------------------------------------------------

def criar_todos_pokemons():
    """Processa a criação de arquivos para todos os Pokémons da tabela."""
    print("\n--- Criando arquivos dos Pokémons ---")
    
    with open('tabela.txt' ,'r') as lista:
        pkm_list_str = lista.read()
    
    pokemon_table_data = extrair_dados_lista(pkm_list_str)

    template_lua_file = 'template.lua'
    template_xml_file = 'template.xml'

    for i, poke_data in enumerate(pokemon_table_data):
        poke_name_lower = poke_data['name'].lower() 
        
        try:
            print(f"Buscando dados para {poke_name_lower.capitalize()}...")
            pokemon_search_data = busca_poke_dados(poke_name_lower)
                
            caminho_da_pasta_pokemon = criar_pasta_pokemon(poke_name_lower)

            output_lua_file = os.path.join(caminho_da_pasta_pokemon, f'{poke_name_lower}.lua')
            preencher_arquivo_lua(pokemon_search_data, poke_data, template_lua_file, output_lua_file)

            output_xml_file = os.path.join(caminho_da_pasta_pokemon, f'{poke_name_lower}.xml')
            preencher_arquivo_xml(pokemon_search_data, poke_data, template_xml_file, output_xml_file)

            print(f'✅ Dados do Pokémon {poke_name_lower.capitalize()} salvos em: {caminho_da_pasta_pokemon}')

        except Exception as e:
            print(f"❌ Erro ao processar o Pokémon {poke_name_lower.capitalize()}: {e}")
    print("\n--- Criação de Pokémons concluída ---")

def listar_pokemons_existentes():
    """Lista as pastas de Pokémons existentes no diretório 'pokemons/'."""
    print("\n--- Pokémons Criados ---")
    pasta_pokemons = "pokemons"
    if not os.path.exists(pasta_pokemons):
        print(f"A pasta '{pasta_pokemons}' não existe. Nenhum Pokémon criado ainda.")
        return

    pokemons = [d for d in os.listdir(pasta_pokemons) if os.path.isdir(os.path.join(pasta_pokemons, d))]
    
    if pokemons:
        for poke in sorted(pokemons):
            print(f"- {poke.capitalize()}")
    else:
        print("Nenhum Pokémon encontrado na pasta 'pokemons'.")
    print("\n--- Fim da lista ---")

def limpar_arquivos_brutos():
    """Remove arquivos temporários como bruto1.txt e bruto3.txt."""
    print("\n--- Limpando arquivos brutos ---")
    arquivos_para_limpar = ['bruto1.txt', 'bruto3.txt']
    
    limpeza_feita = False
    for arquivo in arquivos_para_limpar:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                print(f"🗑️ Arquivo '{arquivo}' removido com sucesso.")
                limpeza_feita = True
            except OSError as e:
                print(f"⚠️ Erro ao remover '{arquivo}': {e}")
        else:
            print(f"Arquivo '{arquivo}' não encontrado. (Ignorando)")
    
    # Adicionando a opção de limpar a pasta 'pokemons' inteira, se o usuário quiser
    print("\nDeseja remover TODAS as pastas de Pokémons criadas (pokemons/)?")
    confirmacao = input("Isso apagará todos os arquivos .lua e .xml gerados. (s/N): ").lower()
    if confirmacao == 's':
        pasta_pokemons = "pokemons"
        if os.path.exists(pasta_pokemons):
            try:
                shutil.rmtree(pasta_pokemons) # Remove a pasta e todo o seu conteúdo
                print(f"🗑️ Pasta '{pasta_pokemons}' e seu conteúdo removidos com sucesso.")
                limpeza_feita = True
            except OSError as e:
                print(f"⚠️ Erro ao remover pasta '{pasta_pokemons}': {e}")
        else:
            print(f"Pasta '{pasta_pokemons}' não encontrada. (Ignorando)")


    if not limpeza_feita:
        print("Nenhum arquivo bruto ou pasta de Pokémon foi limpo.")
    print("\n--- Limpeza concluída ---")


# -----------------------------------------------------------------------------------
# Painel de Controle Principal
# -----------------------------------------------------------------------------------

def exibir_menu():
    """Exibe o menu de opções."""
    print("\n" + "="*30)
    print("      PAINEL POKÉMON      ")
    print("="*30)
    print("1. Criar Pokémons (gerar .lua e .xml)")
    print("2. Listar Pokémons Existentes")
    print("3. Limpar Arquivos Brutos e Pastas de Pokémons")
    print("0. Sair")
    print("="*30)

def main():
    """Função principal que executa o painel de controle."""
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            criar_todos_pokemons()
        elif opcao == '2':
            listar_pokemons_existentes()
        elif opcao == '3':
            limpar_arquivos_brutos()
        elif opcao == '0':
            print("Saindo do Painel Pokémon. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção entre 0 e 3.")
        
        input("\nPressione Enter para continuar...") # Pausa para o usuário ler a saída

if __name__ == "__main__":
    main()