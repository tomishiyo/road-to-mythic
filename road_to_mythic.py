"""
Simulador do número de partidas para atingir o rank Mítico a partir do Plat 4 com 1 ponto, no MTGA.
Metodologia:
- Dada uma WR, simulamos o resultado de uma partida, e ajustamos o rank de acordo com as regras do MTGA, a saber:
1) Uma vitória conta 1 ponto no Bo1, e a vitória em uma série conta 2 pontos no Bo3. Vitórias no último ponto do tier contam 2 (por exemplo, quando se passa de platina 5 para platina 4, o rank inicial não é platina 4 - 0, mas platina 4 - 1);
2) Uma derrota retira 1 ponto no Bo1, o mesmo para a derrota em uma série no Bo3. A menos que você esteja no Platina 4 com zero vitórias ou no Diamante 4 com zero vitórias.
3) Quando 48 pontos são acumulados, o jogador atinge o rank mítico.

"""
# Autor: Guilherme Tomishiyo, 13/06/2023.

import random
import matplotlib.pyplot as plt
import math

class Player:
    """
    Os ranks são representados por um número inteiro na variável rank, onde 0 corresponde à Platina 4 com zero vitórias e 48, o rank mítico.
    24 vitórias resultam no diamante 4.

    A win rate é representada pelo número real wr.
    """
    def __init__(self, wr, rank = 1):
        self.rank = rank
        self.wr = wr
        self.isMythic = False
    
    def rank_up(self, format):
        """
        format: [bo1, bo3] para formatos melhor de 1 e 3, respectivamente. Note que as variáveis são strings.
        """
        if format == "bo1":
            boost = 1
        elif format == "bo3":
            boost = 2

        if (self.rank + boost) % 6 == 0:
            if self.rank + boost >= 48:
                self.isMythic = True              
            else:
                self.rank += boost + 1              
        else: 
            self.rank += boost

    def rank_down(self):
        """
        A mesma função é usada para Bo1 e Bo3
        """
        if self.rank != 0 and self.rank != 24:
            self.rank -= 1

    def play_bo1(self):
       roll = random.random()

       if self.wr >= roll:                      
           self.rank_up("bo1")                      
       else:
           self.rank_down()

    def play_bo3(self):
       victories = len([x for x in range(3) if random.random() <= self.wr])

       if victories > 1:
           self.rank_up("bo3")                      
       else:
           self.rank_down()


def get_mythic(player, format):
    number_of_games = 0

    while not (player.isMythic):
        number_of_games += 1
        if format == "bo1":
          player.play_bo1()
        else:
          player.play_bo3()
    
    # Resetting
    player.isMythic =  False
    player.rank = 1

    return number_of_games
       

if __name__ == "__main__":
    # Condições iniciais

    data_points = 7
    starting_wr = 0.5
    increment = 0.05

    winrates = [starting_wr + increment * i for i in range(data_points)]

    series_bo1 = []
    series_bo3 = []

    # Loop gerador da série de dados

    for winrate in winrates:
      player = Player(winrate)

      number_of_mythics_climbs = 10000
      number_bo1 = 0
      number_bo3 = 0

      for i in range(number_of_mythics_climbs):
          number_bo1 += get_mythic(player, "bo1")
          number_bo3 += get_mythic(player, "bo3")
      
      average_bo1 = round(number_bo1 / number_of_mythics_climbs)
      average_bo3 = round(number_bo3 / number_of_mythics_climbs)

      series_bo1.append(average_bo1)
      series_bo3.append(average_bo3)

    # Plotagem dos resultados
    
    fig1 = plt.figure(1)
    plt.plot(winrates, series_bo1, ".", label="Best of 1")
    plt.xlabel("Winrate")
    plt.ylabel("Número médio de jogos Bo1" )
    plt.grid()
    plt.savefig("wr_versus_numero.png")

    fig2 = plt.figure(2)
    plt.plot(winrates, [round(x / 30) for x in series_bo1], ".", label="Games per day")
    plt.xlabel("Winrate")
    plt.ylabel("Número médio de jogos Bo1 por dia" )
    plt.grid()
    plt.savefig("wwr_versus_numero_dia.png")