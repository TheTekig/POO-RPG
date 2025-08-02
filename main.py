import random
import os
import json
from time import sleep
from random import randint
import datetime

#region  //SAVE|LOAD\\


#endregion

#region  //Classes\\

class Pessoa:
    def __init__(self, nome, vida, defesa, ataque, speed):
        self.nome = nome
        self.vida = vida
        self.defesa = defesa
        self.ataque = ataque
        self.ataquemax = ataque
        self.vidamax = vida
        self.speed = speed

class Heroi(Pessoa):
    def __init__(self, nome, vida, defesa, ataque, classe, speed):
        super().__init__(nome, vida, defesa, ataque, speed)
        self.nivel = 1
        self.xp = 0
        self.classe = classe
        self.inventario = []

    def status(self):
        sleep(0.5)
        print(f"Nome: {self.nome}")
        sleep(0.5)
        print(f"Vida: {self.vida}/{self.vidamax}")
        sleep(0.5)
        print(f"Defesa: {self.defesa}")
        sleep(0.5)
        print(f"Ataque: {self.ataque}/{self.ataquemax}")
        sleep(0.5)
        print(f"Nível: {self.nivel}")
        sleep(0.5)
        print(f"XP: {self.xp}")
        sleep(0.5)
        print(f"Classe: {self.classe}")
        sleep(0.5)
        print(f"Mochila: {self.inventario}")
        sleep(0.5)

    def nivelar(self):
        while self.xp >= (self.nivel * 5):
            self.xp -= (self.nivel * 5)
            self.nivel += 1

            self.vida = self.vidamax

            if self.classe == "Guerreiro":
                self.vidamax += 8
                self.ataque += 1
                self.defesa += 2

            elif self.classe == "Arqueiro":
                self.vidamax += 6
                self.ataque += 2
                self.defesa += 1

            elif self.classe == "Assassino":
                self.vidamax += 10
                self.ataque += 3
                self.defesa += 1
                self.speed += 1

            self.vida = self.vidamax
            self.ataquemax = self.ataque

    def atacar(self, inimigo):
        dano = self.ataque - inimigo.defesa
        if dano < 0:
            dano = 0
        inimigo.vida -= dano

    def ataque_skills(self, inimigo, vSkillset, opcao):

        if opcao == vSkillset['Arqueiro']['Tiro Preciso']:
            if vSkillset['Arqueiro']['Tiro Preciso']['usos'] > 0:
                self.ataque += vSkillset['Arqueiro']['Tiro Preciso']['bonus_ataque']
                dano = self.ataque - (inimigo.defesa * vSkillset['Arqueiro']['Tiro Preciso']['ignora_defesa'])
                if dano < 0:
                    dano = 0
                inimigo.vida -= dano
                self.ataque = self.ataquemax
                vSkillset['Arqueiro']['Tiro Preciso']['usos'] -= 1
            else:
                return False

        elif opcao == vSkillset['Arqueiro']['Chuva de Flechas']:
            if vSkillset['Arqueiro']['Chuva de Flechas']['usos'] > 0:
                for i in range(vSkillset['Arqueiro']['Chuva de Flechas']['hits']):
                    dano = self.ataque - inimigo.defesa
                    if dano < 0:
                        dano = 0
                    inimigo.vida -= dano
                vSkillset['Arqueiro']['Chuva de Flechas']['usos'] -= 1
            else:
                return False

        elif opcao == vSkillset['Guerreiro']['Investida']:
            if vSkillset['Guerreiro']['Investida']['usos'] > 0:
                self.ataque += vSkillset['Guerreiro']['Investida']['bonus_ataque']
                dano = self.ataque - inimigo.defesa
                if dano < 0:
                    dano = 0
                inimigo.vida -= dano
                self.ataque = self.ataquemax
                vSkillset['Guerreiro']['Investida']['usos'] -= 1
            else:
                return False

        elif opcao == vSkillset['Guerreiro']['Escudo Supremo']:
            if vSkillset['Guerreiro']['Escudo Supremo']['usos'] > 0:
                self.defesa += vSkillset['Guerreiro']['Escudo Supremo']['bonus_defesa']
                vSkillset['Guerreiro']['Escudo Supremo']['usos'] -= 1
            else:
                return False

        elif opcao == vSkillset['Assassino']['Ataque Furtivo']:
            if vSkillset['Assassino']['Ataque Furtivo']['usos'] > 0:
                self.ataque *= vSkillset['Assassino']['Ataque Furtivo']['bonus_critico']
                dano = self.ataque - inimigo.defesa
                if dano < 0:
                    dano = 0
                inimigo.vida -= dano
                self.ataque = self.ataquemax
                vSkillset['Assassino']['Ataque Furtivo']['usos'] -= 1
            else:
                return False

        elif opcao == vSkillset['Assassino']['Lamina Rapida']:
            if vSkillset['Assassino']['Lamina Rapida']['usos'] > 0:
                for i in range(vSkillset['Assassino']['Lamina Rapida']['hits']):
                    self.ataque *= vSkillset['Assassino']['Lamina Rapida']['dano_por_hit']
                    dano = self.ataque - inimigo.defesa
                    if dano < 0:
                        dano = 0
                    inimigo.vida -= dano
                    self.ataque = self.ataquemax
                vSkillset['Assassino']['Lamina Rapida']['usos'] -= 1
            else:
                return False

    def descansar(self):
        self.vida += 5
        if self.vida > self.vidamax:
            self.vida = self.vidamax

        vSkillset['Guerreiro']['Escudo Supremo']['usos'] = vSkillset['Guerreiro']['Escudo Supremo']['totalusos']
        vSkillset['Guerreiro']['Investida']['usos'] = vSkillset['Guerreiro']['Investida']['totalusos']

        vSkillset['Arqueiro']['Tiro Preciso']['usos'] = vSkillset['Arqueiro']['Tiro Preciso']['totalusos']
        vSkillset['Arqueiro']['Chuva de Flechas']['usos'] = vSkillset['Arqueiro']['Chuva de Flechas']['totalusos']

        vSkillset['Assassino']['Ataque Furtivo']['usos'] = vSkillset['Assassino']['Ataque Furtivo']['totalusos']
        vSkillset['Assassino']['Lamina Rapida']['usos'] = vSkillset['Assassino']['Lamina Rapida']['totalusos']

    def mochila(self):
        for item in self.inventario:
            print(item)

    def encontrar_item(self):
        item = pocoesger()['potion']
        item = random.choice(item)
        self.inventario.append(item)

    def pocao(self, pocao):
        efeito = pocao
        self.vida += efeito
        self.ataque += efeito
        self.inventario.pop(pocao)


class Enemy(Pessoa):
    def __init__(self, nome, vida, defesa, ataque, localizacao, speed, xp):
        super().__init__(nome, vida, defesa, ataque, speed)
        self.localizacao = localizacao
        self.xp = xp

    def atacar(self, jogador):
        dano = self.ataque - jogador.defesa
        if dano < 0:
            dano = 0
        jogador.vida -= dano

    def morreu(self):
        return self.vida <= 0

class Pocao:
    def __init__(self, nome, vida, ataque):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque

#endregion

def mapa():
    Mapa = """
                                            [VILA BANDIDOS]
    [CASTELO ABANDONADO]  [ACAMPAMENTO]      //
            \               ||              //
        [MONTANHA]======[CIDADE]=======[CAMPO]=======[FLORESTA]
            //             ||                            //
    [DUNGEON]              ||                           //
                        [TORRE SOMBRIA]        [FLORESTA DENSA]

    """
    print(Mapa)

def combate(heroi, inimigo,vSkillset):
    while True:

        if heroi.vida <= 0:
            print(f"{heroi.nome} foi derrotado!")
            break
        elif inimigo.vida <= 0:
            print(f"{inimigo.nome} foi derrotado!")
            break


        vez = ["Jogador", "Inimigo"]
        peso = [heroi.speed, inimigo.speed]
        vez = random.choices(vez, weights=peso, k=1)


        if vez[0] == "Jogador":
            menu_Combate()
            opcao = input("Escolha uma opção: ")
            while opcao not in ["1","2","3","4"]: opcao = input("Opção Invalida\nEscolha uma opção: ")

            if opcao == "1":
                heroi.atacar(inimigo)
                print(f"{heroi.nome} atacou {inimigo.nome} com {heroi.ataque} de dano!")
                continue

            if opcao == "2":
                print("=" * 50)
                print("Skills")
                print("=" * 50)
                heroi.ataque_skills(inimigo, vSkillset, nome_skill_escolhida)
                print(f"{heroi.nome} usou {nome_skill_escolhida} em {inimigo.nome}!")
                continue

            if opcao == "3":
                heroi.mochila()
                opcao = input("Escolha uma opção: ")
                while item not in heroi.inventario: opcao = input("Opção Invalida\nEscolha uma opção: ")
                heroi.pocao(opcao)
                print(f"{heroi.nome} usou uma poção!")
                continue

            if opcao == "4":
                fugir = random.choices(vez, weights=peso, k=1)

                if fugir == "Jogador":
                    print(f"{heroi.nome} fugiu!")
                    break
                else:
                    print(f"Jogador não conseguiu fugir!")
                    continue 
        else:

            inimigo.atacar(heroi)
            print(f"{inimigo.nome} atacou {heroi.nome} com {inimigo.ataque} de dano!")

def move(vLocal,localizacao):

        print("Onde Deseja ir?")
        print("=" * 50)
        for i in localizacao:
            if i != localizacao[-1]:
                print(f"{i}", end=" | ")
        print("Ficar")
        print("=" * 50)
        opcao = input("")
        if opcao == "Ficar": opcao = localizacao[-1]
        while opcao not in localizacao: opcao = input("Opção Invalida\nEscolha uma opção: ")
        localizacao = vLocal[opcao]
        return localizacao

def acontecimentos():

    Ocorrencia = ["Nada Ocorreu", "Inimigo Encontrado", "Item Achado"]
    peso = [0.4, 0.5, 0.1]
    ocorrencia = random.choices(Ocorrencia, weights=peso, k=1)
    return ocorrencia[0]

def controlador(vLocal,heroi,vSkillset):
    localizacao = vLocal["Cidade"]
    while True:
        menu_HUD(localizacao)
        opcao = opcoes()

        if opcao == "1":
            print("=" * 50)
            print("Explorar")
            localizacao = move(vLocal,localizacao)
            ocorrencia = acontecimentos()

            if ocorrencia == "Inimigo Encontrado":
                print("Um inimigo apareceu!")
                print("=" * 50)
                print("Tipo da variável 'localizacao':", type(localizacao))
                print("Valor da variável 'localizacao':", localizacao[-1])
                inimigo = inimigos()[localizacao[-1]]
                inimigo = random.choice(inimigo)
                combate(heroi, inimigo, vSkillset)
                print("=" * 50)

            if ocorrencia == "Item Achado":
                print("Um item foi encontrado!")
                heroi.encontrar_item()
                
                print("=" * 50)

            if ocorrencia == "Nada Ocorreu":
                print("Nada aconteceu!")
                print("=" * 50)

            print("=" * 50)

        if opcao == "2":
            print("=" * 50)
            print("Inventário")
            print("=" * 50)

        if opcao == "3":
            print("=" * 50)
            print("Status")
            heroi.status()
            mapa()
            print("=" * 50)

#region     //Cadastros\\

def cadastrar_heroi(vClasse):

    nome = input("Digite o nome do herói: ")
    classe = input("Digite a classe do herói: ")
    classe = vClasse[classe]
    heroi = Heroi(nome, classe['vidamax'], classe['defesa'], classe['ataquemax'], classe, classe['speed'])

    return heroi

def inimigos():
    return {

            "Campo" : [
                Enemy("Lobo Selvagem", 12, 2, 3, "Campo", 5, 5),
                Enemy("Javali", 14, 3, 2, "Campo", 3, 6),
                Enemy("Bandido Novato", 10, 1, 4, "Campo", 4, 7)
                ],

            "Floresta" : [
                Enemy("Goblin", 16, 3, 5, "Floresta", 6, 10),
                Enemy("Aranha Gigante", 18, 4, 5, "Floresta", 4, 12),
                Enemy("Lobo Alfa", 20, 4, 6, "Floresta", 7, 14)
                ],

            "Floresta_Densa" : [
                Enemy("Troll da Floresta", 28, 5, 7, "Floresta_Densa", 2, 20),
                Enemy("Druida Corrompido", 22, 3, 8, "Floresta_Densa", 5, 18),
                Enemy("Jaguatirica Fantasma", 18, 4, 9, "Floresta_Densa", 8, 22)
                ],

            "Vila_Bandidos" : [
                Enemy("Bandido Veterano", 22, 5, 7, "Vila_Bandidos", 5, 20),
                Enemy("Arqueiro Mercenário", 18, 3, 9, "Vila_Bandidos", 7, 18),
                Enemy("Capanga do Chefe", 24, 5, 8, "Vila_Bandidos", 4, 22)
                ],

            "Acampamento" : [
                Enemy("Capitão Bandido", 26, 6, 8, "Acampamento", 5, 25),
                Enemy("Ladino Emboscador", 20, 4, 10, "Acampamento", 8, 23),
                Enemy("Caçador de Recompensas", 22, 5, 9, "Acampamento", 6, 24)
                ],

            "Torre_Sombria" : [
                Enemy("Feiticeiro Aprendiz", 20, 3, 11, "Torre_Sombria", 6, 26),
                Enemy("Espírito Sombrio", 24, 4, 10, "Torre_Sombria", 7, 28),
                Enemy("Cavaleiro Espectral", 30, 7, 9, "Torre_Sombria", 4, 30)
                ],

            "Montanha" : [
                Enemy("Urso Pardo", 32, 6, 10, "Montanha", 4, 32),
                Enemy("Harpia", 26, 5, 11, "Montanha", 8, 34),
                Enemy("Gigante das Rochas", 40, 8, 9, "Montanha", 3, 40)
                ],

            "Castelo_Abandonado" : [
                Enemy("Cavaleiro Fantasma", 34, 7, 11, "Castelo_Abandonado", 5, 38),
                Enemy("Zumbi de Armadura", 36, 9, 9, "Castelo_Abandonado", 2, 36),
                Enemy("Gárgula", 30, 6, 12, "Castelo_Abandonado", 7, 40)
                ],
            "Dungeon" : [
                Enemy("Esqueleto Guerreiro", 34, 7, 12, "Dungeon", 6, 45),
                Enemy("Necromante", 32, 5, 14, "Dungeon", 7, 50),
                Enemy("Demônio Guardião", 50, 10, 13, "Dungeon", 5, 70)
                ]
    }

def pocoesger():
    return {
        "potion":[
        Pocao("Poção de Cura", 10, 0),
        Pocao("Poção de Ataque", 0, 5),
        Pocao("Poção Mista", 5, 3)
        ]
    }

#endregion

#region       //Menu\\
def menu_HUD(localizacao):
    print("-=-" * 20)
    sleep(0.5)
    print("\t\tHUD")
    sleep(0.5)
    print("=" * 60)
    sleep(0.5)
    print(f"\tLocalização: {localizacao}")
    sleep(0.5)
    print("=" * 60)
    sleep(0.5)
    print("1. Explorar  |  2. Inventario  |  3. Status")
    sleep(0.5)
    print("-=-" * 20)

def menu_Combate():
    print("-=-" * 20)
    sleep(0.5)
    print("Combate")
    sleep(0.5)
    print("-=-" * 20)
    sleep(0.5)
    print("1. Atacar  |  2. Skills  |  3. Poções  |  4. Fugir")
    sleep(0.5)
    print("-=-" * 20)

def menu():
    print("=" * 50)
    sleep(0.5)
    print("Sistemas RPG - POO")
    sleep(0.5)
    print("=" * 50)
    sleep(0.5)
    print("1.      Jogar")
    sleep(0.5)
    print("2. Cadastrar Heroi")
    sleep(0.5)
    print("3.      Sair")
    sleep(0.5)
    print("=" * 50)

def opcoes():
    opcao = input("Escolha uma opção: ")
    while opcao not in ["1","2","3"]: opcao = input("Opção Invalida\nEscolha uma opção: ")
    return opcao

#endregion

def main():

    vClasse = {
    "Arqueiro"  : {"ataquemax": 14, "vidamax": 16, "defesa": 6, "speed" : 6},
    "Guerreiro" : {"ataquemax": 11, "vidamax": 22, "defesa": 10, "speed" : 4},
    "Assassino" : {"ataquemax": 18, "vidamax": 12, "defesa": 4, "speed" : 8}
    }

    vSkillset = {
        "Arqueiro"  : {
            "Tiro Preciso" : {

                "descricao": "Ataque com mira, ignora metade da defesa do inimigo.",
                "bonus_ataque": 4,
                "ignora_defesa": 0.5,
                "usos": 2,
                "totalusos": 2

            },
            "Chuva de Flechas" : {

                "descricao": "Vários tiros rápidos, acerta 2x com dano reduzido.",
                "hits": 2,
                "dano_por_hit": 0.6,
                "usos": 3,
                "totalusos": 3
            }
        },
        "Guerreiro" : {

            "Investida": {

                "descricao": "Ataque poderoso que atordoa por 1 turno.",
                "bonus_ataque": 5,
                "stun": 1,
                "usos": 3,
                "totalusos": 3

        },
            "Escudo Supremo" : {

                "descricao": "Levanta o escudo, reduz 50% do dano por 2 turnos.",
                "bonus_defesa": 0.5,
                "duracao": 2,
                "usos": 4,
                "totalusos": 4

            }
        },
        "Assassino" : {
            "Ataque Furtivo" : {

                "descricao": "Golpe crítico se for o primeiro ataque da luta.",
                "bonus_critico": 2.0,  # multiplica o dano
                "usos": 1,
                "totalusos": 1

            },
            "Lamina Rapida" : {

                "descricao": "Dois ataques rápidos em um turno.",
                "hits": 2,
                "dano_por_hit": 0.8,
                "usos": 2,
                "totalusos": 2

            }
        }
    }

    vLocal = {

            "Cidade" : ["Acampamento", "Campo", "Torre_Sombria", "Montanha",
            "Cidade"],
            "Campo" : ["Vila_Bandidos","Floresta", "Cidade","Campo"],
            "Floresta" : ["Campo","Floresta_Densa", "Floresta"],
            "Floresta_Densa" : ["Floresta", "Floresta_Densa"],
            "Vila_Bandidos" : ["Campo", "Vila_Bandidos"],
            "Acampamento" : ["Cidade", "Acampamento"],
            "Torre_Sombria" : ["Cidade", "Torre_Sombria"],
            "Montanha" : ["Castelo_Abandonado", "Dungeon", "Cidade",    "Montanha"],
            "Castelo_Abandonado" : ["Montanha", "Castelo_Abandonado"],
            "Dungeon" : ["Montanha", "Dungeon"]
    }




    while True:
        menu()
        opcao = opcoes()

        if opcao == "1":
            print("=" * 50)
            controlador(vLocal,heroi,vSkillset)
            print("=" * 50)

        if opcao == "2":
            print("=" * 50)
            heroi = cadastrar_heroi(vClasse)
            print("=" * 50)

        if opcao == "3":
            print("Saindo do programa...")
            sleep(1)
            break

main()









