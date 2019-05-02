# Shawn Davidson
# Chris White
# CSCI 404 - Fall 2018
# Assignment 4
# train.py - parses the training files and stores the
# data in dictionaries for spam words, non-spam words,
# and all words in the training set

import os
from dict import Dictionary

# Find the given word, return the # of occurrences,
# return 0 if not found
def find(dict, spword):
    for (word, count) in dict.dict:
        if word == spword:
            return count
    return 0


# Calculate the probabilities of each word in trainDict occurring
# in the dictionary
def genProb(trainDict, dict):

    probs = []
    for (word, count) in trainDict.dict:
        total = find(dict, word)
        # If word does not occur in the dictionary, ignore it
        if(total != 0):
            prob = float(count)/ float(total)
            probs.append((word, prob))

    return probs

# Parse the training files, store the data in dictionaries for
# spam words, non-spam words, and all words in the training set
def main():
    allSpamTrain = []
    for file in os.listdir("data/spam-train/"):
        if file.endswith(".txt"):
            allSpamTrain.append(open("data/spam-train/" + file, "r").read())
    spamDict = Dictionary(allSpamTrain)


    allNotSpamTrain = []
    for file in os.listdir("data/nonspam-train/"):
        if file.endswith(".txt"):
            allNotSpamTrain.append(open("data/nonspam-train/" + file, "r").read())
    notSpamDict = Dictionary(allNotSpamTrain)

    allTrain = allSpamTrain + allNotSpamTrain
    dict = Dictionary(allTrain)

    spamProbs = genProb(spamDict, dict)
    nonSpamProbs = genProb(notSpamDict, dict)

    return spamProbs, nonSpamProbs, dict


main()
