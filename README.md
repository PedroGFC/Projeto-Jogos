# 🐧 Surfing Penguin

Um jogo simples desenvolvido com PyGame onde você controla um pinguim que precisa desviar de obstáculos em diferentes ambientes ao som de músicas incríveis.

## 🎮 Como Jogar

- Use as **teclas de seta** (↑ ↓) para mover o pinguim
- Desvie dos obstáculos que aparecem no caminho
- Complete cada fase para avançar para ambientes mais desafiadores

## 🌌 Fases do Jogo

| Fase | Ambiente | Velocidade | Pontos para passar | Quantidade de Inimigos | Dificuldade |
|------|----------|------------|--------------------|------------------------|-------------|
| 1    | Neve     | 10         | 150 pontos         | Baixa                  | Fácil       |
| 2    | Oceano   | 12         | 300 pontos         | Média                  | Médio       |
| 3    | Vulcão   | 14         |                    | Alta                   | Difícil     |

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