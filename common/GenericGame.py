#!/usr/bin/env python
# encoding: utf-8
'''
common.GenericGame -- defines base constants and classes

common.GenericGame is the foundation for various card games

It defines classes_and_methods

@author:     Kevin Pintar

@copyright:  2018 Mozart Spring. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
import random

from optparse import OptionParser

__all__ = []
__version__ = 0.1
__date__ = '2018-09-18'
__updated__ = '2018-09-18'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

HEART = "HEART"
DIAMOND = "DIAMOND"
SPADE = "SPADE"
CLUB = "CLUB"

SUITS = [HEART, DIAMOND, SPADE, CLUB]
ORDINAL = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']


class Card(object):
    def __init__(self,suit,ordinal):
        self.suit = suit
        self.ordinal = ordinal
    def __str__(self):
        return str(self.ordinal)+" "+self.suit
    def getValue(self):
        return ORDINAL.index(self.ordinal)+2
        
class Deck(object):
    cards = []

    def __init__(self):
        self.cards = []
        
    def __str__(self):
        retvalue = ''
        for card in self.cards:
            retvalue += card.__str__() + " "
        return retvalue
            
    def addCard(self,card): 
        self.cards.append(card)
        
    def dealCard(self):
        return self.cards.pop(0)
    
    def shuffleDeck(self):
        random.shuffle(self.cards)


class Player(object):
    name = ''
    position = 0
    hand = [] 
    score = 0
    
    def __init__(self,name,position):
        self.name = name
        self.position = position
        self.hand = Deck()
        self.score = 0
    
    def __str__(self):
        return self.name + " " + str(self.position)
    
    def addCard(self,_card):
        self.hand.addCard(_card)
        
    def playCard(self, _game):
        return self.hand.dealCard()
        
    def showHand(self):
        print self.hand 
        
class Game(object):
    deck = Deck()
    discardPile = []
    tableCards = []
    
    players = []
    maxPlayers = 4
    isGameOver = False
    dealerPosition = 0
    round          = 0
    
    def __init__(self):
        # initialize deck
        self.deck = Deck()
        self.discardPile = Deck()
        self.tableCards = Deck()
        self.round = 0
        self.isGameOver = False

    def addPlayer(self, name):
        numPlayers = len(self.players)
        numPlayers += 1
        if DEBUG:
            print "Adding Player ",name," at position ",numPlayers
        self.players.append(Player(name,numPlayers))
        
    def sortPlayersByScore(self):
        decoratedPlayers = [ (_p.score, _p) for _p in self.players ]
        decoratedPlayers.sort()
        undecoratedPlayers  = []
        undecoratedPlayers[:] = [ _p[1] for _p in decoratedPlayers]
        return undecoratedPlayers 
    
    def startGame(self): pass
                 
    def playRound(self): pass

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2018 Kevin Pintar (Mozart Spring)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-i", "--in", dest="infile", help="set input path [default: %default]", metavar="FILE")
        parser.add_option("-o", "--out", dest="outfile", help="set output path [default: %default]", metavar="FILE")
        parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")

        # set defaults
        parser.set_defaults(outfile="./out.txt", infile="./in.txt")

        # process options
        (opts, args) = parser.parse_args(argv)

        if opts.verbose > 0:
            print("verbosity level = %d" % opts.verbose)
        if opts.infile:
            print("infile = %s" % opts.infile)
        if opts.outfile:
            print("outfile = %s" % opts.outfile)

        # MAIN BODY #

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
        profile_filename = 'common.GenericGame_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())