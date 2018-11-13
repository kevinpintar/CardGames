#!/usr/bin/env python
# encoding: utf-8
'''
war.War -- shortdesc

war.War is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2018 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import common.GenericGame

from optparse import OptionParser

__all__ = []
__version__ = 0.1
__date__ = '2018-09-18'
__updated__ = '2018-09-18'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class WarCard(common.GenericGame.Card):
    def __init__(self,_suit,_ordinal):
        super(WarCard,self).__init__(_suit, _ordinal)
        
    def getValue(self):
        return common.GenericGame.ORDINAL.index(self.ordinal)+2

class WarDeck(common.GenericGame.Deck):
    def __init__(self):
        super(WarCard,self).__init__()

class WarPlayer(common.GenericGame.Player):
    def __init__(self, _name, _position ):
        super(WarPlayer,self).__init__(_name, _position)

class WarGame(common.GenericGame.Game):
    def __init__(self):
        super(WarGame,self).__init__()
        self.maxPlayers = 4
        
        # initialize War deck
        for _suit in common.GenericGame.SUITS:
            for _ordinal in common.GenericGame.ORDINAL:
                self.deck.addCard(WarCard(_suit,_ordinal))

    def startGame(self):
        _numPlayers  = len(self.players)
        # check for players > 2
        if _numPlayers < 2:
            print "Not enough players! You have only ",len(self.players),".  There must be at least 2 and less than 4."
            sys.exit(2)
        
        if _numPlayers > self.maxPlayers:
            print "Too many players!"
                        
        # shuffle deck
        self.deck.shuffleDeck()
        
        #  Deal an equal number of cards to each player
        _numCardsPerPerson = (len(self.deck.cards) // _numPlayers)
        if DEBUG: print "number of cards per player = ", _numCardsPerPerson
        
        for i in range(_numCardsPerPerson):
            for _j in range(_numPlayers):
                
                _theCard = self.deck.dealCard()
                if DEBUG: print self.players[_j].name," is being given ", _theCard
                
                self.players[_j].addCard(_theCard)
        
        if DEBUG:
            for _player in self.players:
                _player.showHand()
            
        print "There are ", len(self.deck.cards)," cards left in the deck"
        print "1.2.3.... war!"           
                 
    def playRound(self):
        # check to see if player has any cards.
        if len(self.players[0].hand.cards) <= 0:
            if DEBUG: print "we are done"
            self.isGameOver = True
            return
        
        # increment dealer position 
        self.dealerPosition +=1
        if self.dealerPosition > self.maxPlayers: self.dealerPosition = 1
        
        # clear the field
        while len(self.tableCards.cards) > 0:
            _transientCard = self.tableCards.dealCard()
            if DEBUG: print "moving table card ",_transientCard," to discard pile"
            self.discardPile.addCard(_transientCard)
            
        _noWinner = True
        _lastCardTie = False
        _atWar = False
    
        while _noWinner:
            print
                
            # does not take into consideration dealer position
            _maxCard = 0
            if not _atWar:
                _maxCardHolder = []
                _players = self.players
            else:
                _players = _maxCardHolder
                
            for _player in _players:
                try:
                    _cardPlayed = _player.playCard(self)
                except:
                    if DEBUG: print "At least two people are at war and we have run out of cards"
                    _lastCardTie = True
                    break
                
                _cardValue  = _cardPlayed.getValue()
                self.tableCards.addCard(_cardPlayed)
            
                print _player.name," played ",_cardPlayed," with card value ",_cardValue
                if _cardValue > _maxCard:
                    _maxCard = _cardValue
                    _maxCardHolder = []
                    _maxCardHolder.append(_player)
                    _atWar = False
                    if DEBUG: print "player ",_player.name," played the highest card value of ",_maxCard
                elif _cardValue == _maxCard:
                    _maxCardHolder.append(_player)
                    _atWar = True
                    if DEBUG: print "player ",_player.name," played a card equal to the max value of ",_maxCard
                    print "War!"
        
            if (len(_maxCardHolder) == 1) or (_lastCardTie): _noWinner = False
            
        if _lastCardTie:
            _NameList = [ _p.name for _p in self.players ]
            print "the hand winners were ", _NameList, " with a value of ",_maxCard
        else:
            print "the hand winner was ",_maxCardHolder[0].name," with value of ",_maxCard
            
        for _card in self.tableCards.cards:
            for _p in _maxCardHolder:
                _p.score += _card.getValue()           

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2018 user_name (organization_name)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    game = WarGame()
    
    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-p", "--player" , dest="players", action="append", help="specify a players name.")
        parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")
    
        # set defaults
        parser.set_defaults(outfile="./out.txt", infile="./in.txt")
    
        # process options
        (opts, args) = parser.parse_args(argv)
    
        if opts.verbose > 0:
            print("verbosity level = %d" % opts.verbose)
        if len(opts.players) > 1:
            for _player in opts.players:
                print "adding player ",_player
                game.addPlayer(_player)

        # MAIN BODY #
        game.startGame()
        
        while not game.isGameOver:
            game.playRound()
            
        # Print the scores
        _PlayersSortedByScore = game.sortPlayersByScore()
        for _p in _PlayersSortedByScore:
            print _p.name," has score ",_p.score
        
        print "the winner is ",_PlayersSortedByScore[len(_PlayersSortedByScore)-1].name,"!"
    
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'war.War_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())