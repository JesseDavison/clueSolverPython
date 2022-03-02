from tkinter.font import nametofont


print("CLUE SOLVER")



# TODO: create list of players, in order

class Player:
    def __init__(self, name, card1 = "(unknown)", card2 = "(unknown)", card3 = "(unknown)", turn = -1) -> None:
        self.name = name
        self.card1 = card1
        self.card2 = card2
        self.card3 = card3
        self.turnOrder = turn
    def __repr__(self) -> str:
        return self.name + ", cards: " + self.card1 + ", " + self.card2 + ", " + self.card3
    def getInfoList(self):
        return [self.name, self.card1, self.card2, self.card3]
    def getNameOnly(self):
        return self.name


scarlett =  Player("Scarlett", "kitchen", "knife", "ballroom", 1)
green =     Player("Green")
orchid =    Player("Orchid")
mustard =   Player("Mustard")
plum =      Player("Plum")
white =     Player("White")
playerList = [scarlett, green, orchid, mustard, plum, white]







def printPlayerOrder(inputList):
    print("Current player order:")
    for x in range(len(inputList)):
        print("    " + str(x + 1) + ". ", end=" ")
        print(inputList[x].getInfoList()[0])
    print("  ")


def verifyOrder(listOfPlayers):         # should return a boolean??
    playerOrderIsCorrect = False
    printPlayerOrder(listOfPlayers)
    userInput = input("Is the order correct? (y/n)")
    if(userInput == "y"):
        return True
    else:
        return False


def correctOrder():
    pass
                        # create a list of possible names... this list will be modified so just make a copy of playerList
                        # "Who is first?" (then show list of possible names)
                        # based on int input, add that name to new list, and remove that name from list of possible names

                        # or should I give each player a TURN-NUMBER property? 

# WHY AREN'T COMMENTS APPEARING?

#make a START-GAME function
# make a WHILE loop that keeps going as long as player order is incorrect (FALSE)
verifyOrder(playerList)



def whoseTurnIsIt():
    pass



# TODO: make a working turn cycle... e.g., each player enters 1 on their turn to print "hello," and the turn goes to next appropriate player


# TODO: create a (growing) list of the details of each turn.... guesser, what they guessed, who didn't respond, who did respond, what card (if known)
# TODO: create a function to accept a new guess.... turnNumber will be a parameter

# TODO: after each guess is "completed," run the analysis algorithm over every single guess




# TODO: function to display Guesses chart

# TODO: function to display Analysis chart





