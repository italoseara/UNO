# UNO em Python

## Descrição

Essa é uma implementação do jogo de cartas UNO em Python. É um trabalho em progresso.

## Requisitos

- Python 3.11 ou superior
- Instalar as dependências com `pip install -r requirements.txt`

## Rodando o jogo

Para rodar o jogo, execute o seguinte comando:

### Windows

```bash
py src/main.py
```

### Linux/MacOS

```bash
python3 src/main.py
```

## Como jogar

- Clique em HOST para criar um servidor
- Clique em JOIN para se conectar a um servidor, inserindo o IP e a porta do servidor
- Ao entrar em um servidor, espere o dono do servidor iniciar o jogo clicando em START
- Quando for sua vez, clique em uma carta para jogá-la
- Se não tiver nenhuma carta para jogar, clique no monte para comprar uma carta
- Quando tiver apenas uma carta, clique em UNO para avisar os outros jogadores (TODO)
- Quado algum jogador ficar sem cartas, o jogo acaba e o vencedor é anunciado
- Clique em RESTART para jogar novamente

## Autores

- [Italo Seara](https://github.com/italoseara)
- [Lucas Luige](https://github.com/lluigecm)
