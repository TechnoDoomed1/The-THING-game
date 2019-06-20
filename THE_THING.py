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
names.append('YOU')
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
    if 'YOU' in things:
        print('*** You\'re now a "THING": Survive and infect. ***')
        print("All of the following survivors are \"things\":", things)
        input('')
    else:
        print('*** You\'re still a human. Kill all "things" to win. ***\n')
    
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
            print(names[k], "chooses to:\t", end='')

            # Went scouting or stays at the base?
            if names[k] in scouts:
                print("investigate outside.")
            elif names[k] in stays:
                print("stay at the base.")

    print("-------------------------------------------------------------",
          "------------------", sep='')

    # Now, it's up to you what you choose to do. Remember that you won't be
    # able to choose if you went scouting last turn.
    if 'YOU' not in scouts:
        option = ''
        while option not in ['scout','stay']:
            option = input("(*) What do you choose to do: scout, or stay? ")

        if option == 'scout':
            stays.remove('YOU')
            scouts.append('YOU')
        else:
            pass
        
    else:
        print("\n(*) You're suspicious of infection since you went outside.",
              "The rest of the\nsurvivors force you to not leave the base.\n")
        scouts.remove('YOU')
        stays.append('YOU')


    # Now, in the staying group, the testing starts. If you're there, and you
    # aren't a "thing", you can choose to either let things be like normal:
    # 8 survivors chosen at random, or become leader and test 8 others you want.
    # It may only be done twice per game, and never during the 1st turn.
    # Notice that if only 2 or less human survivors remain in the group, the
    # staying group is overrun and converted instantly.

    if len([x for x in stays if x in scientists]) <= 2:
        print("The group staying at the base is overrun by \"things\" from the",
              "inside.\nNone of them are any longer human.")
        option = []
    
    elif ('YOU' in stays) and (turn_count>1) and (special<2) and len(stays)>8:
        print("(*) You can now become leader and test 8 scientists you choose",
              " that stayed at\nthe base. Should any be a \"thing\", it will",
              " be killed.\n[Write full uppercase names -- USES LEFT: ",
              2-special, "]", sep='')
        option = input("(*) Proceed: yes or no? ")
        
        if option.lower() == 'yes':
            special += 1
            print("Introduce the name of the 8 survivors to test:")
            
            option = []
            while len(option)!=8 or (False in [x in stays for x in option]):
                option = input('')
                option = option.split(' ')
        else:
            option = sample(stays, 8)
            print("The scientists that stay at the base test 8 at random:")
            print(option, "\n")

    elif len(stays)>8:
        option = sample(stays, 8)
        print("The scientists that stay at the base test 8 at random:")
        print(option, "\n")
        
    else:
        print("Everyone in the base is tested.")
        option = stays


    # Any "thing" that is tested is revealed and killed.
    killed = 0 # How many "things" have been killed this turn?
    
    for x in option:
        if (x in things) and (x in stays):
            print(x, 'has been revealed to be a "thing" and has been killed.')
            stays.remove(x)
            things.remove(x)
            dead.append(x)
            killed += 1

    if option and killed == 0:
        print("No results.", end=' ')


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

    if len(scientists)!=0 and len(things)!=0 and ('YOU' not in dead):
        print("Now, 2 persons of each group could have become a \"thing\".")
        print("\nTURN ENDS.")
        print("=============================================================",
              "==================", sep='')
        input('')
        turn_count += 1
        turn()
    elif 'YOU' in dead:
        print("G A M E      O V E R")
    elif len(scientists)==0:
        print("The \"things\" win the game and destroy humankind!", end=' ')
        print("Congratulations!")
    elif len(things)==0:
        print("The human scientists have destroyed all the \"Things\"", end=' ')
        print("and won! Congratulations!")

#------------------------------------------------------------------------------
def play():
    turn()

if __name__ == "__main__":
    # When the module is run, the game starts.
    play()
#------------------------------------------------------------------------------
