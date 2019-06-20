'''"The Thing" game'''

from random import randrange, sample
rand = lambda x, y: randrange(x, y)

#------------------------------------------------------------------------------
# Preparation of the game. List of the names of each scientist, plus you.
# At the start of the game, random characters are chosen at random to be "the
# thing" (it can even be you). Your goal is to survive until the very end.

names = sample(['Alison', 'Charlotte', 'Rachel', 'Amelia', 'Mary', 'Freya',
                'Ruby', 'Jessica', 'Grace', 'Jack', 'Thomas', 'Oliver', 'Jason',
                'Joshua', 'Samuel', 'Alex', 'David', 'George', 'Noah'], 19)
names.append('TÚ')
#------------------------------------------------------------------------------
scientists = names[:] # Copy 'names' list to be the scientists.
things = sample(names, 2) # Choose 2 random characters to start as "things".

# The starting "things" are NOT scientists anymore.
for x in things:
    scientists.remove(x)

#------------------------------------------------------------------------------
scouts, stays = [], names[:] # The scouting and staying parties.
dead = [] # Keeps track of all dead "things". Dead humans are not counted
          # since they are immediately transformed into "things".

special = 0 # How many times has the player become leader? Can be done twice.
turn_count = 1 # Turn count.
#------------------------------------------------------------------------------
def turn ():
    global special, turn_count
    
    # At the start of the turn, the player is informed if they are human.
    if 'TÚ' in things:
        print('*** Ahora eres una "COSA": Sobrevive e infecta. ***')
        print("Los siguientes supervivientes son \"COSAS\":", things)
        input('')
    else:
        print('*** Aún eres humano. Descubre y mata a todas las "COSAS"',
              ' para ganar ***\n', sep='')
    
    # All characters choose to either go scout, or stay. The 'scout' option
    # has 15% probability to happen, while the 'stay' option has 85%. The
    # probability to go scouting increases 5% per turn.

    for k in range(0, 19):
        # Gets a random number from 1 to 100.
        choice = rand(1, 100)

        # Dead characters are of no importance and can't choose.
        if names[k] in dead:
            pass

        # Scouts can't repeat if they already went scouting last turn.
        elif names[k] in scouts:
            scouts.remove(names[k])
            stays.append(names[k])

        # If it's a thing, there is more than 1 "thing" and it didn't scout...
        # Then it does, but still 1 thing must be left at the base.
        # This does NOT apply during the 1st turn, which is the most telltale.
        elif (names[k] in things) and (len(things)>1) and (names[k] in stays):
            if turn_count!= 1 and len([x for x in stays if x in things])>1:
                stays.remove(names[k])
                scouts.append(names[k])

        # If not a thing, and it didn't scout last turn, choice is random.
        # Remember, 15% chance to choose scouting vs 85% chance to stay.
        # The probability to go scouting increases 5% per turn.
        elif choice <= 10 + 5*turn_count:
            stays.remove(names[k])
            scouts.append(names[k])

        # Finally, print on-screen the result.
        # DEAD or not?
        if names[k] not in dead:
            print(names[k], "decide:    \t", end='')

            # Went scouting or stays at the base?
            if names[k] in scouts:
                print("salir a investigar afuera.")
            elif names[k] in stays:
                print("quedarse en la base.")

    print("-------------------------------------------------------------",
          "------------------", sep='')

    # Now, it's up to you what you choose to do. Remember that you won't be
    # able to choose if you went scouting last turn.
    if 'TÚ' not in scouts:
        option = ''
        while option not in ['investigar','quedarse']:
            option = input("(*) Qué decides hacer (investigar/quedarse)? ")

        if option == 'investigar':
            stays.remove('TÚ')
            scouts.append('TÚ')
        else:
            pass
        
    else:
        print("\n(*) Estás bajo sospecha de infección al haber salido antes.",
              " El resto de\nsupervivientes te fuerzan a quedarte en la base.",
              sep='')
        scouts.remove('TÚ')
        stays.append('TÚ')


    # Now, in the staying group, the testing starts. If you're there, and you
    # aren't a "thing", you can choose to either let things be like normal:
    # 8 survivors chosen at random, or become leader and test 8 others you want.
    # It may only be done twice per game, and never during the 1st turn.
    # Notice that if only 2 or less human survivors remain in the group, the
    # staying group is overrun and converted instantly.

    if len([x for x in stays if x in scientists]) <= 2:
        print("El grupo de supervivientes que había en la base ha sido tomado",
              "por \"COSAS\"\ndesde dentro. Ya nadie es humano.", sep='')
        option = []
    
    elif ('TÚ' in stays) and (turn_count>1) and (special<2) and len(stays)>8:
        print("(*) Ahora puedes convertirte en líder y testar a 8 científicos",
              " de los que se\nhan quedado en la base que tú elijas. Si alguno",
              " es una \"COSA\" morirá.\n[Escribe los nombres separados por",
              "espacio. -- USOS RESTANTES: ", 2-special, "]\n", sep='')
        option = input("(*) Proceder a liderar el grupo (s/n)? ")
        
        if option.lower() == 's':
            special += 1
            print("Introduce los nombres de los 8 supervivientes a testar:")
            
            option = []
            while len(option)!=8 or (False in [x in stays for x in option]):
                option = input('')
                option = option.split(' ')
        else:
            option = sample(stays, 8)
            print("Los supervivientes de la base testean a 8 de ellos al azar:")
            print(option, "\n")

    elif len(stays)>8:
        option = sample(stays, 8)
        print("Los supervivientes de la base testean a 8 de ellos al azar:")
        print(option, "\n")
        
    else:
        print("Todo el mundo en la base es testado.")
        option = stays


    # Any "thing" that is tested is revealed and killed.
    killed = 0 # How many "things" have been killed this turn?
    
    for x in option:
        if (x in things) and (x in stays):
            if x != 'TÚ':
                print(x, 'era una "COSA" y ha sido eliminado/a.')
            else:
                print(x, 'has sido descubierto y te han matado.')
            stays.remove(x)
            things.remove(x)
            dead.append(x)
            killed += 1

    if option and killed == 0:
        print("Sin resultados.")


    # The "things" can convert 2 characters per group.
    #
    # If there are scouting "things", they turn a scientist into a thing if
    # there's only one possibility, and two scientists if there are 2 or more
    # possible victims.
    if len([x for x in scouts if x in things])!=0:
        possible_victims = [x for x in scouts if x in scientists]
        
        if possible_victims != []:
            infected = sample(possible_victims, 1)
            scientists.remove(infected[0])
            things.append(infected[0])

    if len([x for x in stays if x in things])!=0:
        possible_victims = [x for x in stays if x in scientists]
        
        if possible_victims != []:
            infected = sample(possible_victims, 1)
            scientists.remove(infected[0])
            things.append(infected[0])

    if len([x for x in scouts if x in things])!=0:
        possible_victims = [x for x in scouts if x in scientists]
        
        if possible_victims != []:
            infected = sample(possible_victims, 1)
            scientists.remove(infected[0])
            things.append(infected[0])
        
    if len([x for x in stays if x in things])!=0:
        possible_victims = [x for x in stays if x in scientists]
        
        if possible_victims != []:
            infected = sample(possible_victims, 1)
            scientists.remove(infected[0])
            things.append(infected[0])
    

    # End of the turn. Continue if the game hasn't finished, otherwise give
    # the victory or the loss to the player.

    if len(scientists)!=0 and len(things)!=0 and ('TÚ' not in dead):
        print("Ahora, 2 personas de cada grupo pueden haberse convertido.", end=' ')
        print("FIN DEL TURNO.")
        print("=============================================================",
              "==================", sep='')
        input('')
        turn_count += 1
        turn()
    elif 'TÚ' in dead:
        print("G A M E      O V E R")
    elif len(scientists)==0:
        print("Las \"COSAS\" ganan el juego y acaban con la humanidad!", end=' ')
        print("Felicidades!")
    elif len(things)==0:
        print("Los científicos humanos han identificado y destruido a",
              "todas las \"COSAS\" y han\nganado.Enhorabuena!", sep='')

#------------------------------------------------------------------------------
def play():
    turn()

# When the module is run, the game starts.
if __name__ == "__main__":
    print("==================================================================")
    print(" Bienvenido al juego de la \"COSA\", basado en la saga de películas")
    print(" homónimas de 1951, 1982 y 2011. Un grupo de científicos humanos")
    print(" entre los que tú te encuentras, han descubierto una forma de vida")
    print(" alienígena bajo el hielo ártico en un aparente letargo. No obstante,")
    print(" el monstruo que albergaba se ha despertado y ahora amenaza con")
    print(" mataros a todos.\n")
    print(" El juego es simple: como humano, tienes que sobrevivir y destruir")
    print(" a todas las \"COSAS\" que encuentres. Pero no lo tendrás fácil,")
    print(" pues estos seres pueden parecer humanos y son muy peligrosos...")
    print(" Los científicos han descubierto un modo de testarse los unos a los")
    print(" otros para descubrir si son o no humanos, pero que alguien haya")
    print(" sido probado humano no significa que después lo sea... pues las")
    print(" \"COSAS\" convierten en más de los suyos a sus víctimas.\n")
    print(" Si te convierten, jugar como \"COSA\" es más simple: evita que")
    print(" te descubran, y convierte a todos los humanos para escapar del")
    print(" ártico y destruir a la humanidad.\n")
    print(" Buena suerte!! [PULSA ENTER PARA CONTINUAR]")
    input('')
    print("==================================================================")
    play()
#------------------------------------------------------------------------------

