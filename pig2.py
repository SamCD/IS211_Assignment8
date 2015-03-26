import random
import sys
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("player1")
parser.add_argument("player2")
parser.add_argument("--timed",action="store_true")
args = parser.parse_args()

random.seed(0)
class Player(object):


    def __init__(self,name):

        self.name = name
        self.score = 0
        self.Turn = False
        self.rolls = []
        self.status = 0
        self.choice = ''
        self.type = 'Human'


    def Roll(self):

        die = Die()
        return die.roll()


    def Hold(self):
        self.score += sum(self.rolls)
        

class Die(object):

    
    def __init__(self):
        self.showing = 0


    def roll(self):

        self.showing = random.randint(1,6)
        return self.showing


class Game(object):


    def __init__(self,player1='Player1',player2='Player2'):

        players = PlayerFactory()
        self.Player1 = players.create_player(args.player1)
        self.Player2 = players.create_player(args.player2)
        if self.Player1.name == self.Player2.name:
            self.Player2.name += '2'
        self.die = Die()
        self.winner = ''
        self.turn(self.Player1)

        


    def switch(self,player):

        if player.score >= 100:
            self.winner = player.name
            self.game_over('{} is the winner'.format(self.winner))

        if player == self.Player1:
            self.Player1.Turn = False
            self.turn(self.Player2)

        if player == self.Player2:
            self.Player2.Turn = False
            self.turn(self.Player1)


    def turn(self,player):
        player.Turn = True
        while player.Turn == True and player.score < 100:
            if player.type == 'Computer':
                player.strategy()
            else:
                player.choice = raw_input('{}, Hold or Roll? (h/r): '.format(
                                                                player.name))
                if player.choice[0].lower() == 'r':
                    player.status = player.Roll()
                    if player.status == 1:
                        player.rolls = []
                        break
                    else:
                        player.rolls.append(player.status)
                    print 'Roll: {}, Turn total: {}, ' \
                        'Game total: {}'.format(
                                player.status,sum(player.rolls),
                                player.score + sum(player.rolls))
    
                if player.choice[0].lower() == 'h':
                    player.Hold()
                    player.rolls = []
                    print '{} current score: {}'.format(player.name,player.score)
                    player.Turn = False
                    
        self.switch(player)

                
    def game_over(self,msg):

        print msg
        sys.exit()

class ComputerPlayer(Player):

    def __init__(self):
        Player.__init__(self,'Watson')
        self.type = 'Computer'
    
    def strategy(self):
        
        while self.Turn == True:
            decide = 25 if (25 < (100 - self.score)) else (100 - self.score)
            if sum(self.rolls) < decide:
                self.status = self.Roll()
                if self.status == 1:
                    self.rolls = []
                    break
                else:
                    self.rolls.append(self.status)
            else:
                self.Hold()
                self.rolls = []
                print '{} current score: {}'.format(self.name,self.score)
                self.Turn = False
            
class PlayerFactory(object):


    def create_player(self,ai_hum,name='Human'):
        if ai_hum[0].lower() == 'h':
            return Player(name)
        if ai_hum[0].lower() == 'c':
            return ComputerPlayer()
    
class TimedGameProxy(Game):

    def __init__(self):
        self.start_time = time.time()
        Game.__init__(self,player1='Player1',player2='Player2')


    def time_check(self):
        if time.time() - self.start_time >= 60:
            self.game_over('Time... {}: {}, {}: {}'.format(
            self.Player1.name
            ,self.Player1.score
            ,self.Player2.name
            ,self.Player2.score))
            
    def turn(self,player):
        player.Turn = True
        if player.type == 'Computer':
            player.strategy()
        else:
            while player.Turn == True and player.score < 100:
                self.time_check()
                player.choice = raw_input('{}, Hold or Roll? (h/r): '.format(
                    player.name))
                if player.choice[0].lower() == 'r':
                    player.status = player.Roll()
                    if player.status == 1:
                        player.rolls = []
                        break
                    else:
                        player.rolls.append(player.status)
                    print 'Roll: {}, Turn total: {}, ' \
                        'Game total: {}'.format(
                                player.status,sum(player.rolls),
                                player.score + sum(player.rolls))
        
                if player.choice[0].lower() == 'h':
                    player.Hold()
                    player.rolls = []
                    print '{} current score: {}'.format(player.name,player.score)
                    player.Turn = False
                
        self.switch(player)

def main():
    if args.timed:
        game = TimedGameProxy()
    else:
        game = Game()

if __name__ == '__main__':
  main()
