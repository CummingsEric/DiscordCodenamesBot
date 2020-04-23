# needs a function to generate a deck of cards this includes a dictionary with a cardID as a key and a card object as its
#
#
#
from enum import Enum
import random


# init class types
class Type(Enum):
    RED = 1
    BLUE = 2
    NEUTRAL = 3
    ASSASSIN = 4


class Card:
    def __init__(self, word, x, y, type):
        self.selected = False
        self.word = word
        self.x = x
        self.y = y
        if type < 9:
            self.type = Type(1)
        elif (type < 17):
            self.type = Type(2)
        elif (type == 24):
            self.type = Type(4)
        else:
            self.type = Type(3)


# this needs to init the deck based on the
class Cards:
    def __init__(self, wordset):
        self.cards = {}
        self.wordstoID = {}
        types = random.sample(range(25), 25)
        # get 25 random words

        file = open(("WordSets/" + str(wordset)), "r")
        words = [(line.strip().lower()) for line in file]
        file.close()
        random.shuffle(words)
        self.words = words[:25]

        for CardID in range(25):
            self.cards[CardID] = Card(words[CardID], CardID % 5, 5 - int(CardID / 5), types[CardID])
            self.wordstoID[words[CardID]] = CardID

    def solution(self):
        return [(x.word, x.type.name) for x in self.cards.values()]
