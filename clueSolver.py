# from tkinter.font import nametofont
# from tkinter.tix import InputOnly


from asyncio.windows_utils import pipe
import random

print("CLUE SOLVER")


# TODO: create list of players, in order


class Card:
    def __init__(self, name, type, place) -> None:
        self.name = name
        self.type = type    # i.e., killer / weapon / room
        self.owner = "unknown"      # might not use this
        self.placeInCardList = place
    def __repr__(self) -> str:
        output = self.name + " (" + self.type + ")"
        return output
    def getType(self):
        return self.type
    def getName(self):
        return self.name
    def setOwner(self, player):
        self.owner = player
    def getOwner(self):
        return self.owner
    def getPlaceInCardList(self):
        return self.placeInCardList

greenCard =         Card("Green", "killer", 0)
mustardCard =       Card("Mustard", "killer", 1)
peacockCard =       Card("Peacock", "killer", 2)
plumCard =          Card("Plum", "killer", 3)
scarlettCard =      Card("Scarlett", "killer", 4)
orchidCard =        Card("Orchid", "killer", 5)

candlestickCard =   Card("Candlestick", "weapon", 6)
daggerCard =        Card("Dagger", "weapon", 7)
pipeCard =          Card("Pipe", "weapon", 8)
revolverCard =      Card("Revolver", "weapon", 9)
ropeCard =          Card("Rope", "weapon", 10)
wrenchCard =        Card("Wrench", "weapon", 11)

ballroomCard =      Card("Ballroom", "room", 12)
billiardRoomCard =  Card("Billiard Room", "room", 13)
conservatoryCard =  Card("Conservatory", "room", 14)
diningRoomCard =    Card("Dining Room", "room", 15)
hallCard =          Card("Hall", "room", 16)
kitchenCard =       Card("Kitchen", "room", 17)
libraryCard =       Card("Library", "room", 18)
loungeCard =        Card("Lounge", "room", 19)
studyCard =         Card("Study", "room", 20)

cardList = [greenCard, mustardCard, peacockCard, plumCard, scarlettCard, orchidCard, candlestickCard, daggerCard, pipeCard, revolverCard, ropeCard, wrenchCard, ballroomCard, billiardRoomCard, conservatoryCard, diningRoomCard, hallCard, kitchenCard, libraryCard, loungeCard, studyCard]


class Player:
    def __init__(self, name, turn = -1) -> None:
        self.name = name
        # self.card1 = card1
        # self.card2 = card2
        # self.card3 = card3
        self.cardList = []
        self.turnOrder = turn
        self.turnOrderConfirmed = False
    def __repr__(self) -> str:
        return self.name #+ ", cards: " + self.card1 + ", " + self.card2 + ", " + self.card3
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
    def addToCardList(self, card):
        if len(self.cardList) >= 3:
            print("ERROR - there are already 3 cards held by the player")
        else:
            self.cardList.append(card)


scarlettPlayer =  Player("Scarlett", 1)
greenPlayer =     Player("Green", 2)
orchidPlayer =    Player("Orchid", 6)
mustardPlayer =   Player("Mustard", 5)
plumPlayer =      Player("Plum", 4)
peacockPlayer =   Player("Peacock", 3)
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




def askUserWhichCharacter():
        # the goal here is to be able to ask the user to name the 3 cards held by a certain player... it might not matter much beyond that...?
    printPlayerOrder(playerList, "Which character are you playing as?", False, True)
    userInputPlayer = int(input(" "))
    #use this integer to identify the user's character
    usersCharacter = Player
    for player in playerList:
        if player.getTurnOrder() == userInputPlayer:
            usersCharacter = player

    print("Which cards do you have? Please enter 3 integers on 3 separate lines.")
    #print list of all cards, with numbers
    x = 1
    while(x <= len(cardList)):
        for card in cardList:
            print("    ", end=" ")
            print(card.getPlaceInCardList(), end=" ")
            print(". ", end=" ")
            print(card.getName())
            x += 1
    #user enters the integers, each on a separate line
    userCard1 = int(input(""))
    userCard2 = int(input(""))
    userCard3 = int(input(""))

    #use self.addToCardList 3 times to add the three cards
    
    for card in cardList:
        if userCard1 == card.getPlaceInCardList():
            usersCharacter.addToCardList(card)
        if userCard2 == card.getPlaceInCardList():
            usersCharacter.addToCardList(card)
        if userCard3 == card.getPlaceInCardList():
            usersCharacter.addToCardList(card)
            
    #show the user the self.getCardList so the user can verify & possibly try again if the messed up ..........maybe later
    print("These are your cards:")
    print(usersCharacter.getCardList())







def convertTurnToPlayerTurn(turn):
    return ((turn - 1) % 6) + 1


def executeTurn(turnNumber, turnDataDictionary):
    # identify the guessing player by converting the turn number into playerTurn
    activePlayer = Player
    for player in playerList:
        if player.getTurnOrder() == convertTurnToPlayerTurn(turnNumber):
            activePlayer = player
    activePlayerName = activePlayer.getNameOnly()
    
    print("Start of TURN ", end="")
    print(turnNumber, end="")
    print(", guessing player is ", end="")
    print(activePlayerName)

    turnDataDictionary[turnNumber] = {}
    turnDataDictionary[turnNumber]['guesser'] = activePlayerName

    # prompt the player to enter info
    print("Enter the killer guessed: ")
    #           **** print a list of possible killers
    for x in range(6):
        print(str(x) + ". " + str(cardList[x].getName()))
    playerInput = int(input(""))    
    turnDataDictionary[turnNumber]["killerGuessed"] = playerInput

    print("Enter the weapon guessed: ")
    for x in range(6, 12):
        print(str(x) + ". " + str(cardList[x].getName()))
    playerInput = int(input(""))
    turnDataDictionary[turnNumber]["weaponGuessed"] = playerInput

    print("Enter the room guessed: ")
    for x in range(12, 21):
        print(str(x) + ". " + str(cardList[x].getName()))
    playerInput = int(input(""))
    turnDataDictionary[turnNumber]["roomGuessed"] = playerInput

    tempString = str(activePlayerName) + "Response"
    turnDataDictionary[turnNumber][tempString] = 'n'        # the guessing player's response is null

    # Record other player's responses
    #   the first respondent will be the one whose turnOrder is 1 higher than the guesser's
    incrementalVariable = 1
    while incrementalVariable < 6:
        respondentTurnOrder = convertTurnToPlayerTurn(turnNumber + incrementalVariable)
        for player in playerList:
            if player.getTurnOrder() == respondentTurnOrder:
                respondentName = player.getNameOnly()
                print("What was the response of " + str(respondentName) + "? n = null, d = declined to respond, r = responded")
                playerInput = str(input(""))
                tempString = str(respondentName) + "Response"            
                turnDataDictionary[turnNumber][tempString] = playerInput
        incrementalVariable += 1

    # Record the card that was shown (if known). The card number (0 thru 20) will be recorded. If unknown, set to -1
    turnDataDictionary[turnNumber]['card'] = -1
    print("Do you know what card was shown? (y/n)")
    playerInput = str(input(""))
    if playerInput == "y":
        print("What card was shown?")
        # print list of all cards, with numbers
        for card in cardList:
            print(str(card.getPlaceInCardList()) + ". " + str(card.getName()))
        playerInput = str(input(""))
        turnDataDictionary[turnNumber]['card'] = playerInput



    print(turnDataDictionary)
    print("")





def startGame():
    # askUserWhichCharacter()
    # verifyOrder(playerList)

    #                               need to initialize a blank analyzedData table?

    turnLog = {}
    # turnLog = {1: {'guesser': -1, 'killerGuessed': -1, 'weaponGuessed': -1, 'roomGuessed': -1, 'p1Response': 'noResponse', 'p2Response': 'noResponse', 'p3Response': 'noResponse', 'p4Response': 'noResponse', 'p5Response': 'noResponse', 'p6Response': 'noResponse', 'cardShown': -1} }


#   info in a TURN:
#       guesser - this is the player whose turn it is
#       what 3 cards were guessed - this will be 1 killer, 1 weapon, 1 room
#       responses - 
#           n = never asked to respond, i.e. NOT APPLICABLE... this will also be the value assigned to the guesser
#           d = declined to respond
#           r = responded
#       card (integer) - most of the time this will not be known

#   for analysis purposes, it will probably be easier to keep all guesses in 1 nested list or nested dictionary


    turn = 9
    gameFinished = False
    while (gameFinished == False): 
        executeTurn(turn, turnLog)      # turn is an int
        # print(turnLog)
        turn += 1
        if turn == 2:
            gameFinished = True



startGame()



#guesser
#killers are cards 1 thru 6     (initialized as -1)
#weapons are cards 7 thru 12
#rooms are cards   13 thru 21
#possible player responses are: noResponse, declined, responded
#cardShown is -1 if unknown, otherwise it's the card number (1 thru 21)

# turnLog = {1: {'guesser': -1, 'killerGuessed': -1, 'weaponGuessed': -1, 'roomGuessed': -1, 'p1Response': 'noResponse', 'p2Response': 'noResponse', 'p3Response': 'noResponse', 'p4Response': 'noResponse', 'p5Response': 'noResponse', 'p6Response': 'noResponse', 'cardShown': -1} }



# print(turnLog[1])
# print(" ")
# print(turnLog[1]['p1Response'])

















# example start of game:
#   startGame():
#       askUserWhichCharacter()
#       verifyOrder(playerList)

#       (initialize the turnData nested dictionary, and initialize a blank analyzedData nested list/dictionary)

#       turn = 1
#       gameFinished = False
#       while(gameFinished == False):
#           executeTurn(x)                  ... this will use the convertTurnToPlayerTurn function to know which player is making a guess
#           analyzeAllData()                .... this will always start with turn 1 and go thru all turn data
#           turn += 1
#           gameFinished = checkIfGameFinished















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





