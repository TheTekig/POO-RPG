# Projeto 12 – RPG Console com Mapa

Um RPG de console em Python com:

        - Sistema de mapa textual
        - Exploração de locais (Cidade, Floresta, Caverna, Dungeon, Lago, etc.)
        - Combate por turnos
        - Inventário básico
        - Eventos aleatórios
        - HUD colorido (usando `termcolor`)


---

## 🎮 Funcionalidades

- **Mapa textual**:
    - Exibição do mundo com diferentes áreas.
- **Sistema de personagem**:
    - Criação de personagem.
    - Atributos: vida, ataque, defesa.
- **Combate por turnos**:
    - Ataque simples.
    - Derrota e vitória com XP.
- **Eventos aleatórios**:
    - Inimigos aparecem ao entrar em áreas.
- **Inventário básico**:
    - Itens simples para uso durante o jogo.
- **Interface colorida no console**:
    - Utilizando a biblioteca `termcolor`.


---

## 🗺️ Locais do Jogo

        - Cidade
        - Floresta
        - Lago
        - Floresta Sombria
        - Caverna
        - Dungeon
        - Vila Antiga

---

## 🚀 Como executar

1. Clone o repositório:

        git clone https://github.com/seuusuario/projeto12-rpg-console.git
        cd projeto12-rpg-console

Instale as dependências:

        pip install termcolor

Execute:

        python main.py

📂 Estrutura de Pastas

        projeto12-rpg-console/
        │
        ├── main.py             # Código principal do jogo
        ├── data/               # Futuro: armazenar saves
        ├── README.md
        └── CHANGELOG.md
