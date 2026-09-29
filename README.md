<div align="center">

  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/showdown/25.gif" alt="Pikachu Animado" width="130" />

  # ⚡ PokemonGenerator ⚡

  **Gerador Automatizado de Monstros (.lua e .xml) para Servidores PokeTibia / OTServer**

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3" />
    <img src="https://img.shields.io/badge/PokeTibia-OTServer-E3350D?style=for-the-badge&logo=pokemon&logoColor=white" alt="PokeTibia" />
    <img src="https://img.shields.io/badge/Web_Scraping-BeautifulSoup4-43B02A?style=for-the-badge" alt="Scraping" />
    <img src="https://img.shields.io/badge/Status-Ativo-brightgreen?style=for-the-badge" alt="Status" />
  </p>

```text
       \.-=-./
      /       \
     | (\   /) |      ⚡ Pika-Pikachu! ⚡
    /    _O_    \     Pronto para automatizar
   |   ( . . )   |    a criação dos seus Pokémons!
    \   `---'   /
     `--.....--'
```

</div>

---

## 📖 Sobre o Projeto

O **PokemonGenerator** é uma ferramenta desenvolvida em Python para automatizar a criação de arquivos de monstros (`.lua` e `.xml`) utilizados em servidores de **PokeTibia / Open Tibia Server (OTServer)**.

Ao invés de criar manualmente arquivos e status para centenas de Pokémons, o script faz **Web Scraping** em fontes especializadas ([PokemonDB](https://pokemondb.net) e [Pokemon.com](https://www.pokemon.com)), extraindo automaticamente:

- 📊 **Status Base:** HP, Attack, Defense, Sp. Atk, Sp. Def, Speed e Experience.
- 🥋 **Movesets:** Ataques base, Egg Moves e compatibilidade com TMs.
- 🧬 **Evoluções:** Próxima evolução, nível necessário e itens exigidos.
- 🥚 **Grupos de Ovos & Habilidades:** Egg groups e Abilities.
- 📝 **Descrições & Falas:** Pokédex oficial e falas temáticas.

---

## ⚡ Pikachu Adicionado!

O mascote oficial agora faz parte da lista padrão em `tabela.txt`:

<div align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png" alt="Pikachu Artwork" width="180" />
  <p><i>#025 - Pikachu (Electric)</i></p>
</div>

```csv
Pikachu,1025,20025,30025,40025,50025,60025,99999
```

---

## 📂 Estrutura de Arquivos

```bash
pokemon_project/
├── busca_dados_pokemon.py  # Módulo de web scraping (BeautifulSoup4 / Requests)
├── main.py                 # Painel interativo com menu de controle
├── tabela.txt              # Mapeamento de Pokémons e IDs de sprites/looktypes
├── template.lua            # Modelo base para os scripts Lua do PokeTibia
├── template.xml            # Modelo base para os arquivos XML do monster
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação do projeto
```

---

## 🛠️ Como Funciona o Mapeamento (`tabela.txt`)

Cada linha de `tabela.txt` representa um Pokémon e seus respectivos IDs utilizados pelo client e servidor:

```csv
Nome, LookType, CorpseId, PortraitId, ExtraId1, ExtraId2, ExtraId3, ExtraId4
```

Exemplo:
```csv
Bulbasaur,1001,20001,30001,40001,50001,60001,99999
Pikachu,1025,20025,30025,40025,50025,60025,99999
```

---

## 🚀 Instalação e Execução

### 1. Clonar o Repositório
```bash
git clone https://github.com/danielsoares15/PokemonGenerator.git
cd PokemonGenerator
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Iniciar o Painel
```bash
python main.py
```

---

## 🎮 Painel de Controle

Ao iniciar o `main.py`, um menu interativo estará disponível no terminal:

```text
==============================
      PAINEL POKÉMON      
==============================
1. Criar Pokémons (gerar .lua e .xml)
2. Listar Pokémons Existentes
3. Limpar Arquivos Brutos e Pastas de Pokémons
0. Sair
==============================
```

- **Opção 1:** Lê os Pokémons de `tabela.txt`, realiza a raspagem online e gera a pasta `pokemons/<nome>/` contendo os arquivos `<nome>.lua` e `<nome>.xml`.
- **Opção 2:** Exibe todos os Pokémons gerados localmente.
- **Opção 3:** Remove arquivos temporários ou a pasta gerada para recomeçar do zero.

---

## 👨‍💻 Autor

Desenvolvido por **[Daniel Soares](https://github.com/danielsoares15)**.
Fique à vontade para contribuir, abrir issues ou sugerir novas melhorias!
