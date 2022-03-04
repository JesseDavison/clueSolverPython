# from tkinter.font import nametofont
# from tkinter.tix import InputOnly


print("CLUE SOLVER")


# TODO: create list of players, in order


class Card:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type    # i.e., killer / weapon / room
        self.owner = "unknown"      # might not use this
    def __repr__(self) -> str:
        return self.name
    def getType(self):
        return self.type
    def getName(self):
        return self.name
    def setOwner(self, player):
        self.owner = player
    def getOwner(self):
        return self.owner

greenCard =         Card("Green", "killer")
mustardCard =       Card("Mustard", "killer")
peacockCard =       Card("Peacock", "killer")
plumCard =          Card("Plum", "killer")
scarlettCard =      Card("Scarlett", "killer")
orchidCard =        Card("Orchid", "killer")

candlestickCard =   Card("Candlestick", "weapon")
daggerCard =        Card("Dagger", "weapon")
pipeCard =          Card("Pipe", "weapon")
revolverCard =      Card("Revolver", "weapon")
ropeCard =          Card("Rope", "weapon")
wrenchCard =        Card("Wrench", "weapon")

ballroomCard =      Card("Ballroom", "room")
billiardRoomCard =  Card("Billiard Room", "room")
conservatoryCard =  Card("Conservatory", "room")
diningRoomCard =    Card("Dining Room", "room")
hallCard =          Card("Hall", "room")
kitchenCard =       Card("Kitchen", "room")
libraryCard =       Card("Library", "room")
loungeCard =        Card("Lounge", "room")
studyCard =         Card("Study", "room")



class Player:
    def __init__(self, name, turn = -1, card1 = "(unknown)", card2 = "(unknown)", card3 = "(unknown)") -> None:
        self.name = name
        # self.card1 = card1
        # self.card2 = card2
        # self.card3 = card3
        self.cardList = [card1, card2, card3]
        self.turnOrder = turn
        self.turnOrderConfirmed = False
    def __repr__(self) -> str:
        return self.name + ", cards: " + self.card1 + ", " + self.card2 + ", " + self.card3
    def getInfoList(self):
        return [self.name, self.turnOrder, self.card1, self.card2, self.card3]
    def getNameOnly(self):
        return self.name
    def getTurnOrder(self):
        return self.turnOrder
    def setTurnOrder(self, newTurn):
        self.turnOrder = newTurn
    def getConfirmedStatus(self):
        return self.turnOrderConfirmed
    def turnOrderConfirmedSetTrue(self):
        self.turnOrderConfirmed = True
    def getCardList(self):
        return self.cardList


scarlettPlayer =  Player("Scarlett", 3, greenCard, candlestickCard, ballroomCard)
greenPlayer =     Player("Green", 6)
orchidPlayer =    Player("Orchid", 2)
mustardPlayer =   Player("Mustard", 4)
plumPlayer =      Player("Plum", 1)
peacockPlayer =   Player("Peacock", 5)
playerList = [scarlettPlayer, greenPlayer, orchidPlayer, mustardPlayer, plumPlayer, peacockPlayer]



                        # TODO: user needs to select their character??? yes, so they can input their cards




def testForProblemsInTurnOrder(inputList):
    # print warning if turn order is messed up.... e.g., two players have same turn order, or anyone has a -1 turnOrder 
    sameTurnOrderProblem = False
    # stick all the turnOrder values into a new list, then COUNT how many times you see 1, then 2, etc
    listOfTurnOrders = []
    for name in inputList:
        listOfTurnOrders.append(name.getTurnOrder())
    x = 1
    y = len(inputList)
    while x <= y:
        if listOfTurnOrders.count(x) != 1:
            sameTurnOrderProblem = True
        x += 1
    return sameTurnOrderProblem


def printPlayerOrder(inputList, title, worryAboutProblems, printOnlyPlayersWithUnconfirmedStatus):                
    if (testForProblemsInTurnOrder(inputList) and worryAboutProblems):
            print("we've got a problem.... some players are either sharing a turnOrder, or a player's turnOrder hasn't been initialized and is still -1")
    else:    
        # if you only want to print UNCONFIRMED TURN ORDER players, run with this chunk of code        
        if (printOnlyPlayersWithUnconfirmedStatus):
            print(title)
            x = 1
            while(x <= len(inputList)):
                for playerObject in inputList:
                    if(playerObject.getTurnOrder() == x and playerObject.getConfirmedStatus() == False):
                        print("    " + str(x) + ". ", end=" ")
                        print(playerObject.getNameOnly())
                x += 1

        # if you only want to print CONFIRMED players, run with this chunk of code
        else: 
            print(title)
            x = 1
            while(x <= len(inputList)):
                for playerObject in inputList:
                    if(playerObject.getTurnOrder() == x and playerObject.getConfirmedStatus() == True):
                        print("    " + str(x) + ". ", end=" ")
                        print(playerObject.getNameOnly())
                x += 1

        # if you want to print ALL players REGARDLESS of CONFIRMED status, run with this chunk of code
        # (write this later)


def correctTheOrder(inputList):
    # user sees list of all players, in their current turnOrder, whose turnOrderConfirmed is FALSE
    #   that is, only show players with turnOrderConfirmed set to FALSE
    x = 1
    while (x <= len(inputList)):
        printPlayerOrder(inputList, "Who is player {}".format(x), False, True)   
        userInput = int(input(" "))     # user is prompted to pick who is first... user inputs an integer
                                        # for example, the user inputs 4, which is Mustard... so we need to identify which player object has self.turnOrder of 4
        for player in inputList:
            if player.getTurnOrder() == userInput and player.getConfirmedStatus() == False:
                player.setTurnOrder(x)
                player.turnOrderConfirmedSetTrue()
        x += 1


def verifyOrder(inputList):         # should return a boolean? yay or nay?
    printPlayerOrder(inputList, "Current player order (using verifyOrder function)", False, True)
    userInput = input("Is this order correct? (y/n)")
    if(userInput == "y"):
            # set each player as CONFIRMED
        for player in inputList:
            player.turnOrderConfirmedSetTrue()
    else:
        correctTheOrder(inputList)
        printPlayerOrder(inputList, "Final player order:", False, False)


printPlayerOrder(playerList, "Which character are you playing as?", False, True)
userInput = input(" ")


# verifyOrder(playerList)





#make a START-GAME function



def whoseTurnIsIt():
    pass














# TODO: make a very basic but still-working turn cycle... e.g., each player enters 1 on their turn to print "hello," and the turn goes to next appropriate player


# TODO: create a (growing) list of the details of each turn.... guesser, what they guessed, who didn't respond, who did respond, what card (if known)
#               maybe use a dictionary of dictionaries e.g., 
#                               {
#                                   1: {guesser: scarlett, killerGuessed: plum,    weaponGuessed: candlestick, roomGuessed: ballroom}.........},
#                                   2: {guesser: plum,     killerGuessed: mustard, weaponGuessed: dagger,      roomGuessed: lounge  }.........},

#                               }

# SHOULD PROBABLY LEARN MORE ABOUT DATA REPRESENTATION IN PYTHON, BEFORE TACKLING THIS, e.g. "Visualize Data with Python," on Codecademy.com


# TODO: create a function to accept a new guess.... turnNumber will be a parameter

# TODO: after each guess is "completed," run the analysis algorithm over every single guess




# TODO: function to display Guesses chart

# TODO: function to display Analysis chart





