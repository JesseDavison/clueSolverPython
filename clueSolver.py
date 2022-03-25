# from tkinter.font import nametofont
# from tkinter.tix import InputOnly


from asyncio.windows_utils import pipe
from collections import UserString
from dis import disco
import filecmp
from imghdr import what
from operator import index
import random
# import json
import ast
import os           # to be able to use os.scandir() to get the list of possible gameSaves to load
import datetime     # to be able to timestamp new files that are created
# from kivy.app import App


print("CLUE SOLVER")

numberOfFunctionCalls = 0       # keeping track of how much processing is being done, for the sake of becoming more efficient

initialAnalysisCompletedOfLoadedSavedGame = [False, False]
initialAnalysisCompletedOfLoadedSavedGame[0] = False    # this will toggle to True after the first time processDecline() is run, after a saved game is loaded
initialAnalysisCompletedOfLoadedSavedGame[1] = False    # this will toggle to True after the first time processRespond() is run, after a saved game is loaded

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


def correctTheOrder(inputList, playerOrderForFile):
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
                playerOrderForFile.append(player.getNameOnly())
                # print("TESTING TESTING TESTING: " + str(playerOrderForFile))
                player.turnOrderConfirmedSetTrue()
        x += 1


def verifyOrder(inputList, uniqueFileName):         # should return a boolean? yay or nay?
    printPlayerOrder(inputList, "Current player order (using verifyOrder function)", False, True)
    # userInput = input("Is this order correct? (y/n)")
    userInput = askUserInputChar(["y", "n"], "Is this order correct? (y/n):  ")
    playerOrderForFile = []
    if(userInput == "y"):
        # this is the default player order:
        playerOrderForFile = ['Scarlett', 'Green', 'Peacock', 'Plum', 'Mustard', 'Orchid']
            # set each player as CONFIRMED
        for player in inputList:
            player.turnOrderConfirmedSetTrue()
    else:
        correctTheOrder(inputList, playerOrderForFile)
        printPlayerOrder(inputList, "Final player order:", False, False)
    # print("about to write the player Order to the file... it looks like: " + str(playerOrderForFile))
    fileObject = open(uniqueFileName, 'a')
    fileObject.write(str(playerOrderForFile) + "\n")
    fileObject.write("this is a temporary line 5, to be replaced by the first instance of turnDataDictionary. This line exists to prevent an index error\n")
    fileObject.write("this is a temporary line 6, where the last completed turn # will go")
    fileObject.close()    




def askUserWhichCharacter(uniqueFileName):
        # the goal here is to be able to ask the user to name the 3 cards held by a certain player... it might not matter much beyond that...?

    usersCharacter = Player    
    printPlayerOrder(playerList, "Which character are you playing as?", False, True)
    # userInputPlayer = int(input(" "))
    userInputPlayer = askUserInputInt([1, 2, 3, 4, 5, 6], "")
    #use this integer to identify the user's character
    for player in playerList:
        if player.getTurnOrder() == userInputPlayer:
            usersCharacter = player

    # write this info to file
    fileObject = open(uniqueFileName, 'w')
    fileObject.write(str(usersCharacter.getNameOnly()) + "\n")
    fileObject.close()

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
    fileObject = open(uniqueFileName, 'a')
    fileObject.write(str(userCard1) + "\n")
    fileObject.close()

    possibleCards.remove(userCard1)
    userCard2 = askUserInputInt(possibleCards, "Second Card. Type a number from 0 to 20: ")
    fileObject = open(uniqueFileName, 'a')
    fileObject.write(str(userCard2) + "\n")
    fileObject.close()

    possibleCards.remove(userCard2)
    userCard3 = askUserInputInt(possibleCards, "Third Card. Type a number from 0 to 20: ")
    fileObject = open(uniqueFileName, 'a')
    fileObject.write(str(userCard3) + "\n")
    fileObject.close()


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



def printTurnsPretty(turnNumber, turnDataDictionary):
    print("")
    print("TURN SUMMARY:")
    print("                      -------GUESSED------       ------------------RESPONSES-----------------             ")
    print("turnNum  Guesser      killer   wep    room       scar    green   orchid  must    plum    peac    cardShown")

    for x in range(turnNumber):
        turnNum = x + 1
        print(str(turnNum).ljust(2, " ") + "".center(7, " ") + str(turnDataDictionary[turnNum]['guesser']).ljust(13, " "), end="")
        print(str(turnDataDictionary[turnNum]['killerGuessed']).ljust(9, " "), end="")
        print(str(turnDataDictionary[turnNum]['weaponGuessed']).ljust(7, " ") + str(turnDataDictionary[turnNum]['roomGuessed']).ljust(11, " "), end="")
        print(str(turnDataDictionary[turnNum]['scarlettResponse']).ljust(8, " ") + str(turnDataDictionary[turnNum]['greenResponse']).ljust(8, " "), end="")
        print(str(turnDataDictionary[turnNum]['orchidResponse']).ljust(8, " ") + str(turnDataDictionary[turnNum]['mustardResponse']).ljust(8, " "), end="")
        print(str(turnDataDictionary[turnNum]['plumResponse']).ljust(8, " ") + str(turnDataDictionary[turnNum]['peacockResponse']).ljust(8, " "), end="")
        print(str(turnDataDictionary[turnNum]['card']).ljust(8, " "))
    print("")



def convertTurnToPlayerTurn(turn):
    return ((turn - 1) % 6) + 1


def executeTurn(turnNumber, turnDataDictionary, uniqueFileName):
    # identify the guessing player by converting the turn number into playerTurn
    activePlayer = Player
    for player in playerList:
        if player.getTurnOrder() == convertTurnToPlayerTurn(int(turnNumber)):
            activePlayer = player
    activePlayerName = activePlayer.getNameOnly()
    
    print("Start of TURN " + str(turnNumber) + ", guessing player is " + str(activePlayerName))

    turnDataDictionary[turnNumber] = {}
    turnDataDictionary[turnNumber]['guesser'] = activePlayerName

    for x in range(6):
        print(str(x) + ". " + str(cardList[x].getName()))
    playerInput = askUserInputInt([-1, 0, 1, 2, 3, 4, 5], "Enter the killer guessed (enter -1 if a guess wasn't able to be made):  ")
    turnDataDictionary[turnNumber]["killerGuessed"] = playerInput

    for x in range(6, 12):
        print(str(x) + ". " + str(cardList[x].getName()))
    playerInput = askUserInputInt([-1, 6, 7, 8, 9, 10, 11], "Enter the weapon guessed (enter -1 if a guess wasn't able to be made):  ")
    turnDataDictionary[turnNumber]["weaponGuessed"] = playerInput

    for x in range(12, 21):
        print(str(x) + ". " + str(cardList[x].getName()))
    playerInput = askUserInputInt([-1, 12, 13, 14, 15, 16, 17, 18, 19, 20], "Enter the room guessed (enter -1 if a guess wasn't able to be made):  ")
    turnDataDictionary[turnNumber]["roomGuessed"] = playerInput

    # set the player responses to a default of null. We're doing it here so the order in which the players appear is consistent between turns
    # for player in playerList:
    #     turnDataDictionary[turnNumber][str(player.getNameOnly()).lower() + "Response"] = "n"
    for x in range(6):
        for player in playerList:
            if x+1 == player.getTurnOrder():
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
    playerInput = askUserInputChar(["y", "n"], "Do you know what card was shown? (y/n):  ")
    if playerInput == "y":
        print("What card was shown?")
        # print list of all cards, with numbers
        for card in cardList:
            print(card.getNumberAndName())
        playerInput = askUserInputInt([x for x in range(21)], "What card was shown?:  ")
        turnDataDictionary[turnNumber]['card'] = playerInput

    # print out the turns in the terminal, for reference
    printTurnsPretty(turnNumber, turnDataDictionary)

    # copy the current contents of the turnInfo.txt file, and then replace the turnDataDictionary line with the newest turnDataDictionary
    with open(uniqueFileName, 'r') as fileObject:
        currentContents = fileObject.readlines()
    
    currentContents[5] = str(turnDataDictionary) + "\n"         # replace turnDataDictionary with the newest version
    currentContents[6] = str(turnNumber)                        # records the most recent completed turn (for the purpose of loading an old game)

    with open(uniqueFileName, 'w') as fileObject:
        fileObject.writelines(currentContents)






def analyzeData(turnNumber, turnData, analyTable, user, killerWeaponRoom, announces):

    # if turnNumber == 1:
    #       turning this off so we can paste in old games and start at turnNumber > 1
    card1 = user.getCard1()
    card2 = user.getCard2()
    card3 = user.getCard3()

    column = user.getColumnNumber()     # identify the user's player's column number
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

    def processYsHorizontal():      # if a row contains a 'Y', then mark all other cells in that row with '-' because it's impossible that another player also has that cardu
        global numberOfFunctionCalls
        numberOfFunctionCalls += 1
        for row in range(21):
            for column in range(6):
                if "Y" in analyTable[row][column]:
                    for x in range(6):
                        if x != column:
                            analyTable[row][x] = ["-"]
                            ################## CALL FUNCTION(S) HERE 
                            functionsToCallIfNegativeAdded()
                            # allFunctions()


#   if a player has three Ys in their column, then we know they do NOT have any other cards
#   if a player has two Ys in their column and one ?, then we know that "?" is actually a "Y"
#   if a player has two Ys in their column and 1 to 3 other cells with a turnNumber, then we know that all '?'-only cells in the column should be changed to '-'
#   if a player has one Y  in their column and two distinct "groups" of turnNumbers, then we know that all '?'-only cells in the column should be changed to '-'
    def processYsVertical():        
        global numberOfFunctionCalls
        numberOfFunctionCalls += 1
        #   look down each column and count up how many Ys we see
        for column in range(6):
            numberOfYs = 0
            locationOfYs = []
            numberOfQuestionMarks = 0            
            locationOfQuestionMarks = []
            doAtLeastTwoCellsShareATurnNumber = False
            # tally up the Ys and ?s
            for row in range(21):
                # tally up the Ys
                if "Y" in analyTable[row][column]:
                    numberOfYs += 1
                    locationOfYs.append(row)
                if numberOfYs > 3:
                    print("THERE ARE TOO MANY Ys IN COLUMN " + str(column))
                # tally up the ?s
                if "?" in analyTable[row][column]:
                    numberOfQuestionMarks += 1
                    locationOfQuestionMarks.append(row)

            if numberOfYs == 3:     #   if a player has three Ys in their column, then we know they do NOT have any other cards
                for y in range(21):
                    if y not in locationOfYs and "-" not in analyTable[y][column]:
                        analyTable[y][column] = ["-"]
                        print("THREE Ys WERE FOUND IN COLUMN " + str(column) + ", SO THE CELL AT ROW " + str(y) + " WAS MARKED WITH '-'")
                        ############## CALL FUNCTION(S) HERE
                        functionsToCallIfNegativeAdded()
                        # allFunctions()
            if numberOfYs == 2 and numberOfQuestionMarks == 1:      #   if a player has two Ys in their column and one ?, then we know that the "?" should be changed to "Y"
                analyTable[locationOfQuestionMarks[0]][column] = ["Y"]  
                print("COLUMN " + str(column) + " WAS FOUND TO HAVE TWO Ys AND ONE ?, SO WE TURNED THE ? AT ROW " + str(locationOfQuestionMarks[0]) + " INTO A Y.")
                #### CALL FUNCTION(S) HERE
                functionsToCallIfYAdded()
                functionsToCallIfQuestionMarkRemoved()
                functionsToCallIfTurnNumberRemoved()
                # allFunctions()

            # if a player has two Ys in their column and 1 to 3 other cells with a turnNumber, then we know that all '?'-only cells in the column should be changed to '-'                
            # check whether there are at least 2 cells that share a turnNumber
            for x in range(turnNumber):
                for row in range(21):               # this chunk of code was backed up by one shift-tab
                    if (x+1) in analyTable[row][column]:
                        for rrow in range(21):
                            if (x+1) in analyTable[rrow][column] and row != rrow:        
                                doAtLeastTwoCellsShareATurnNumber = True
            if numberOfYs == 2 and doAtLeastTwoCellsShareATurnNumber:
                for row in range(21):
                    if analyTable[row][column] == ["?"]:
                        analyTable[row][column] = ["-"]
                        print("(vertical function) COLUMN " + str(column) + " HAD TWO Ys AND AT LEAST ONE OTHER SET OF turnNUMBERS, SO AT ROW " + str(row) + " WE REPLACED THE LONE ? WITH '-'")
                        ########### CALL FUNCTION HERE    
                        functionsToCallIfQuestionMarkRemoved()
                        functionsToCallIfTurnNumberRemoved()
                        functionsToCallIfNegativeAdded()                    
                        # allFunctions()

            #   if a player has one Y  in their column and two distinct "groups" of turnNumbers, then we know that all '?'-only cells in the column should be changed to '-'
            if numberOfYs == 1:       # don't bother will all this crap if numberOfYs isn't 1
#######################################################################################################################################################
#######################################################################################################################################################
##########################       START      #############################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
                groupXCells = [ [] for i in range(10)]          # for example, groupXCells[1] = []          is a list of the cells in group 1
                groupXTurnNumbers = [ [] for i in range(10)]	# for example, groupXTurnNumbers[1] = []    is a list of the turnNumbers in group 1
                # we're assuming that there will never be more than 10 groups... doesn't feel like a dangerous assumption in a six player game.....

                def putCellIntoGroupNumber(rowNumber, columnNumber, cellsInGroup, turnNumbersInGroup, groupNumber):	 # this function should only be called on cells with turnNumber(s)
                    if cellsInGroup[groupNumber] == []:                      # if there are no cells in this group, then... 
                        cellsInGroup[groupNumber].append(rowNumber)          # add this cell/rowNumber to groupXCells[groupNumber]
                        for turnNumber in analyTable[rowNumber][columnNumber]:  # ... and add these turnNumbers to groupXTurnNumbers
                            if turnNumber not in turnNumbersInGroup[groupNumber] and isinstance(turnNumber, int):   # don't want redundant duplicates, and we don't want non-integers
                                turnNumbersInGroup[groupNumber].append(turnNumber)    
                    else:  # if groupXCells is NOT empty, or in other words if this group already has cells attached to it,
                        doesTheNewCellHaveTurnNumbersThatAreAlreadyInTheGroup = False
                        for turnNumber in analyTable[rowNumber][columnNumber]:
                            if turnNumber in turnNumbersInGroup[groupNumber] and isinstance(turnNumber, int):
                                doesTheNewCellHaveTurnNumbersThatAreAlreadyInTheGroup = True
                        if doesTheNewCellHaveTurnNumbersThatAreAlreadyInTheGroup:
                            cellsInGroup[groupNumber].append(rowNumber)                 # add this cell to cellsInGroup
                            for turnNumber in analyTable[rowNumber][columnNumber]:      # and add these turnNumbers to turnNumbersInGroup
                                if turnNumber not in turnNumbersInGroup[groupNumber] and isinstance(turnNumber, int):       # ...without adding duplicates
                                    turnNumbersInGroup[groupNumber].append(turnNumber)
                        else: # if NONE of the turnNumbers in this cell are in groupXTurnNumbers, then try to add them to a different group:
                            putCellIntoGroupNumber(rowNumber, columnNumber, cellsInGroup, turnNumbersInGroup, groupNumber + 1)		# recursion - this will end on its own eventually


                # save all non-Y, non-'-', non-?-only cells to a list
                listOfCellsInColumnWithTurnNumbers = []
                for row in range(21):
                    if 'Y' not in analyTable[row][column] and '-' not in analyTable[row][column] and analyTable[row][column] != ['?']:
                        listOfCellsInColumnWithTurnNumbers.append(row)         # these cells will have '?' in them but that shouldn't matter

                if column == 1:
                    print("listOfCells: " + str(listOfCellsInColumnWithTurnNumbers))
                    for element in listOfCellsInColumnWithTurnNumbers:
                        print(analyTable[element][column])
                        print("done")

                def useThe_putCellsIntoGroupNumber_functionInAnOrderThatDoesntBreakThings(listOfCells):
                    # pick one of the biggest cells to start with
                    biggestCellSize = -1
                    for cell in listOfCells:            # 'cell' is a row number
                        if len(analyTable[cell][column]) > biggestCellSize:
                            biggestCellSize = len(analyTable[cell][column])
                    indexOfOneOfBiggestCells = -1
                    for cell in listOfCells:
                        if len(analyTable[cell][column]) == biggestCellSize:
                            indexOfOneOfBiggestCells = cell
                            # break

                    # identify the turnNumbers contained in that "biggest" cell
                    turnNumbersInBiggestCell = []
                    for element in analyTable[indexOfOneOfBiggestCells][column]:
                        if element != '?':
                            turnNumbersInBiggestCell.append(element)
                    if column == 1:
                        print("turnNumbersInBiggestCell: " +str(turnNumbersInBiggestCell))

                    # identify any cells that DO NOT SHARE any turnNumbers with our "biggest" cell
                    cellsThatDoNotShareTurnNumbers = []     # again, remember that "cell" = row number in the analyTable
                    for cell in listOfCells:
                        cellDoesShareTurnNumbersWithBiggestCell = False
                        for turnNum in turnNumbersInBiggestCell:
                            if turnNum in analyTable[cell][column]:
                                cellDoesShareTurnNumbersWithBiggestCell = True
                        if cellDoesShareTurnNumbersWithBiggestCell == False:
                            cellsThatDoNotShareTurnNumbers.append(cell)
                    cellsThatDoDoDoDoDoShareTurnNumbers = []                # we'll make a parallet list, so we can process these cells first
                    for cell in listOfCells:
                        if cell not in cellsThatDoNotShareTurnNumbers:
                            cellsThatDoDoDoDoDoShareTurnNumbers.append(cell)

                    
                    if column == 1:
                        print("cellsThatDoNotShareTurnNumbers: " + str(cellsThatDoNotShareTurnNumbers))
                        print("cellsThatDoDoDoDoDoShareTurnNumbers: " + str(cellsThatDoDoDoDoDoShareTurnNumbers))

                    # now process every cell that doesn't fit in 'cellsThatDoNotShareTurnNumbers'
                    for cell in cellsThatDoDoDoDoDoShareTurnNumbers:
                        putCellIntoGroupNumber(cell, column, groupXCells, groupXTurnNumbers, 0)

                    # now that that is done, we start again, this time defining our "biggest" cell again from the cellsThatDoNotShareTurnNumbers
                    if len(cellsThatDoNotShareTurnNumbers) > 0:
                        useThe_putCellsIntoGroupNumber_functionInAnOrderThatDoesntBreakThings(cellsThatDoNotShareTurnNumbers)


                useThe_putCellsIntoGroupNumber_functionInAnOrderThatDoesntBreakThings(listOfCellsInColumnWithTurnNumbers)    




















                # # pick one of the biggest cells to start with
                # biggestCellSize = -1
                # for cell in listOfCellsInColumnWithTurnNumbers:            # 'cell' is a row number
                #     if len(analyTable[cell][column]) > biggestCellSize:
                #         biggestCellSize = len(analyTable[cell][column])
                # indexOfOneOfBiggestCells = -1
                # for cell in listOfCellsInColumnWithTurnNumbers:
                #     if len(analyTable[cell][column]) == biggestCellSize:
                #         indexOfOneOfBiggestCells = cell
                #         # break

                # # identify the turnNumbers contained in that "biggest" cell
                # turnNumbersInBiggestCell = []
                # for element in analyTable[indexOfOneOfBiggestCells][column]:
                #     if element != '?':
                #         turnNumbersInBiggestCell.append(element)
                # if column == 1:
                #     print("turnNumbersInBiggestCell: " +str(turnNumbersInBiggestCell))

                # # identify any cells that DO NOT SHARE any turnNumbers with our "biggest" cell
                # cellsThatDoNotShareTurnNumbers = []     # again, remember that "cell" = row number in the analyTable
                # for cell in listOfCellsInColumnWithTurnNumbers:
                #     cellDoesShareTurnNumbersWithBiggestCell = False
                #     for turnNum in turnNumbersInBiggestCell:
                #         if turnNum in analyTable[cell][column]:
                #             cellDoesShareTurnNumbersWithBiggestCell = True
                #     if cellDoesShareTurnNumbersWithBiggestCell == False:
                #         cellsThatDoNotShareTurnNumbers.append(cell)
                # cellsThatDoDoDoDoDoShareTurnNumbers = []                # we'll make a parallet list, so we can process these cells first
                # for cell in listOfCellsInColumnWithTurnNumbers:
                #     if cell not in cellsThatDoNotShareTurnNumbers:
                #         cellsThatDoDoDoDoDoShareTurnNumbers.append(cell)

                
                # if column == 1:
                #     print("cellsThatDoNotShareTurnNumbers: " + str(cellsThatDoNotShareTurnNumbers))
                #     print("cellsThatDoDoDoDoDoShareTurnNumbers: " + str(cellsThatDoDoDoDoDoShareTurnNumbers))

                # # now process every cell that doesn't fit in 'cellsThatDoNotShareTurnNumbers'
                # for cell in cellsThatDoDoDoDoDoShareTurnNumbers:
                #     putCellIntoGroupNumber(cell, column, groupXCells, groupXTurnNumbers, 0)

                # # now that that is done, we start again, this time defining our "biggest" cell again from the cellsThatDoNotShareTurnNumbers













#######################################################################################################################################################
#######################################################################################################################################################
###########################     END      ############################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
                # groupXCells = [ [] for i in range(10)]          # for example, groupXCells[1] = []          is a list of the cells in group 1
                # groupXTurnNumbers = [ [] for i in range(10)]	# for example, groupXTurnNumbers[1] = []    is a list of the turnNumbers in group 1
                # # we're assuming that there will never be more than 10 groups... doesn't feel like a dangerous assumption in a six player game.....

                # def putCellIntoGroupNumber(rowNumber, columnNumber, cellsInGroup, turnNumbersInGroup, groupNumber):	 # this function should only be called on cells with turnNumber(s)
                #     if cellsInGroup[groupNumber] == []:                      # if there are no cells in this group, then... 
                #         cellsInGroup[groupNumber].append(rowNumber)          # add this cell/rowNumber to groupXCells[groupNumber]
                #         for turnNumber in analyTable[rowNumber][columnNumber]:  # ... and add these turnNumbers to groupXTurnNumbers
                #             if turnNumber not in turnNumbersInGroup[groupNumber] and isinstance(turnNumber, int):   # don't want redundant duplicates, and we don't want non-integers
                #                 turnNumbersInGroup[groupNumber].append(turnNumber)    
                #     else:  # if groupXCells is NOT empty, or in other words if this group already has cells attached to it,
                #         doesTheNewCellHaveTurnNumbersThatAreAlreadyInTheGroup = False
                #         for turnNumber in analyTable[rowNumber][columnNumber]:
                #             if turnNumber in turnNumbersInGroup[groupNumber] and isinstance(turnNumber, int):
                #                 doesTheNewCellHaveTurnNumbersThatAreAlreadyInTheGroup = True
                #         if doesTheNewCellHaveTurnNumbersThatAreAlreadyInTheGroup:
                #             cellsInGroup[groupNumber].append(rowNumber)                 # add this cell to cellsInGroup
                #             for turnNumber in analyTable[rowNumber][columnNumber]:      # and add these turnNumbers to turnNumbersInGroup
                #                 if turnNumber not in turnNumbersInGroup[groupNumber] and isinstance(turnNumber, int):       # ...without adding duplicates
                #                     turnNumbersInGroup[groupNumber].append(turnNumber)
                #         else: # if NONE of the turnNumbers in this cell are in groupXTurnNumbers, then try to add them to a different group:
                #             putCellIntoGroupNumber(rowNumber, columnNumber, cellsInGroup, turnNumbersInGroup, groupNumber + 1)		# recursion - this will end on its own eventually

                # find the sizes of all the cells, e.g., 
                numberOfElementsInCells = []  # numberOfElementsInCells[0] = 2, means that cell 0 in the column has 2 things in it... likely something like ['?', 4] or something
                for row in range(21):
                    numberOfElementsInCells.append(len(analyTable[row][column]))
                # if __column == 1:
                #     print("numberOfElementsInRows: " + str(numberOfElementsInRows))

                biggestCellSize = -1  		# then loop thru numberOfElementsInCells and identify the biggestCellSize
                for entry in numberOfElementsInCells:
                    if entry > biggestCellSize:
                        biggestCellSize = entry
                # if __column == 1:
                #     print("biggestCellSize: " + str(biggestCellSize))
                # if biggestCellSize = 1, then drop everything and stop????

                listOfCellsOfDifferentSizes = [ [] for i in range(biggestCellSize + 1)]			# for example listOfCellsOfDifferentSizes[2] = [3, 7] means that rows 3 and 7 have 2 elements each
                for x in range(biggestCellSize + 1):
                    for row in range(21):
                        if len(analyTable[row][column]) == x + 1:
                            # print("the length of the list at row " + str(row) + " and column " + str(__column) + " is " + str(len(analyTable[row][__column])))
                            listOfCellsOfDifferentSizes[x + 1].append(row)
                # listOfCellsOfDifferentSizes[1] = [], which is a list of the row numbers that have cells of size 1 
                # listOfCellsOfDifferentSizes[2] = [], which is a list of the row numbers that have cells of size 2
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
                # if column == 1:
                #     print("column: " + str(column) + "                                listOfCellsOfDifferentSizes: " + str(listOfCellsOfDifferentSizes))
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
#######################################################################################################################################################
                cellSizesToSearchFor = [biggestCellSize - x for x in range(biggestCellSize)]		# should look like [4, 3, 2, 1], or [3, 2, 1] or [2, 1]
                # this is so we can start creating "groups" beginning with the cells that have the most turnNumbers in them
                # if we didn't do it this way, then we could build up two separate groups, only to find out near the end of the process that they're in fact in the SAME group
                # because we found a cell where at least one turnNumber from each group are in the same cell together

                for cellSize in cellSizesToSearchFor:						# start with the biggest cell size & work your way down
                    for rowNumber in listOfCellsOfDifferentSizes[cellSize]: 			# for example, look at cells with 4 elements, then cells with 3 elements, etc.	
                        # only run the function IF THE CELL CONTAINS AT LEAST 1 TURN NUMBER!!!!
                        # very important!!!! because a group really shouldn't exist unless there's a turnNumber in the cell (and we're too lazy to deal with '?' in another way)
                        containsAtLeastOneTurnNumber = False
                        for x in range(turnNumber + 1):
                            if x in analyTable[rowNumber][column]:
                                containsAtLeastOneTurnNumber = True
                        if containsAtLeastOneTurnNumber:
                            putCellIntoGroupNumber(rowNumber, column, groupXCells, groupXTurnNumbers, 0)	# at first, try to fit the cell into group 0, & recursion will try all other groups

                numberOfGroups = 0
                for x in range(len(groupXCells)):
                    if len(groupXCells[x]) > 0:
                        numberOfGroups += 1

                # all of this was so we can execute the following:
                if numberOfYs == 1 and numberOfGroups > 1:      # yes, we already know that numberOfYs is 1, because we indented above... but we repeat here for the coder's benefit
                    # if there is one Y and at least 2 distinct groups of turnNumbers, then we know that all cells in that column that only have '?' can be changed to '-'
                    # so, go thru this __column and change the ? to -
                    for row in range(21):
                        if analyTable[row][column] == ['?']:
                            analyTable[row][column] = ['-']
                            print("OMG IT ACTUALLY WORKED?? in column " + str(column) + " we found one Y and two or more groups of turnNumbers, so we changed row " + str(row) + "'s '?' to '-'")
                            ############# CALL FUNCTION HERE
                            functionsToCallIfQuestionMarkRemoved()
                            functionsToCallIfNegativeAdded()
                            functionsToCallIfTurnNumberRemoved()
                            # allFunctions()
                # look at .txt file titled 'clueSolver - one Y and groups.txt' for a breakdown (or muddy history?) of how we got this to work


    def checkForAllNegativesInRow(namesOfKillerWeaponRoom, announcements):
        global numberOfFunctionCalls
        numberOfFunctionCalls += 1
        #   if a row has all "-", we know that that card is in the envelope, so announce that fact by printing it at top of analysis table printout
        for row in range(21):       # look at row 0 of the analysis table. If there is a "-" in every column then we're golden
            numberOfNegatives = 0
            for column in range(6):                
                if "-" in analyTable[row][column]:
                    numberOfNegatives += 1
            if numberOfNegatives == 6:
                if row < 6:
                    namesOfKillerWeaponRoom[0] = cardList[row].getName()
                    if announcements[0] == False:
                        print("KILLER DISCOVERED, BECAUSE SIX '-' WERE FOUND IN ROW " + str(row) + ".")
                        announcements[0] = True
                if row > 5 and row < 12:
                    namesOfKillerWeaponRoom[1] = cardList[row].getName()
                    if announcements[1] == False:
                        print("WEAPON DISCOVERED, BECAUSE SIX '-' WERE FOUND IN ROW " + str(row) + ".")
                        announcements[1] = True
                if row > 11:
                    namesOfKillerWeaponRoom[2] = cardList[row].getName()
                    if announcements[2] == False:
                        print("ROOM DISCOVERED, BECAUSE SIX '-' WERE FOUND IN ROW " + str(row) + ".")
                        announcements[2] = True


    def checkForLastRemainingQuestionMarksInCategory():             
        global numberOfFunctionCalls
        numberOfFunctionCalls += 1        
        # this function checks whether the last few (or single) ? in a section can be changed into a Y or Ys, or possibly a '-'
 		# basically, if Y + ? = 5, and the killer is known, then the ? can safely be turned into Y
        #####################################################################################
        # scan the killers & tally up
        tallyKillerSection = [0, 0]       # tallyKillerSection[0] = number of Y     ...         tallyKillerSection[1] = number of ?
        for row in range(6):
            for column in range(6):
                if "Y" in analyTable[row][column]:
                    tallyKillerSection[0] += 1
                if "?" in analyTable[row][column]:
                    tallyKillerSection[1] += 1
        if tallyKillerSection[0] < 5 and tallyKillerSection[0] + tallyKillerSection[1] == 5:
            for row in range(6):
                for column in range(6):
                    if "?" in analyTable[row][column]:
                        whatWasRemoved = []
                        whatWasRemoved = analyTable[row][column]
                        analyTable[row][column] = ["Y"]
                        print("IN THE KILLER SECTION THERE WERE " + str(tallyKillerSection[0]) + " Ys AND " + str(tallyKillerSection[1]) + " ?s, SO WE TURNED THE ? AT ROW " + str(row) + ", COLUMN " + str(column) + " INTO Y.")
                        for rrow in range(21):
                            for element in whatWasRemoved:
                                if element in analyTable[rrow][column] and element != "?" and element != "Y" and element != "-":   # include "Y" bc we don't want to undo what we just did
                                    analyTable[rrow][column].remove(element)
                        ############ CALL FUNCTION HERE
                        functionsToCallIfYAdded()
                        functionsToCallIfQuestionMarkRemoved()
                        # allFunctions()

        elif tallyKillerSection[0] == 5:    # if there are n-1 Ys in the section, then the last row, no matter what, is the card in the envelope
            for row in range(6):
                for column in range(6):
                    if "?" in analyTable[row][column]:
                        analyTable[row][column] = ["-"]
                        print("FIVE Ys WERE FOUND IN THE KILLER SECTION, MEANING THAT THE REMAINING ROW MUST REPRESENT THE CARD IN THE ENVELOPE")
                        ########### CALL FUNCTION HERE
                        functionsToCallIfNegativeAdded()
                        # allFunctions()
        
        #####################################################################################
        tallyWeaponSection = [0, 0]       
        for row in range(6, 12):
            for column in range(6):
                if "Y" in analyTable[row][column]:
                    tallyWeaponSection[0] += 1
                if "?" in analyTable[row][column]:
                    tallyWeaponSection[1] += 1
        if tallyWeaponSection[0] < 5 and tallyWeaponSection[0] + tallyWeaponSection[1] == 5:
            for row in range(6, 12):
                for column in range(6):
                    if "?" in analyTable[row][column]:
                        whatWasRemoved = []
                        whatWasRemoved = analyTable[row][column]
                        analyTable[row][column] = ["Y"]
                        print("IN THE WEAPON SECTION THERE WERE " + str(tallyWeaponSection[0]) + " Ys AND " + str(tallyWeaponSection[1]) + " ?s, SO WE TURNED THE ? AT ROW " + str(row) + ", COLUMN " + str(column) + " INTO Y.")
                        for rrow in range(21):
                            for element in whatWasRemoved:
                                if element in analyTable[rrow][column] and element != "?" and element != "Y" and element != "-":
                                    analyTable[rrow][column].remove(element)
                        ######## CALL FUNCTION HERE
                        functionsToCallIfYAdded()
                        functionsToCallIfQuestionMarkRemoved()
                        # allFunctions()
        elif tallyWeaponSection[0] == 5:    # if there are n-1 Ys in the section, then the last row, no matter what, is the card in the envelope
            for row in range(6, 12):
                for column in range(6):
                    if "?" in analyTable[row][column]:
                        analyTable[row][column] = ["-"]
                        print("FIVE Ys WERE FOUND IN THE WEAPON SECTION, MEANING THAT THE REMAINING ROW MUST REPRESENT THE CARD IN THE ENVELOPE")
                        ######## CALL FUNCTION HERE
                        functionsToCallIfNegativeAdded()
                        # allFunctions()
        #####################################################################################
        tallyRoomSection = [0, 0]       
        for row in range(12, 21):
            for column in range(6):
                if "Y" in analyTable[row][column]:
                    tallyRoomSection[0] += 1
                if "?" in analyTable[row][column]:
                    tallyRoomSection[1] += 1
        if tallyRoomSection[0] < 5 and tallyRoomSection[0] + tallyRoomSection[1] == 5:
            for row in range(12, 21):
                for column in range(6):
                    if "?" in analyTable[row][column]:
                        whatWasRemoved = []
                        whatWasRemoved = analyTable[row][column]
                        analyTable[row][column] = ["Y"]
                        print("IN THE ROOM SECTION THERE WERE " + str(tallyRoomSection[0]) + " Ys AND " + str(tallyRoomSection[1]) + " ?s, SO WE TURNED THE ? AT ROW " + str(row) + ", COLUMN " + str(column) + " INTO Y.")
                        for rrow in range(21):
                            for element in whatWasRemoved:
                                if element in analyTable[rrow][column] and element != "?" and element != "Y" and element != "-":
                                    analyTable[rrow][column].remove(element)
                        ########### CALL FUNCTION HERE
                        functionsToCallIfYAdded()
                        functionsToCallIfQuestionMarkRemoved()
                        # allFunctions()
        elif tallyRoomSection[0] == 8:    # if there are n-1 Ys in the section, then the last row, no matter what, is the card in the envelope
            for row in range(12, 21):
                for column in range(6):
                    if "?" in analyTable[row][column]:
                        analyTable[row][column] = ["-"]
                        print("EIGHT Ys WERE FOUND IN THE ROOM SECTION, MEANING THAT THE REMAINING ROW MUST REPRESENT THE CARD IN THE ENVELOPE")    
                        ######### CALL FUNCTION HERE
                        functionsToCallIfNegativeAdded()
                        # allFunctions()

    def checkForSingleTurnNumbersInColumn():    #   if a turnNumber appears only once in a column, we know that that player has that card
        global numberOfFunctionCalls
        numberOfFunctionCalls += 1        
        for column in range(6):   #   loop thru each column, one at a time:
            # initialize a tally list for that column, to keep track of how many times we see each turn number appear
            #   the tally list answers the question, "How many times does turn 1 appear in the entire analysis table column? 0, 1, 2 or 3 times?"
            tally = {}
            for turn in range(turnNumber):
                tally[turn + 1] = 0         # initialize the tallies at zero
            # if we look at a cell, and see for example [?, 4, 5], then we do: tally[4] += 1, and tally[5] += 1
            for row in range(21):
                for turnMinusOne in range(turnNumber):
                    if turnMinusOne+1 in analyTable[row][column]:
                        tally[turnMinusOne+1] += 1
            # now we've got our tally list... and we check to see if any turn# appears ONLY ONCE in the tally dictionary
            for turn in range(turnNumber):
                if tally[turn + 1] == 1:
                    print("WE IDENTIFIED A LONE TURN " + str(turn + 1) + " IN COLUMN " + str(column))
                    # because we know that the turn number exists only once, we know that the player has that card... so we need to change that turn number into a "Y"
                    # but we don't know the exact location within the analysisTable ... all we know is that for example there is "one 6 in Orchid's column"
                    #   so because we know the column, we can cycle thru the rows and replace (turn + 1) with "Y"
                    for row in range(21):
                        if (turn + 1) in analyTable[row][column]:
                            # WE NEED TO ACT IMMEDIATELY to prevent a logic error!!!!!!! Keep track of whatWasThere and remove those turn numbers from the rest of the column
                            # for example if a cell has [17, 18, 19] and the 19 is the only 19 in the column, then when we change the cell to ["Y"] it will look like the 
                            # 17 and 18 that are in other cells in that column are indicative of a card being held... and that should not happen
                            whatWasThere = []
                            whatWasThere = analyTable[row][column]
                            analyTable[row][column] = ["Y"]
                            print("...AND REPLACED IT WITH A 'Y' AT ROW " + str(row))
                            # IMMEDIATELY we need to go up & down that column and remove the turn numbers that USED TO BE in the cell where we're putting the "Y"
                            if "Y" not in whatWasThere and "-" not in whatWasThere:
                                for row in range(21):
                                    for element in whatWasThere:
                                        if element in analyTable[row][column] and element != "?":
                                            analyTable[row][column].remove(element)
                            ######### CALL FUNCTION(S) HERE
                            functionsToCallIfYAdded()
                            functionsToCallIfTurnNumberRemoved()
                            # allFunctions()



    def processDecline():       # mark a "-" for each player who declines, for those three cards
        global numberOfFunctionCalls
        numberOfFunctionCalls += 1        
        #   identify all players who declined ... i.e., scarlettResponse == 'd', mustardResponse == 'd', etc, and mark all three card in that guess as "-" for that respondent

        listOfIterations = []
        if initialAnalysisCompletedOfLoadedSavedGame[0] == False:           # when loading a saved game we want to process each turn in the turnData dictionary
            listOfIterations = [x for x in range(turnNumber)]
            initialAnalysisCompletedOfLoadedSavedGame[0] = True
        elif initialAnalysisCompletedOfLoadedSavedGame[0] == True:
            listOfIterations = [turnNumber-1]

        for turnMinusOne in listOfIterations:

            killerRowNum = turnData[turnMinusOne+1]['killerGuessed']
            weaponRowNum = turnData[turnMinusOne+1]['weaponGuessed']
            roomRowNum = turnData[turnMinusOne+1]['roomGuessed']

            for player in playerList:
                nameString = player.getNameOnly().lower() + "Response"
                if turnData[turnMinusOne+1][nameString] == 'd':
                    analyTable[killerRowNum][player.getColumnNumber()] = ["-"]
                    analyTable[weaponRowNum][player.getColumnNumber()] = ["-"]
                    analyTable[roomRowNum][player.getColumnNumber()] = ["-"]  
                ####### CALL FUNCTION(S) HERE
                functionsToCallIfNegativeAdded()
                # allFunctions()


         
    #       respond by showing a card (r)
    #           if we don't know what card was shown, then we replace the "?" with the turn number, indicating that on that turn one of those 3 cards is held by the player
    #           if the card is known, then the ONLY THING we put into the analyTable is the "Y" for the owner of the card, and we remove everything else
    #           every time a new Y appears in the table, we need to run horizontal & vertical processing
    def processRespond():
        global numberOfFunctionCalls
        numberOfFunctionCalls += 1

        listOfIterations = []         
        if initialAnalysisCompletedOfLoadedSavedGame[1] == False:           # when loading a saved game we want to process each turn in the turnData dictionary
            listOfIterations = [x for x in range(turnNumber)]
            initialAnalysisCompletedOfLoadedSavedGame[1] = True
        elif initialAnalysisCompletedOfLoadedSavedGame[1] == True:
            listOfIterations = [turnNumber-1]

        for turnMinusOne in listOfIterations:
            killerRowNum = turnData[turnMinusOne+1]['killerGuessed']
            weaponRowNum = turnData[turnMinusOne+1]['weaponGuessed']
            roomRowNum = turnData[turnMinusOne+1]['roomGuessed']

            isTheShownCardKnown = False
            if turnData[turnMinusOne+1]['card'] != -1:
                isTheShownCardKnown = True

            #   going to append the turnNumber into the cell's list
            for player in playerList:
                nameString = player.getNameOnly().lower() + "Response"
                if turnData[turnMinusOne+1][nameString] == 'r':
                    if isTheShownCardKnown:     #   if the card is known then don't enter turnNumbers... only enter "Y"
                        cardNumber = turnData[turnMinusOne+1]['card']
                        whatWasRemoved = []
                        whatWasRemoved = analyTable[cardNumber][player.getColumnNumber()]
                        analyTable[cardNumber][player.getColumnNumber()] = ["Y"]
                        for row in range(21):
                            for element in whatWasRemoved:
                                if element in analyTable[row][player.getColumnNumber()] and element in [x+1 for x in range(turnNumber)]: # i.e. we don't want to remove "Y" or "?"
                                    analyTable[row][player.getColumnNumber()].remove(element)
                        ######### CALL FUNCTION(S) HERE
                        functionsToCallIfYAdded()
                        functionsToCallIfQuestionMarkRemoved()
                        functionsToCallIfTurnNumberRemoved()
                        functionsToCallIfNegativeRemoved()
                        # allFunctions()


                    #   if there is a "Y" in any of the three cards that were just guessed, then don't bother recording the turnNumbers bc for all we know they showed that "Y" card
                    elif "Y" in analyTable[killerRowNum][player.getColumnNumber()] or "Y" in analyTable[weaponRowNum][player.getColumnNumber()] or "Y" in analyTable[roomRowNum][player.getColumnNumber()]:
                        continue
                    else:    #  if there's no '-' already, and we don't already know that player's 3 cards, then add the turn number
                        if "-" not in analyTable[killerRowNum][player.getColumnNumber()] and howManyYsInColumn(player.getColumnNumber()) < 3:
                            if (turnMinusOne + 1) not in analyTable[killerRowNum][player.getColumnNumber()]:  # don't add more than one instance of that turnNumber
                                analyTable[killerRowNum][player.getColumnNumber()].append(turnMinusOne + 1)
                        if "-" not in analyTable[weaponRowNum][player.getColumnNumber()] and howManyYsInColumn(player.getColumnNumber()) < 3:
                            if (turnMinusOne + 1) not in analyTable[weaponRowNum][player.getColumnNumber()]:
                                analyTable[weaponRowNum][player.getColumnNumber()].append(turnMinusOne + 1)
                        if "-" not in analyTable[roomRowNum][player.getColumnNumber()] and howManyYsInColumn(player.getColumnNumber()) < 3:
                            if (turnMinusOne + 1) not in analyTable[roomRowNum][player.getColumnNumber()]:
                                analyTable[roomRowNum][player.getColumnNumber()].append(turnMinusOne + 1)
                        ##### CALL FUNCTION(S) HERE
                        functionsToCallIfTurnNumberAdded()
                        # allFunctions()

    # Dealing with changes to -
    def functionsToCallIfNegativeAdded():
        checkForAllNegativesInRow(killerWeaponRoom, announces)
    def functionsToCallIfNegativeRemoved():
        pass   
    
    # Dealing with changes to Y
    def functionsToCallIfYAdded():
        processYsHorizontal()
        processYsVertical()
        checkForLastRemainingQuestionMarksInCategory()
    def functionsToCallIfYRemoved():
        pass
  
    # Dealing with changes to turnNumbers
    def functionsToCallIfTurnNumberAdded():
        processYsVertical()
        checkForSingleTurnNumbersInColumn()
    def functionsToCallIfTurnNumberRemoved():
        checkForSingleTurnNumbersInColumn()
  
    # Dealing with changes to ?
    def functionsToCallIfQuestionMarkAdded():
        checkForLastRemainingQuestionMarksInCategory()
    def functionsToCallIfQuestionMarkRemoved():
        processYsVertical()
        checkForLastRemainingQuestionMarksInCategory()




    for repetitionNumber in range(1):      # this is a lazy way to make sure we process everything.... hopefully change this later
        processYsHorizontal()       # these two (horiz/vert) are run first thing in order to incorporate the user's 3 known cards
        processYsVertical()         # these two (horiz/vert) are run first thing in order to incorporate the user's 3 known cards
        processDecline()
        processRespond()            # there will always be 1 response, and possibly some declines, so always run these

    #add "cleanup" functionality here, in case the previous processes have revealed some important info ... because we want to show this info to the user before the next turn starts



def printAnalysisTable(table, actualKillerWeaponRoom):
    print("ANALYSIS TABLE:")
    print("# of function calls: " + str(numberOfFunctionCalls))
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
            # elif table[row][column] == ['?']:
            #     print('?'.center(15, ' '), end=" ")
            else:
                print(str(table[row][column]).center(15, ' '), end=" ")
        print(" |")
    print("----------------------------------------------------------------------------------------------------------------------")    
    print(" ")


def showSavedGames():       # EXPERIMENTING WITH os.scandir()
    path = os.getcwd()
    # Scan the directory and get an iterator of os.DirEntry objects corresponding to entries in it using os.scandir() method
    obj = os.scandir(path)
    listOfSaveFiles = []

    # List all files and directories in the specified path
    # print("Files and Directories in '% s':" % path)
    print("")
    for entry in obj :
        # if entry.is_dir() or entry.is_file():     # don't want directories to be printed
        if entry.is_file() and ".txt" in entry.name and "ClueSolverGameSave" in entry.name:           
            listOfSaveFiles.append(str(entry.name))
    obj.close()   # To close the iterator and free acquired resources use scandir.close() method

    print("this is a list of saved game files:")
    x = 1
    for entry in listOfSaveFiles:
        print(str(x) + ". " + str(entry))
        x += 1

    userChoice = askUserInputInt([y+1 for y in range(x)], "which game do you want to load? :  ")
    gameToLoad = str(listOfSaveFiles[userChoice - 1])    
    return gameToLoad



def startGame():
    # initialize a bunch of stuff
    userCharacter = Player
    turnNumber = -1
    # analysisTable = [["?"]*6]*21        # can't initialize with this technique because it creates a "shallow list", see https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
    analysisTable = [[ ["?"] for i in range(6)] for j in range(21)]
    actualKillerWeaponRoom = ["?", "?", "?"]
    announcementsHaveBeenMadeForKillerWeaponRoom = [False, False, False]   # this regulates when, in the terminal, the discovery of the killer/weapon/room is announced
    fileName = ""

    userInput = askUserInputChar(["y", "n"], "Do you want to load a previous game? (y/n):  ")
    if userInput == "y":
        fileName = showSavedGames()

        # fileToLoad is the file to which we save future progress
        print("LOADING FILE: " + str(fileName))

        with open(str(fileName)) as fileObject:
            fileContents = fileObject.readlines()
        playerName = str(fileContents[0]).strip()        # .strip() will remove the /n newline character     # line 0 is the player name
        for player in playerList:
            if playerName == player.getNameOnly():
                userCharacter = player
        playerCard1 = int(fileContents[1].strip())       #   line 1 2 3 are the player's 3 cards
        playerCard2 = int(fileContents[2].strip())
        playerCard3 = int(fileContents[3].strip())

        # identify the card objects, and then .add them to the player character... they will then be processed in the first part of the analyzeData() function
        for card in cardList:
            cardNum = card.getPlaceInCardList()
            if playerCard1 == cardNum:
                userCharacter.addCard1(card)
            if playerCard2 == cardNum:
                userCharacter.addCard2(card)
            if playerCard3 == cardNum:
                userCharacter.addCard3(card)

        # next we set the player order 
        playerOrderList = fileContents[4].strip()       # line 4 is the player order... need to ensure that this is saved as an actual list, because right now it's a string
        newPlayerOrderList = playerOrderList.replace('[', '')       # get rid of the extra characters before we convert it into a list with " " as delimiter
        newPlayerOrderList = newPlayerOrderList.replace(']', '')    # get rid of the extra characters before we convert it into a list with " " as delimiter
        newPlayerOrderList = newPlayerOrderList.replace('\'', '')   # get rid of the extra characters before we convert it into a list with " " as delimiter
        newPlayerOrderList = newPlayerOrderList.replace(',', '')    # get rid of the extra characters before we convert it into a list with " " as delimiter
        playerOrderList = list(newPlayerOrderList.split(" "))       # finally, convert the stripped string into a list
        x = 1
        for element in playerOrderList:
            for player in playerList:
                if player.getNameOnly() == element:
                    player.setTurnOrder(x)
                    player.turnOrderConfirmedSetTrue()
                    x += 1

        turnLog = ast.literal_eval(fileContents[5].strip())     # line 5 is the turnDataDictionary
        # turnLog = fileContents[5].strip()     # this line doesn't work on a dictionary object

        turnNumber = int(fileContents[6].strip())       # line 6 is the last completed turn number
        printTurnsPretty(turnNumber, turnLog)
        print("")
        analyzeData(turnNumber, turnLog, analysisTable, userCharacter, actualKillerWeaponRoom, announcementsHaveBeenMadeForKillerWeaponRoom)
        printAnalysisTable(analysisTable, actualKillerWeaponRoom)
        turnNumber += 1     # because (turnNumber) was completed successfully, the next turn we start with is turnNumber+1

    else:
        # create a timestamp, for the purpose of making a unique filename
        x = datetime.datetime.now()
        timeStamp = str(x.year) + "-" + str(x.month) + "-" + str(x.day) + " " + str(x.hour) + "h-" + str(x.minute) + "m-" + str(x.second) + "s"
        fileName = "ClueSolverGameSave " + str(timeStamp) + ".txt"

        userCharacter = askUserWhichCharacter(fileName)
        verifyOrder(playerList, fileName)
        # initialize a blank nested dictionary to record the events of each turn
        turnLog = {}
        turnNumber = 1

    gameFinished = False
    while (gameFinished == False): 
        global numberOfFunctionCalls
        numberOfFunctionCalls = 0
        executeTurn(turnNumber, turnLog, fileName)      
        analyzeData(turnNumber, turnLog, analysisTable, userCharacter, actualKillerWeaponRoom, announcementsHaveBeenMadeForKillerWeaponRoom)
        printAnalysisTable(analysisTable, actualKillerWeaponRoom)
        # print(turnLog)
        turnNumber += 1
        if turnNumber == 55:
            gameFinished = True

startGame()


