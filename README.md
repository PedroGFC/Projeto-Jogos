# 🐧 Surfing Penguin

Um jogo simples desenvolvido com PyGame onde você controla um pinguim que precisa desviar de obstáculos em diferentes ambientes.

## 🎮 Como Jogar

- Use as **teclas de seta** (← → ↑ ↓) para mover o pinguim
- Desvie dos obstáculos/buracos que aparecem no caminho
- Complete cada fase para avançar para ambientes mais desafiadores

## 🌌 Fases do Jogo

| Fase | Ambiente | Velocidade | Pontos para passar | Dificuldade |
|------|----------|------------|---------------------|-------------|
| 1    | Gelo     | 5          | 150 pontos          | Fácil       |
| 2    | Água     | 10         | 300 pontos          | Médio       |
| 3    | Espaço   | 15         | 500 pontos          | Difícil     |

## 🎯 Mecânicas do Jogo

- Buracos aleatórios: Aparecem em posições diferentes a cada partida
- Sistema de pontuação: Pontos aumentam conforme o tempo de sobrevivência
- Aumento progressivo de dificuldade: Cada fase tem velocidade e objetivos diferentes

## 🛠️ Requisitos Técnicos

- Python 3.x instalado
- Biblioteca PyGame instalada (`pip install pygame`)
- Arquivos de assets na pasta `Assets/`

## 📥 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/PedroGFC/Projeto-Jogos.git
2. Acesse a pasta do projeto:
    ```bash
    cd Projeto-Jogos
3. Execute o jogo
    ```bash
    python game.py