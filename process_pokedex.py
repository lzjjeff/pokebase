from lzj_util import *
import re

def pokedex():
    pokedex = []
    with open("raw_data/pokedex.txt", "r", encoding="utf-8") as fi:
        generation = -1
        for line in fi:
            if re.match(".*第[一|二|三|四|五|六|七]世代", line):
                generation += 1
                pokedex.append([])
                continue
            elif len(line) < 4:
                continue
            poke = line.split("|")
            pokedex[generation].append([poke[1], poke[2]])

    for pokegen in pokedex:
        for pokemon in pokegen:
            output_str_to_file("\t".join(pokemon) + "\n", "pokedex.txt", mode="a+")

def moves():
    moves = []
    with open("raw_data/moves.txt", "r", encoding="utf-8") as fi:
        generation = -1
        for line in fi:
            if re.match(".*第[一|二|三|四|五|六|七]世代", line):
                generation += 1
                moves.append([])
                continue
            elif len(line) < 4:
                continue
            move = re.split("\||}", line)
            moves[generation].append([move[1], move[2], move[5], move[6], move[7], move[8], move[9]])

    for pokegen in moves:
        for pokemon in pokegen:
            output_str_to_file("\t".join(pokemon) + "\n", "moves.txt", mode="a+")

def stats():
    stats = []
    with open("raw_data/stats.txt", "r", encoding="utf-8") as fi:
        for line in fi:
            poke = re.split("\||}", line)
            if poke[3].startswith("form"):
                form = poke[3][5:]
                sum = 0
                for i in range(4, 10):
                    sum += int(poke[i])
                stats.append([poke[1], form + poke[2], poke[4], poke[5], poke[6],
                              poke[7], poke[8], poke[9], str(sum)])
            else:
                sum = 0
                for i in range(3, 9):
                    sum += int(poke[i])
                stats.append([poke[1], poke[2], poke[3], poke[4], poke[5], poke[6],
                              poke[7], poke[8], str(sum)])

        for stat in stats:
            output_str_to_file("\t".join(stat) + "\n", "stats.txt", mode="a+")

def pokemon():
    pokemon = []
    with open("raw_data/pokemon.txt", "r", encoding="utf-8") as fi:
        for line in fi:
            poke = []
            line = re.split("\|\|", line)
            poke.append(line[0])
            poke.append(line[1])
            temp = re.split("\||\}\}", line[4])
            poke.append(temp[1])
            if len(temp) == 3:
                poke.append("")
            else:
                poke.append(temp[3])
            pokemon.append(poke)

        for poke in pokemon:
            output_str_to_file("\t".join(poke) + "\n", "pokemon.txt", mode="a+")


if __name__ == '__main__':
    pokemon()