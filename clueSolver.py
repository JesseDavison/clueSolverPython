# from tkinter.font import nametofont
# from tkinter.tix import InputOnly


from asyncio.windows_utils import pipe
from collections import UserString
from imghdr import what
import random
# import json
import ast

print("CLUE SOLVER")




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
    def getNumberAndName(self):
        tempString = str(self.placeInCardList) + ". " + str(self.name)
        return tempString
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
    def __init__(self, name, turn = -1, column = -1) -> None:
        self.name = name
        self.card1 = Card
        self.card2 = Card
        self.card3 = Card
        self.cardList = []
        self.turnOrder = turn
        self.turnOrderConfirmed = False
        self.columnNumber = column          # this is the column this player will ALWAYS have in the analysisTable
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
    
    def addCard1(self, card):
        self.card1 = card
    def addCard2(self, card):
        self.card2 = card
    def addCard3(self, card):
        self.card3 = card
    def getCard1(self):
        return self.card1
    def getCard2(self):
        return self.card2
    def getCard3(self):
        return self.card3

    def getColumnNumber(self):
        return self.columnNumber





scarlettPlayer =  Player("Scarlett", 1, 0)
greenPlayer =     Player("Green", 2, 1)
orchidPlayer =    Player("Orchid", 6, 5)
mustardPlayer =   Player("Mustard", 5, 4)
plumPlayer =      Player("Plum", 4, 3)
peacockPlayer =   Player("Peacock", 3, 2)
playerList = [scarlettPlayer, greenPlayer, orchidPlayer, mustardPlayer, plumPlayer, peacockPlayer]




def askUserInputInt(choices, promptText):
    while True:
        try:
            garbage = -9999
            while garbage not in choices:
                garbage = int(input(promptText))
            return garbage
        except ValueError as e:
                print("Ya done fucked up your typing. You need to type an INTEGER. Try again.")

def askUserInputChar(choices, promptText):
    while True:
        try:
            garbage = ""
            while garbage not in choices:
                garbage = str(input(promptText))
            return garbage
        except ValueError as e:
                print("Ya done fucked up your typing. You need to type a CHARACTER. Try again.")


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
        # userInput = int(input(" "))     # user is prompted to pick who is first... user inputs an integer
                                        # for example, the user inputs 4, which is Mustard... so we need to identify which player object has self.turnOrder of 4
        userInput = askUserInputInt([1, 2, 3, 4, 5, 6], "")
        for player in inputList:
            if player.getTurnOrder() == userInput and player.getConfirmedStatus() == False:
                player.setTurnOrder(x)
                player.turnOrderConfirmedSetTrue()
        x += 1


def verifyOrder(inputList):         # should return a boolean? yay or nay?
    printPlayerOrder(inputList, "Current player order (using verifyOrder function)", False, True)
    # userInput = input("Is this order correct? (y/n)")
    userInput = askUserInputChar(["y", "n"], "Is this order correct? (y/n):  ")
    if(userInput == "y"):
            # set each player as CONFIRMED
        for player in inputList:
            player.turnOrderConfirmedSetTrue()
    else:
        correctTheOrder(inputList)
        printPlayerOrder(inputList, "Final player order:", False, False)




def askUserWhichCharacter(loadFromFileUserCharacter = -12, loadFromFileCard1 = -11, loadFromFileCard2 = -11, loadFromFileCard3 = -11):
        # the goal here is to be able to ask the user to name the 3 cards held by a certain player... it might not matter much beyond that...?

    usersCharacter = Player    
    if loadFromFileUserCharacter != -12:
        usersCharacter = loadFromFileUserCharacter
    else:
        printPlayerOrder(playerList, "Which character are you playing as?", False, True)
        # userInputPlayer = int(input(" "))
        userInputPlayer = askUserInputInt([1, 2, 3, 4, 5, 6], "")
        #use this integer to identify the user's character
        for player in playerList:
            if player.getTurnOrder() == userInputPlayer:
                usersCharacter = player

    userCard1 = -5
    userCard2 = -5
    userCard3 = -5
    if loadFromFileCard1 != -11:
        userCard1 = loadFromFileCard1
        userCard2 = loadFromFileCard2
        userCard3 = loadFromFileCard3
    else:
        print("Which cards do you have? Please enter 3 integers on 3 separate lines.")
        #print list of all cards, with numbers
        x = 1
        while(x <= len(cardList)):
            for card in cardList:
                print("    ", end=" ")
                print(card.getNumberAndName())
                x += 1
        #user enters the integers, each on a separate line
        possibleCards = [x for x in range(21)]
        userCard1 = askUserInputInt(possibleCards, "First Card. Type a number from 0 to 20: ")
        userCard2 = askUserInputInt(possibleCards, "Second Card. Type a number from 0 to 20: ")
        userCard3 = askUserInputInt(possibleCards, "Third Card. Type a number from 0 to 20: ")

    #use self.addToCardList 3 times to add the three cards
    
    for card in cardList:
        if userCard1 == card.getPlaceInCardList():
            usersCharacter.addToCardList(card)
            usersCharacter.addCard1(card)
        if userCard2 == card.getPlaceInCardList():
            usersCharacter.addToCardList(card)
            usersCharacter.addCard2(card)
        if userCard3 == card.getPlaceInCardList():
            usersCharacter.addToCardList(card)
            usersCharacter.addCard3(card)
            
    #show the user the self.getCardList so the user can verify & possibly try again if the messed up ..........maybe later
    print("These are your cards:")
    print(usersCharacter.getCardList())

    return usersCharacter






def convertTurnToPlayerTurn(turn):
    return ((turn - 1) % 6) + 1


def executeTurn(turnNumber, turnDataDictionary):
    # identify the guessing player by converting the turn number into playerTurn
    activePlayer = Player
    for player in playerList:
        if player.getTurnOrder() == convertTurnToPlayerTurn(int(turnNumber)):
            activePlayer = player
    activePlayerName = activePlayer.getNameOnly()
    
    print("Start of TURN ", end="")
    print(turnNumber, end="")
    print(", guessing player is ", end="")
    print(activePlayerName)

    turnDataDictionary[turnNumber] = {}
    turnDataDictionary[turnNumber]['guesser'] = activePlayerName

    # prompt the player to enter info
    # print("Enter the killer guessed: ")
    #           **** print a list of possible killers
    for x in range(6):
        print(str(x) + ". " + str(cardList[x].getName()))
    playerInput = askUserInputInt([x for x in range(6)], "Enter the killer guessed: ")
    turnDataDictionary[turnNumber]["killerGuessed"] = playerInput

    # print("Enter the weapon guessed: ")
    for x in range(6, 12):
        print(str(x) + ". " + str(cardList[x].getName()))
    playerInput = askUserInputInt([x for x in range(6, 12)], "Enter the weapon guessed: ")
    turnDataDictionary[turnNumber]["weaponGuessed"] = playerInput

    # print("Enter the room guessed: ")
    for x in range(12, 21):
        print(str(x) + ". " + str(cardList[x].getName()))
    playerInput = askUserInputInt([x for x in range(12, 21)], "Enter the room guessed: ")
    turnDataDictionary[turnNumber]["roomGuessed"] = playerInput

    # set the player responses to a default of null. We're doing it here so the order in which the players appear is consistent between turns
    for player in playerList:
        turnDataDictionary[turnNumber][str(player.getNameOnly()).lower() + "Response"] = "n"
        
    # Record other player's responses
    #   the first respondent will be the one whose turnOrder is 1 higher than the guesser's... hence the incrementalVariable = 1
    #   as soon as 1 player responds (r), stop asking if the other players responded... hence didSomeoneRespond = False
    didSomeoneRespond = False
    incrementalVariable = 1
    while incrementalVariable < 6:
        respondentTurnOrder = convertTurnToPlayerTurn(turnNumber + incrementalVariable)
        for player in playerList:
            if player.getTurnOrder() == respondentTurnOrder:
                respondentName = player.getNameOnly()
                if didSomeoneRespond == False:
                    # print("What was the response of " + str(respondentName) + "? n = null (wasn't asked), d = declined to respond, r = responded")
                    playerInput = askUserInputChar(["n", "d", "r"], "What was the response of " + str(respondentName) + "? n = null (wasn't asked), d = declined, r = responded:  ")
                    tempString = str(respondentName).lower() + "Response"            
                    turnDataDictionary[turnNumber][tempString] = playerInput
                    
                    if playerInput == "r":
                        didSomeoneRespond = True
                else:
                    continue        # we already set all responses to null (n) as a default, so this is fine
        incrementalVariable += 1

    # Record the card that was shown (if known). The card number (0 thru 20) will be recorded. If unknown, set to -1
    turnDataDictionary[turnNumber]['card'] = -1
    # print("Do you know what card was shown? (y/n)")
    playerInput = askUserInputChar(["y", "n"], "Do you know what card was shown? (y/n):  ")
    if playerInput == "y":
        print("What card was shown?")
        # print list of all cards, with numbers
        for card in cardList:
            print(card.getNumberAndName())
        playerInput = askUserInputInt([x for x in range(21)], "What card was shown?:  ")
        turnDataDictionary[turnNumber]['card'] = playerInput

    # print out the turns, for reference
    for x in range(turnNumber):
        turnNum = x + 1
        print(str(turnNum) + ": ", end="")
        print(turnDataDictionary[turnNum])
    print("")


    # open file for writing
    f = open("turnInfo.txt", "w")

    # write file
    f.write(str(turnDataDictionary))
    # close file
    f.close()





def analyzeData(turnNumber, turnData, analyTable, user, killerWeaponRoom):

    # if turnNumber == 1:
    #       turning this off so we can paste in old games and start at turnNumber > 1
    card1 = user.getCard1()
    card2 = user.getCard2()
    card3 = user.getCard3()

    column = user.getColumnNumber()
    #   the row number is simply the card's id #
    row1 = card1.getPlaceInCardList()
    row2 = card2.getPlaceInCardList()
    row3 = card3.getPlaceInCardList()

    #   now, we change the analysis table to reflect the fact that these cards' owner is known
    analyTable[row1][column] = ["Y"]
    analyTable[row2][column] = ["Y"]
    analyTable[row3][column] = ["Y"]


    def howManyYsInColumn(columnNum):
        numberOfYs = 0
        for row in range(21):
            if "Y" in analyTable[row][columnNum]:
                numberOfYs += 1
        return numberOfYs




    #   next, mark those rows with "-" to indicate it's impossible that other players have those same cards
    def processYsHorizontal():
        __incrementalRow = 0
        while __incrementalRow < 21:
            __incrementalColumn = 0
            while __incrementalColumn < 6:
                if "Y" in analyTable[__incrementalRow][__incrementalColumn]:
                    for x in range(6):
                        if x != __incrementalColumn and "*****" not in analyTable[__incrementalRow][x]:
                            analyTable[__incrementalRow][x] = ["-"]
                __incrementalColumn += 1
            __incrementalRow += 1
        checkForAllNegativesInRow(killerWeaponRoom)


#   if a player has 3xY in their column, then we know they do NOT have any other cards
#   if a player has two "Y" in their column and one "?", then we know that "?" is actually a "Y"
    def processYsVertical():
        #   look down each column and count up how many Ys we see
        for __column in range(6):
            __numberOfYs = 0
            __locationOfYs = []
            __numberOfQuestionMarks = 0            
            __locationOfQuestionMarks = []
            for row in range(21):
                if "Y" in analyTable[row][__column]:
                    __numberOfYs += 1
                    __locationOfYs.append(row)
                if "?" in analyTable[row][__column]:
                    __numberOfQuestionMarks += 1
                    __locationOfQuestionMarks.append(row)
                if __numberOfYs > 3:
                    print("THERE ARE TOO MANY Ys IN COLUMN " + str(__column))
            if __numberOfYs == 3:
                for y in range(21):
                    if y not in __locationOfYs and "*****" not in analyTable[y][__column]:
                        analyTable[y][__column] = ["-"]
            if __numberOfYs == 2 and __numberOfQuestionMarks == 1:
                # set the "?" to become a "Y"
                analyTable[__locationOfQuestionMarks[0]][__column] = ["YES", "Y"]  # it has "YES" for now, for debugging purposes
        checkForAllNegativesInRow(killerWeaponRoom)


    def checkForAllNegativesInRow(kWR):
        #   if a row has all "-", we know that that card is in the envelope, so let's print a bunch of **** for the user's convenience

        # look at row 0 of the analysis table. If there is a "-" in every column (0 thru 5), then set each cell to = ["*****"] (has 11 * characters)
        for __row in range(21):
            __numberOfNegatives = 0
            for __column in range(6):                
                if "-" in analyTable[__row][__column]:
                    __numberOfNegatives += 1
            if __numberOfNegatives == 6:
                # for __column in range(6):
                #     analyTable[__row][__column] = []
                #     analyTable[__row][__column].append("*****")   # instead of marking the analyTable with ***** let's just announce that the card is known
                
                if __row < 6:
                    # print("THE KILLER IS KNOWN")
                    # set the global "known" variable here
                    kWR[0] = cardList[__row].getName()
                if __row > 5 and __row < 12:
                    # print("THE WEAPON IS KNOWN")
                    kWR[1] = cardList[__row].getName()
                if __row > 11:
                    # print("THE ROOM IS KNOWN")
                    kWR[2] = cardList[__row].getName()


    def checkForLastRemainingQuestionMarkInCategory():
        pass


    def checkForSingleTurnNumbersInColumn():
        #   if a turnNumber appears only once in a column, we know that that player has that card
        #   loop thru each column, one at a time:
        for __column in range(6):
            # initialize a tally list for that column, to keep track of how many times we see each turn number appear
            #   the tally list answers the question, "How many times does turn 1 appear in the entire analysis table column? 0, 1, 2 or 3 times?"
            __tally = {}
            for __turn in range(turnNumber):
                __tally[__turn + 1] = 0
            # if we look at a cell, and see for example [4, 5], then we do: tally[4] += 1, and tally[5] += 1
            for row in range(21):
                for x in range(turnNumber):
                    __turnNumbah = x + 1
                    if __turnNumbah in analyTable[row][__column]:
                        __tally[__turnNumbah] += 1
            # now we've got our tally list... and we check to see if any turn# appears ONLY ONCE in the tally dictionary
            for __turn in range(turnNumber):
                if __tally[__turn + 1] == 1:
                    print("WE IDENTIFIED A LONE TURN " + str(__turn + 1) + " IN COLUMN " + str(__column))
                    # because we know that the turn number exists only once, we know that the player has that card... so we need to change that turn number into a "Y"
                    # but we don't know the exact location within the analysisTable ... all we know is that for example there is "one 6 in Orchid's column"
                    #   so we know the column, and we can cycle thru the rows and replace (turn + 1) with "Y"
                    for row in range(21):
                        if (__turn + 1) in analyTable[row][__column]:
                            analyTable[row][__column] = ["Y"]



        #   at end of this function, run horiz/vert again, because we may have added a "Y" into the analysisTable
        processYsHorizontal()       
        processYsVertical() 



    #   we need some nested functions to handle:
    #       decline to respond (d)
    #           mark a "-" for each player who declines, for those three cards  *DONE*
    #           every time a new "-" appears, we need to check whether that affects/refines info we learned in previous turns
    #       respond by showing a card (r)
    #           if we don't know what card was shown, then we replace the "?" with the turn number, indicating that on that turn one of those 3 cards is held by the player
    #           if the card is known, then the ONLY THING we put into the analyTable is the "Y" for the owner of the card, and we remove everything else
    #           every time a new Y appears in the table, we need to run horizontal & vertical processing
    #
    #       check columns to see if a turn number appears all by itself... if so, then we know ......

    def processDecline():
        #   identify all players who declined ... i.e., scarlettResponse == 'd', mustardResponse == 'd', etc, and mark all three card in that guess as "-" for that respondent
        
        for __x in range(turnNumber):
        
            __killerRowNum = turnData[__x + 1]['killerGuessed']
            __weaponRowNum = turnData[__x + 1]['weaponGuessed']
            __roomRowNum = turnData[__x + 1]['roomGuessed']

            for __player in playerList:
                __nameString = __player.getNameOnly().lower() + "Response"
                if turnData[__x + 1][__nameString] == 'd' and "*****" not in analyTable[__killerRowNum][__player.getColumnNumber()]:
                    analyTable[__killerRowNum][__player.getColumnNumber()] = ["-"]
                    analyTable[__weaponRowNum][__player.getColumnNumber()] = ["-"]
                    analyTable[__roomRowNum][__player.getColumnNumber()] = ["-"]  
   
            checkForAllNegativesInRow(killerWeaponRoom)
            checkForSingleTurnNumbersInColumn()         #   if there is indeed a single turnNumber in a column, what is the best way to handle it? recursively run the turn over again? 
                                                        #   Or just turn that turnNumber into a "Y" and call it good? If so, we can add a "cleanup" step at end of turn to see if 
                                                        #   there is any conclusive info the user can benefit from. .... we want the conclusive info presented ASAP
                                                        #         


    def processRespond():
        for __x in range(turnNumber):

            __killerRowNum = turnData[__x + 1]['killerGuessed']
            __weaponRowNum = turnData[__x + 1]['weaponGuessed']
            __roomRowNum = turnData[__x + 1]['roomGuessed']

            __isTheShownCardKnown = False
            if turnData[__x + 1]['card'] != -1:
                __isTheShownCardKnown = True

            #   going to append the turnNumber into the cell's list, and remove "?" if it is there
            for __player in playerList:
                __nameString = __player.getNameOnly().lower() + "Response"
                if turnData[__x + 1][__nameString] == 'r':
                    #   if the card is known then don't enter turnNumbers... only enter "Y"
                    if __isTheShownCardKnown:
                        __cardNumber = turnData[__x + 1]['card']
                        whatWasRemoved = []
                        whatWasRemoved = analyTable[__cardNumber][__player.getColumnNumber()]
                        analyTable[__cardNumber][__player.getColumnNumber()] = ["Y"]
                        # IMMEDIATELY we need to clear out turn numbers from past guesses (whatWasRemoved), before checkForSingleTurnNumbersInColumn() screws it up by accidentally
                        #   leaving a lone turnNumber in a cell (and thereby making future analysis incorrectly think that that lone number indicates the card is held)
                        #       in other words, if where we just put a "Y", this cell was associated with previous turns, we need to deactivate those turns, i.e. .remove() them
                        #           go down the column in the analysis table, and check each cell for all the turn numbers in whatWasRemoved
                        for row in range(21):
                            for element in whatWasRemoved:
                                if element in analyTable[row][__player.getColumnNumber()] and element in [x+1 for x in range(turnNumber)]: # i.e. we don't want to remove "Y" or "?"
                                    analyTable[row][__player.getColumnNumber()].remove(element)



                    #   if there is a "Y" in any of the three cards that were just guessed, then don't bother recording the turnNumbers bc for all we know they showed that "Y" card
                    elif "Y" in analyTable[__killerRowNum][__player.getColumnNumber()] or "Y" in analyTable[__weaponRowNum][__player.getColumnNumber()] or "Y" in analyTable[__roomRowNum][__player.getColumnNumber()]:
                        continue
                    else:    #  if there's no "-" already, and we don't already know that player's 3 cards, then add the turn number
                        if "-" not in analyTable[__killerRowNum][__player.getColumnNumber()] and howManyYsInColumn(__player.getColumnNumber()) < 3:
                            if (__x + 1) not in analyTable[__killerRowNum][__player.getColumnNumber()] and "*****" not in analyTable[__killerRowNum][__player.getColumnNumber()]:
                                analyTable[__killerRowNum][__player.getColumnNumber()].append(__x + 1)
                        if "-" not in analyTable[__weaponRowNum][__player.getColumnNumber()] and howManyYsInColumn(__player.getColumnNumber()) < 3:
                            if (__x + 1) not in analyTable[__weaponRowNum][__player.getColumnNumber()] and "*****" not in analyTable[__weaponRowNum][__player.getColumnNumber()]:
                                analyTable[__weaponRowNum][__player.getColumnNumber()].append(__x + 1)
                        if "-" not in analyTable[__roomRowNum][__player.getColumnNumber()] and howManyYsInColumn(__player.getColumnNumber()) < 3:
                            if (__x + 1) not in analyTable[__roomRowNum][__player.getColumnNumber()] and "*****" not in analyTable[__roomRowNum][__player.getColumnNumber()]:
                                analyTable[__roomRowNum][__player.getColumnNumber()].append(__x + 1)

                        # if "?" in analyTable[__killerRowNum][__player.getColumnNumber()]:
                        #     analyTable[__killerRowNum][__player.getColumnNumber()].remove("?")
                        # if "?" in analyTable[__weaponRowNum][__player.getColumnNumber()]:
                        #     analyTable[__weaponRowNum][__player.getColumnNumber()].remove("?")
                        # if "?" in analyTable[__roomRowNum][__player.getColumnNumber()]:
                        #     analyTable[__roomRowNum][__player.getColumnNumber()].remove("?")
            processYsHorizontal()        # because this function can sometimes result in "Y"s being added, these 2 (horiz/vert) need to be run afterwards, every time
            processYsVertical()          # because this function can sometimes result in "Y"s being added, these 2 (horiz/vert) need to be run afterwards, every time
            checkForAllNegativesInRow(killerWeaponRoom)
            checkForSingleTurnNumbersInColumn()


    for x in range(10):
        processYsHorizontal()       # these two (horiz/vert) are run first thing in order to incorporate the user's 3 known cards
        processYsVertical()         # these two (horiz/vert) are run first thing in order to incorporate the user's 3 known cards
        processDecline()
        processRespond()            # there will always be 1 response, and possibly some declines, so always run these

    #add "cleanup" functionality here, in case the previous processes have revealed some important info ... because we want to show this info to the user before the next turn starts







def printAnalysisTable(table, actualKillerWeaponRoom):
    print("ANALYSIS TABLE:")
    print("                             Killer is: " + str(actualKillerWeaponRoom[0]))
    print("                             Weapon is: " + str(actualKillerWeaponRoom[1]))
    print("                             Room is: " + str(actualKillerWeaponRoom[2]))
    print("----------------------------------------------------------------------------------------------------------------------")    
    print("".ljust(20, " "), end="")
    print("scarlett".center(15, ' '), "green".center(15, ' '), "peacock".center(15, ' '), "plum".center(15, ' '), "mustard".center(15, ' '), "orchid".center(15, ' '), " |")
    for row in range(21):
        # create a blank row to separate each category of cards:
        if row == 6 or row == 12 or row == 17:
            print("                                                                                                                     |")
        print(cardList[row].getNumberAndName().ljust(20, " "), end="")
        for column in range(6):
            # if the output would be "-" then just leave it blank, otherwise print it
            if "-" in table[row][column]:
                print("-".center(15, ' '), end=" ")
            else:
                print(str(table[row][column]).center(15, ' '), end=" ")
        print(" |")
    print("----------------------------------------------------------------------------------------------------------------------")    
    print(" ")



def startGame():
    userCharacter = askUserWhichCharacter()
    verifyOrder(playerList)

    # print("Do you want to load a previous game? (y/n)")
    userInput = askUserInputChar(["y", "n"], "Do you want to load a previous game? (y/n):  ")
    if userInput == "y":
        
        with open("turnInfo.txt") as f:

            # pull out the second line, which will have card1
            #   use f.readline() instead of f.read()....???
            # pull out card2

            # pull out card3

            # pull out the last turn completed????  deal with this later

            # pull out the huge turn log
            
            
            data = f.read()
        turnLog = ast.literal_eval(data)



        # print("what was the last turn that was completed? Look at the .txt file if you're not sure.")
        turnNumber = askUserInputInt([x for x in range(99)], "What was the last turn that was completed? Look at the .txt file if you're not sure. :  ")
        turnNumber += 1
        
    else:

        
    # initialize a blank data table (nested dictionary) to record the events of each turn
        turnLog = {}
        turnNumber = 1
    # example of what a turn will look like:
    # turnLog = {1: {'guesser': -1, 'killerGuessed': -1, 'weaponGuessed': -1, 'roomGuessed': -1, 'p1Response': 'noResponse', 'p2Response': 'noResponse', 'p3Response': 'noResponse', 'p4Response': 'noResponse', 'p5Response': 'noResponse', 'p6Response': 'noResponse', 'cardShown': -1} }
    #   info in a TURN:
    #       guesser - this is the player whose turn it is
    #       what 3 cards were guessed - this will be 1 killer, 1 weapon, 1 room
    #       responses - 
    #           n = never asked to respond, i.e. NOT APPLICABLE... this will also be the value assigned to the guesser
    #           d = declined to respond
    #           r = responded
    #       card (integer) - most of the time this will not be known

    # initialize an analysis table
    #   columns, then rows
    # analysisTable = [["?"]*6]*21        # can't initialize with this technique because it creates a "shallow list", see https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
    analysisTable = [[ ["?"] for i in range(6)] for j in range(21)]

    # actualKiller = "unknown"
    # actualWeapon = "unknown"
    # actualRoom = "unknown"
    actualKillerWeaponRoom = ["unknown", "unknown", "unknown"]

    gameFinished = False
    while (gameFinished == False): 
        executeTurn(turnNumber, turnLog)      
        analyzeData(turnNumber, turnLog, analysisTable, userCharacter, actualKillerWeaponRoom)
        printAnalysisTable(analysisTable, actualKillerWeaponRoom)
        # print(turnLog)
        turnNumber += 1
        if turnNumber == 55:
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



























# SHOULD PROBABLY LEARN MORE ABOUT DATA REPRESENTATION IN PYTHON, BEFORE TACKLING THIS, e.g. "Visualize Data with Python," on Codecademy.com





# TODO: function to display Guesses chart






