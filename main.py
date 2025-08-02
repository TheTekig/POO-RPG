import random
import os
import json
from time import sleep
from random import randint
import datetime
from termcolor import colored

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
        print(colored(f"\tNome: {self.nome}", "white", attrs=["bold"]))
        sleep(0.5)
        print(colored(f"\tVida: {self.vida}/{self.vidamax}", "white", attrs=["bold"]))
        sleep(0.5)
        print(colored(f"\tDefesa: {self.defesa}", "white", attrs=["bold"]))
        sleep(0.5)
        print(colored(f"\tAtaque: {self.ataque}/{self.ataquemax}", "white", attrs=["bold"]))
        sleep(0.5)
        print(colored(f"\tNível: {self.nivel}", "white", attrs=["bold"]))
        sleep(0.5)
        print(colored(f"\tXP: {self.xp}", "white", attrs=["bold"]))
        sleep(0.5)
        print(colored(f"\tClasse: {self.classe}", "white", attrs=["bold"]))
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

            print(colored(""))

    def atacar(self, inimigo):
        dano = self.ataque - inimigo.defesa
        if dano < 0:
            dano = 0
        inimigo.vida -= dano

    def ataque_skills(self, inimigo, vSkillset, opcao):

        if opcao == 'Tiro Preciso':
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

        if opcao == 'Chuva de Flechas':
            if vSkillset['Arqueiro']['Chuva de Flechas']['usos'] > 0:
                for i in range(vSkillset['Arqueiro']['Chuva de Flechas']['hits']):
                    dano = self.ataque - inimigo.defesa
                    if dano < 0:
                        dano = 0
                    inimigo.vida -= dano
                vSkillset['Arqueiro']['Chuva de Flechas']['usos'] -= 1
            else:
                return False

        if opcao == 'Investida':
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

        if opcao == 'Escudo Supremo':
            if vSkillset['Guerreiro']['Escudo Supremo']['usos'] > 0:
                self.defesa += vSkillset['Guerreiro']['Escudo Supremo']['bonus_defesa']
                vSkillset['Guerreiro']['Escudo Supremo']['usos'] -= 1
            else:
                return False

        if opcao == "Ataque Furtivo":
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

        if opcao == 'Lamina Rapida':
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
        for i, item in enumerate(self.inventario, start=1):
            print(f"{i}.{item.nome} (vida +{item.vida}, ataque +{item.ataque})")

    def encontrar_item(self):
        item = pocoesger()['potion']
        item = random.choice(item)
        self.inventario.append(item)

    def pocao(self, pocao):
        self.vida += pocao.vida
        self.ataque += pocao.ataque
        self.inventario.pop(pocao)


class Enemy(Pessoa):
    def __init__(self, nome, vida, defesa, ataque, localizacao, speed, xp):
        super().__init__(nome, vida, defesa, ataque, speed)
        self.localizacao = localizacao
        self.xp = xp
        self.vidamax = vida

    def atacar(self, jogador):
        dano = self.ataque - jogador.defesa
        if dano < 0:
            dano = 0
        jogador.vida -= dano
    
    def morte(self,jogador):
        jogador.xp += self.xp

class Pocao:
    def __init__(self, nome, vida, ataque):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque

#endregion

def mapa():
    Mapa = """


                                            [VILA BANDIDOS]
    [CASTELO ABANDONADO]  [ACAMPAMENTO]      /
             ||              ||             /
        [MONTANHA]======[CIDADE]=======[CAMPO]=======[FLORESTA]
            //             ||                            //
    [DUNGEON]              ||                           //
                        [TORRE SOMBRIA]        [FLORESTA DENSA]


    """
    print(colored(Mapa,"white", "on_grey",attrs=["bold"]))

def combate(heroi, inimigo,vSkillset):
    while True:

        if heroi.vida <= 0:
            print(colored(f"{heroi.nome} foi derrotado!", "red", "on_grey"))
            break
        elif inimigo.vida <= 0:
            print(colored(f"{inimigo.nome} foi derrotado!", "green", "on_grey"))
            inimigo.morte(heroi)
            heroi.nivelar()
            break

        print("\n")
        print(colored(f"{heroi.nome}:", "white", attrs=["bold"]), colored(f"{heroi.vida}", "white"), "/", colored(f"{heroi.vidamax}", "blue"), "  ⚔️  " , colored(f"{inimigo.nome}:", "red", attrs=["bold"]), colored(f"{inimigo.vida}"), "/", colored(f"{inimigo.vidamax}", "magenta"))
        vez = ["Jogador", "Inimigo"]
        peso = [heroi.speed, inimigo.speed]
        vez = random.choices(vez, weights=peso, k=1)


        if vez[0] == "Jogador":
            menu_Combate()
            opcao = input(colored("\tOP: ", "red", attrs=["bold"]))
            while opcao not in ["1","2","3","4"]: opcao = input(colored("\tOpção Invalida\n\tOP: ", "red", attrs=["bold"]))

            if opcao == "1":
                heroi.atacar(inimigo)
                print(colored(f"{heroi.nome} atacou {inimigo.nome} com {heroi.ataque} de dano!", "white", attrs=["bold"]))
                continue

            if opcao == "2":
                print("Skills")
                skills = list(vSkillset[heroi.classe].keys())
                for i, chave in enumerate(vSkillset[heroi.classe].keys(), start=1):
                    usos_restantes = vSkillset[heroi.classe][chave]['usos']
                    total_usos = vSkillset[heroi.classe][chave]['totalusos']
                    print(f"{i}. {chave} ({usos_restantes}/{total_usos})")

                opcao_skill = int(input("Escolha uma Skill: "))
                nome_skill_escolhida = skills[opcao_skill - 1]   
                
                resultado = heroi.ataque_skills(inimigo, vSkillset, nome_skill_escolhida)
                
                if resultado is False:
                    print(colored("\n\tVoce nao tem mais usos para essa skill!","red", "on_grey"))
                else:
                    print(colored(f"\n{heroi.nome} usou {nome_skill_escolhida} em {inimigo.nome}!", "green", "on_grey"))
                continue

            if opcao == "3":
                heroi.mochila()
                opcao = int(input(colored("\tOP: ", "red", attrs=["bold"])))
                while opcao < 1 or opcao > len(heroi.inventario) : opcao = int(input(colored("\tOpção Invalida\n\tOP: ", "red", attrs=["bold"])))
                pocao = heroi.inventario[opcao - 1]
                heroi.pocao(pocao)
                print(colored(f"{heroi.nome} usou a poção - {pocao.nome}!", "blue", "on_grey"))
                continue

            if opcao == "4":
                fugir = random.choices(vez, weights=peso, k=1)

                if fugir == "Jogador":
                    print(colored(f"{heroi.nome} fugiu!", "red"))
                    break
                else:
                    print(colored(f"Jogador não conseguiu fugir!", "red"))
                    continue 
        else:

            inimigo.atacar(heroi)
            print(f"{inimigo.nome} atacou {heroi.nome} com {inimigo.ataque} de dano!")

def move(vLocal,localizacao):

        print(colored("\t\t    Onde Deseja ir?      ", "white", attrs=["bold"]))
        for i in localizacao:
            if i != localizacao[-1]:
                print(colored(f"{i}", "white", attrs=["bold"]), end=" | ")
        print(colored("Ficar", "white"))
        opcao = input(colored("Local: ", "white", attrs=["bold"]))
        if opcao == "Ficar": opcao = localizacao[-1]
        while opcao not in localizacao: 
            opcao = input(colored("\tOpção Invalida\n\tOP: ", "red", attrs=["bold"]))
            if opcao == "Ficar": 
                opcao = localizacao[-1]
                break

        localizacao = vLocal[opcao]
        return localizacao

def acontecimentos():

    Ocorrencia = ["Nada Ocorreu", "Inimigo Encontrado", "Item Achado"]
    peso = [0.1, 0.6, 0.3]
    ocorrencia = random.choices(Ocorrencia, weights=peso, k=1)
    return ocorrencia[0]

def controlador(vLocal,heroi,vSkillset):
    localizacao = vLocal["Cidade"]
    while True:
        menu_HUD(localizacao)
        opcao = opcoes()

        if opcao == "1":
            print(colored("\t\t\tExplorar", "green", attrs=["bold"]))
            localizacao = move(vLocal,localizacao)
            ocorrencia = acontecimentos()

            if ocorrencia == "Inimigo Encontrado":
                print(colored("\t\t   Um Inimigo Surgiu!", "red", "on_grey", attrs=["bold"]))
                inimigo = inimigos()[localizacao[-1]]
                inimigo = random.choice(inimigo)
                combate(heroi, inimigo, vSkillset)


            if ocorrencia == "Item Achado":               
                print(colored("\n\t\t   Um Item Foi Achado", "yellow", "on_grey", attrs=["bold"]))

                heroi.encontrar_item()


            if ocorrencia == "Nada Ocorreu":
                print(colored("\n\t\t  Nada Ocorreu", "blue", "on_grey", attrs=["bold"]))


        if opcao == "2":
            print(colored("\n\t\t  Inventário", "cyan", "on_grey", attrs=["bold"]))
            heroi.mochila()

        if opcao == "3":
            print(colored("\n\t\t\tStatus", "magenta", "on_grey", attrs=["bold"]))
            heroi.status()
        
        if opcao == "4":
            print(colored("\n\t\t\tMapa", "white", "on_grey", attrs=["bold"]))
            mapa()

#region     //Cadastros\\

def mostrar_classes():
    print("\n")
    print(colored("           CLASSES DISPONIVEIS          ", "yellow", "on_grey", attrs=["bold"]))
    print("\n")
    print(colored("   🏹 Arqueiro", "cyan", attrs=["bold"]))
    print("     - Ataque: 14")
    print("     - Vida: 16")
    print("     - Defesa: 6")
    print("     - Velocidade: 6")
    print(colored("     Especialidade: Alta precisão e ataques à distância.\n", "cyan"))

    print(colored("   🗡️ Assassino", "red", attrs=["bold"]))
    print("     - Ataque: 18")
    print("     - Vida: 12")
    print("     - Defesa: 4")
    print("     - Velocidade: 8")
    print(colored("     Especialidade: Críticos e velocidade.\n", "red"))

    print(colored("   🛡️ Guerreiro", "green", attrs=["bold"]))
    print("     - Ataque: 11")
    print("     - Vida: 22")
    print("     - Defesa: 10")
    print("     - Velocidade: 4")
    print(colored("     Especialidade: Resistência e força bruta.\n", "green"))

def cadastrar_heroi(vClasse):
    print(colored("\t       CADASTRO       ", "white", "on_grey", attrs=["bold"]))
    nome = input(colored("\tHerói: ", "white", attrs=["bold"]))
    mostrar_classes()
    nome_classe = input(colored("\tClasse: ", "white", attrs=["bold"]))
    print(colored("                                      ", "white", "on_grey"))
    classe = vClasse[nome_classe]
    heroi = Heroi(nome, classe['vidamax'], classe['defesa'], classe['ataquemax'], nome_classe, classe['speed'])

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
    print("\n")
    print(colored(f"\t\t      Localização: {localizacao[-1]}      ", "white", "on_grey", attrs=["bold"]))
    print(colored("1. 🌍Explorar  |  2. 🎒Inventario  |  3. ✨Status  |  4. 🗺️ Mapa  ", "white", "on_grey", attrs=["bold"] ))

def menu_Combate():
    print(colored("\n\t\t      Combate      ", "red", attrs=["bold"]))
    print(colored("1. ⚔️ Atacar  |  2. 🌟Skills  |  3. 🧪Poções  |  4. 🏃🏽‍♂️ Fugir", "white", attrs=["bold"]))

def menu():
    print("\n")
    print(colored("\t       EUCHRONIA      ", "red", "on_grey", attrs=["bold"]))
    print(colored("\t1.       Jogar", "white", attrs=["bold"]))
    print(colored("\t2.  Cadastrar Heroi", "white", attrs=["bold"]))
    print(colored("\t3.       Sair", "white", attrs=["bold"]))
    print(colored("\t                      ", "grey", attrs=["reverse"]))

def opcoes():
    opcao = input(colored("\tOP: ", "red", attrs=["bold"]))
    while opcao not in ["1","2","3","4"]: opcao = input(colored("\t    Opção Invalida   \n\tOP: ", "red", attrs=["bold"]))
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
            controlador(vLocal,heroi,vSkillset)

        if opcao == "2":
            heroi = cadastrar_heroi(vClasse)

        if opcao == "3":
            print("Saindo do programa...")
            break

main()









