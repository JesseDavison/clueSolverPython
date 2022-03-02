from tkinter.font import nametofont


print("CLUE SOLVER")



# TODO: create array of players, in order

class Player:
    def __init__(self, name, card1 = "(unknown)", card2 = "(unknown)", card3 = "(unknown)") -> None:
        self.name = name
        self.card1 = card1
        self.card2 = card2
        self.card3 = card3
    def __repr__(self) -> str:
        return self.name + ", cards: " + self.card1 + ", " + self.card2 + ", " + self.card3
    def getInfoList(self):
        return [self.name, self.card1, self.card2, self.card3]
    def getNameOnly(self):
        return self.name


scarlett =  Player("Scarlett", "kitchen", "knife", "ballroom")
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




def verifyAndCorrectOrder():
    playerOrderIsCorrect = False
    printPlayerOrder(playerList)
    
    while(playerOrderIsCorrect == False):
        
        userInput = input("Is the order correct? (y/n)")       

        if(userInput == "y"):
            playerOrderIsCorrect = True
            print("yay!", end=" ")
        else:
            namesToPickFrom = {1: scarlett, 2: green, 3: orchid, 4: mustard, 5: plum, 6: white}   
            firstSecondEtc = ["first", "second", "third", "fourth", "fifth", "sixth"]
            newOrder = []

            iterator = 0
            while (len(namesToPickFrom) > 0):
                print("Who is " + firstSecondEtc[iterator])
                iterator += 1
                x = 1
                for key, value in namesToPickFrom.items():
                    print(x, end=" ")
                    print(". ", end=" ")
                    print(value.getNameOnly())
                    x += 1
                userInput = int(input(""))
                newOrder.append(namesToPickFrom.get(userInput))
                del namesToPickFrom[userInput]                              # this line is a problem because the user input won't necessarily match the dictionary key
        printPlayerOrder(newOrder)          
    return newOrder     # return corrected player order list

playerList = verifyAndCorrectOrder()









# TODO: create a (growing) list of the details of each turn.... guesser, what they guessed, who didn't respond, who did respond, what card (if known)
# TODO: create a function to accept a new guess.... turnNumber will be a parameter

# TODO: after each guess is "completed," run the analysis algorithm over every single guess




# TODO: function to display Guesses chart

# TODO: function to display Analysis chart





