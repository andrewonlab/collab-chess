__author__ = 'My'

import time
import math


#Teams are split up between White team and Black team
#White team goes first

#To start Timer:
#   1) create instance of TimerClass (in = TimerClass())
#   2) immediately call startTimer for that instance (in.TimerClass(in))

#A single turn for a team is 20 seconds (15 seconds to move, 5 second "break")
#At the end of the first 15 seconds in a turn, collectVotes is called
#To differentiate the teams, the boolean whiteTurn is used (True if it is whites turn, False if it is blacks turn)
#collectVotes is where code to initiate vote collection goes

#When a person first joins the game, to get the time of the current turn, they call getTime()
#The two arguments will be the instance of the class and a boolean depending on their team (white = true, black = false)
#This function returns an integer of how many seconds are left in their team's current turn (0 if it isn't their teams turn)
#this integer is then used to update their personal timer

#From then on their turn times will be updated through notifyTurnStart()
#notifyTurnStart() should prompt members of the appropriate team (based on whiteTurn boolean) to update their personal timers to 15

#Runs indefinitely



class TimerClass:

    timer = time.time()
    whiteTurn = True

    def startTimer(self):
        while True:
            TimerClass.notifyTurnStart(self, TimerClass.whiteTurn)
            time.sleep(15)
            TimerClass.collectVotes(self, TimerClass.whiteTurn)
            if TimerClass.whiteTurn == False:
                TimerClass.whiteTurn = True
            else:
                TimerClass.whiteTurn = False
            time.sleep(5)

    def collectVotes(self, wT):
        #code to prompt the collecting of votes
        if wT == True:
            #collect white teams votes
            return
        else:
            #collect black teams votes
            return

    def notifyTurnStart(self, wT):
        if wT == True:
            #notify white team that their turn is starting so they can update their countdown timer to 15
            return
        else:
            #notify black team that their turn is starting so they can update their countdown timer to 15
            return

    def getTime(self, wTeam):
        timeNow = time.time()
        totalTime = math.floor(timeNow - TimerClass.timer)
        turnTime = totalTime%40
        #whites turn
        if turnTime < 20:
            if wTeam == False:
                return 0
            else:
                if turnTime < 15:
                    return -turnTime+15
                return 0
        #blacks turn
        else:
            if wTeam == True:
                return 0
            else:
                if turnTime-20 < 15:
                    return -turnTime+15
                return 0


def main():
    h = TimerClass
    h.startTimer(h)
    return 0

if __name__ == "__main__":
    main()
