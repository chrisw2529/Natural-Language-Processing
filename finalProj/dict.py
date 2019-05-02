# Shawn Davidson
# Chris White
# CSCI 404 - Fall 2018
# Assignment 4
# dict.py -  stores all the tokens with the count
# of each in a list.

import nltk

size = 10000

class Dictionary:
    # Pass the text in as input
    def __init__(self, input):
        self.tokens = 0
        self.createDict(input)

    # Tokenize the input and generate the count of each token
    def createDict(self, input):
        tokens = nltk.word_tokenize(str(input))
        counts = nltk.FreqDist(tokens)
        self.dict = counts.most_common(size)
        for (word, count) in self.dict:
            self.tokens += count

