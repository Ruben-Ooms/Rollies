from random import randrange as rand

class DNDRoller:
    def __init__(self):
        self.dice=[]
        self.total=0
        self.numMod=[]

    def parser(self,unParsed):
        # understands the user input for number of dice, 
        # number of sides, and modifiers

        # n is number of dice
        # m is sides of die
        # a is modifier
        for uP in unParsed:
            # get numerical modifier total
            if(uP.find("+")!=-1):
                numMods=uP.split("+")[1:]
                uP=uP.split("+")[0]
                tempNumMod=0
                for n in numMods:
                    if(n.lstrip("-").isnumeric()):
                        tempNumMod+=int(n)
                    else:
                        print("Numerical modifiers must be positive integers.\n")
                        return True
                self.numMod.append(tempNumMod)
            else:
                self.numMod.append(0)
            
            # if no d is found
            if(uP.find("d")==-1): 
                n="1" # 1 die needs to be rolled
                m=uP # and die is the input
            else: # if d is found
                # if multiple d error
                if(uP.count("d")>1):
                    print("Individual input can not contain more than one 'd'.\n")
                    return True
                # before d is how many die need to be rolled and after is faces
                n=uP.split("d")[0] 
                m=uP.split("d")[1]

            # if n is not numeric error
            if(not n.isdigit() or int(n)==0):
                print("Number of die must be positive integer.\n")
                return True
            n=int(n)

            # if multiple modifiers error
            modCount=0
            modList=["A","D","E"]
            for i in modList:
                modCount+=m.count(i);
            if(modCount>1):
                print("Only one modifier can be applied at once.\n")
                return True

            # setting modifier
            if(m.find("A")!=-1): # advantage
                a="advantage"
                m=m.split("A")[0]
            elif(m.find("D")!=-1): # disadvantage
                a="disadvantage"
                m=m.split("D")[0]
            elif(m.find("E")!=-1): # emphasis
                a="emphasis"
                m=m.split("E")[0]
            else:
                a="none"

            # if m is not numeric error
            if(not m.isdigit() or int(m)==0):
                print("Number of faces must be a positive integer.\n")
                return True
            m=int(m)

            self.dice.append(Die(n,m,a))
        return False

    def release(self):
        # release the die to roll all of them

        for d in self.dice:
            d.roll()

    def result(self):
        # creates a result string to be printed in main

        result=""
        for i in range(len(self.dice)):
            d=self.dice[i]
            # special print for 1 die being rolled
            if(d.n==1):
                result+=f"Result for {d.m}"
            else:
                result+=f"Result for {d.n}d{d.m}"

            # special print events
            dieResult=""
            if(d.a=="advantage"): # advantage
                dieResult+=" with advantage"
            elif(d.a=="disadvantage"): # disadvantage
                dieResult+=" with disadvantage"
            elif(d.a=="emphasis"): # emphasis
                dieResult+=" with emphasis"
            if(self.numMod[i]!=0):
                if(d.a=="none"):
                    dieResult+=f" with {self.numMod[i]} modifier"
                else:
                    dieResult+=f" and {self.numMod[i]} modifier"
            dieResult+=".\n"

            # if there are bad values
            if(d.a!="none" and d.n>1):
                # print row of bad values
                dieResult+="\tUnused rolls: "
                width=[];
                for n in range(len(d.badValues)):
                    v=d.values[n]+self.numMod[i]
                    b=d.badValues[n]+self.numMod[i]
                    width.append(len(str(max(v,b))))
                    dieResult+=f"{b:>{width[n]}} "
                dieResult+="\n"
                # print row of good values
                dieResult+="\tUsed rolls:   "
                for n in range(len(d.values)):
                    v=d.values[n]+self.numMod[i]
                    dieResult+=f"{v:>{width[n]}} "
            # if there are only good values
            elif(d.n>1): 
                dieResult+="\tRolls: "
                for n in range(len(d.values)):
                    dieResult+=f"{d.values[n]+self.numMod[i]} "
            # only 1 roll with bad roll
            elif(d.a!="none"): 
                # print bad value
                v=d.values[0]+self.numMod[i]
                b=d.badValues[0]+self.numMod[i]
                dieResult+="\tUnused roll: "
                width=len(str(max(v,b)))
                dieResult+=f"{b:>{width}} "
                dieResult+="\n"
                # print good value
                dieResult+="\tUsed roll:   "
                dieResult+=f"{v:>{width}} "
            # only 1 roll, no bad roll
            else: 
                dieResult+="\tRoll: "
                dieResult+=f"{d.values[0]+self.numMod[i]}"

            # print subtotal of rolls
            d.totaler()
            if(d.n>1 and len(self.dice)>1):
                tempTotal=d.total+d.n*self.numMod[i]
                dieResult+=f"\n\tSubtotal: {tempTotal}\n"
                self.total+=tempTotal
            else:
                dieResult+="\n"
                self.total+=d.total+self.numMod[i]
            result+=dieResult.replace(str(d.m+self.numMod[i]),f"\033[1;4m{d.m+self.numMod[i]}\033[0m")
        
        # print final total
        result+=f"Total: {self.total}\n" 
        return result

    def help(self):
        # return DND help string

        helpStr="""
    This app can perform roles for DND. 
    These include single, multi die, advantage, disadvantage, and emphasis rolls.

    Basic Rolls:
    To perform a single roll, enter a single number.
    To perform a multiroll, enter the number of dice and then the number of die sides seperated by a "d". Example: 5d6

    Roll Modifiers:
    To perform a roll with advantage, append an "A" to a basic roll.
    To perform a roll with disadvantage, append a "D" to a basic roll.
    To perform a roll with emphasis, append an "E" to a basic roll.
    A numerical modifier can be used by appending a "+x" where x is the number you wish to add. Example: 8+5

    Multiple rolls can be performed at once by adding a space between them. However, only one modifier can be applied to each roll, excluding numerical modifier.
"""
        return helpStr

class AnimonRoller:
    def __init__(self):
        self.dice=[]
        self.total=0
        self.b=[]
        self.s=[]

    def parser(self,unParsed):
        # understands the user input for number of dice and modifiers

        # n is number of dice
        # a is modifier
        for uP in unParsed:
            self.b.append(uP.count("B"))
            self.s.append(uP.count("S"))
            n=uP.split("B")[0]
            n=n.split("S")[0]

            # if n is not numeric error
            if(not n.isdigit() or int(n)==0):
                print("Number of die must be positive integer.\n")
                return True
            n=int(n)

            animonDieSides=6
            a="none"
            self.dice.append(Die(n,animonDieSides,a))
        return False

    def release(self):
        # release the die to roll all of them

        for d in self.dice:
            d.roll()

    def result(self):
        # creates a result string to be printed in main

        result=""
        #d=self.dice[0]
        for i in range(len(self.dice)):
            d=self.dice[i]
            result+=f"Result for {d.n} rolls"

            # special print events
            offset=self.b[i]-self.s[i]
            if(offset>0): # totall boost
                if(offset==1):
                    result+=f" with {offset} boost"
                else:
                    result+=f" with {offset} boosts"
            elif(offset<0): # total setback
                if(offset==-1):
                    result+=f" with {abs(offset)} setback"
                else:
                    result+=f" with {abs(offset)} setbacks"
            result+=".\n"

            # if there is more than 1 roll
            dieResult=""
            if(d.n>1): 
                dieResult+="\tRolls: "
                for i in range(len(d.values)):
                    dieResult+=f"{d.values[i]} "
            # only 1 roll
            else: 
                dieResult+="\tRoll: "
                dieResult+=f"{d.values[0]} "
            result+=dieResult.replace(str(d.m),f"\033[1;4m{d.m}\033[0m")

            # print number of successes of rolls
            successes=0
            for i in range(len(d.values)):
                if d.values[i]>3-offset:
                    successes+=1
            #result+=f"\n\tSuccesses: {successes}\n"
            result+=f"Successes: {successes}\n"
            

        return result

    def help(self):
        # return Animon help string

        helpStr="""
    This app can perform roles for Animon.
    All roles are performed with a d6. So the user must enter the number of d6 to roll.

    Roll Modifiers:
    To perform a roll with a setback, append an "S" to a basic roll.
    To perform a roll with boost, append a "B" to a basic roll.
    Multiple can be appended and the effective number of setbacks or boosts will be caluclated.

    Multiple rolls can be performed at once by adding a space between them.
"""
        return helpStr

class Die:
    def __init__(self,n,m,a):
        self.n=n # number of die
        self.m=m # sides on die
        self.a=a # modifier
        self.badValues=[]
        self.values=[]
        self.total=0

    def roll(self):
        # rolls the dice

        # if no advantage or disadvantage
        if(self.a=="none"):
            for i in range(self.n):
                self.values.append(rand(1,self.m+1))
            return
        # has a modifier
        for i in range(self.n):
            a=rand(1,self.m+1)
            b=rand(1,self.m+1)
            # advantage
            if(self.a=="advantage"):
                self.badValues.append(min(a,b))
                self.values.append(max(a,b))
            # disadvantage
            elif(self.a=="disadvantage"):
                self.badValues.append(max(a,b))
                self.values.append(min(a,b))
            # emphasis
            elif(self.a=="emphasis"):
                d1=abs(a-self.m/2)
                d2=abs(b-self.m/2)
                # if both are equivalent you take that roll
                if(a==b):
                    self.values.append(a)
                    self.badValues.append(b)
                # if both are equidistant from (number of sides)/2
                # then must reroll 1 and take its result
                elif(d1==d2):
                    self.values.append(rand(1,self.m+1))
                    self.badValues.append(0)
                elif(d1>d2):
                    self.values.append(a)
                    self.badValues.append(b)
                else:
                    self.values.append(b)
                    self.badValues.append(a)

    def totaler(self):
        # finds the total of that roll

        for i in self.values:
            self.total+=i

def getGame():
    # ensures the user enters a valid game
    print("Enter DND or Animon to select game.")
    game=""
    validGames=["DND","ANIMON"]
    while(game.upper() not in validGames):
        game=input("Enter game: ")
        game=game.split(" ")[0]
        if(game.upper()=="DND"):
            game=game.upper()
        else:
            game=game.title()   
    return game

def helper():
    helperStr="""    Enter "help" for an explanation of how to roll in this game.
    Enter "select" to change game.
    Enter "exit" to exit the program.
"""
    return helperStr

def main():
    # setup of the program
    game=getGame()
    print(helper())
    print("Game set to",game+".")
    # main program loop
    while(True):
        # initalize the game roller
        if(game.upper()=="DND"):
            tray=DNDRoller()
        elif(game.upper()=="ANIMON"):
            tray=AnimonRoller()

        userIn=input("Enter dice roll(s): ")
        # special cases for user non roll inputs
        if(userIn.upper()=="HELP"):
            print(tray.help())
            continue
        elif(userIn.upper()=="SELECT"):
            print()
            game=getGame()
            print("\nGame changed to",game+".")
            print(helper())
            continue
        elif(userIn.upper()=="EXIT"):
            quit()

        # split input for each roll
        individualUP=userIn.split()
        # parse the input
        if(tray.parser(individualUP)): # has an error
            continue
        # roll all the dice
        tray.release()
        # print the result of the rolls
        print(tray.result())    

if __name__=="__main__":
    main()