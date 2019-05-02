# Shawn Davidson, Chris White
# CSCI 404 - Fall 2018
# Assignment 5

import sys
import nltk
import math
from math import log

# Table to keep track of transition probabilities
transitions = []

# Table to keep track of emission probabilities
emissions = []

# Initial probabilities
initials = []

# The tag dictionary
tag_dict = {}

# Create a dictionary for the number of singletons associated with each tag
def createTagSing(tags, tagPairHaps):
    tagSing = {}
    for tag in tags:
        tagSing[tag] = 0

    for pair in tagPairHaps:
        tagSing[pair[0]] += 1

    return tagSing

# Create a dicionary for the number of singleton words associated with each tag
def createWordSing(words, tags, pairHaps):
    wordSing = {}
    for tag in tags:
        wordSing[tag] = 0
    for pair in pairHaps:
        wordSing[pair[1]] += 1
    return wordSing

def calcTagBackoff(tag, tagDict, numTokens):
    return float(tagDict[tag])/float(numTokens)

def calcWordBackoff(word, wordDict, numTokens, numWords):
    return float(wordDict[word] + 1)/float(numTokens+numWords)


# Parse the given text, create emission and transition tables
def parseText(text, lam):
    tags = []
    words = []
    pairs = []
    numTokens = 0
    lines = text.splitlines()
    for line in lines:
        tokens = line.split("/")
        numTokens += 1
        words.append(tokens[0])
        tags.append(tokens[1])
        pairs.append((tokens[0], tokens[1]))

    tagDict = nltk.FreqDist(tags)
    tagDict["###"] -= 1
    tagPairs = nltk.bigrams(tags)
    tagPairDict = nltk.FreqDist(tagPairs)


    wordDict = nltk.FreqDist(words)
    wordDict["###"] -= 1
    numTokens -= 1
    pairDict = nltk.FreqDist(pairs)
    pairDict[("###", "###")] -= 1

    # Set the initial probabilities
    tagSet = list(set(tags))
    numTags = len(tagSet)
    for i in range(0, numTags):
        if(tagSet[i] != "###" ):
            initials.append(tagPairDict["###", tagSet[i]] / float(tagDict["###"]))
    print "INIT: " + str(initials)

    # Removing all instances of sentence boundaries
    tags = [i for i in tags if i != "###"]
    words = [i for i in words if i != "###"]
    pairs = [i for i in pairs if i != ("###", "###")]

    tagDict = nltk.FreqDist(tags)
    tagPairs = nltk.bigrams(tags)
    tagPairDict = nltk.FreqDist(tagPairs)
    wordDict = nltk.FreqDist(words)
    pairDict = nltk.FreqDist(pairs)

    wordSet = set(words)
    words = list(wordSet)
    print words
    tagSet = set(tags)
    tags = list(tagSet)
    print(tags)
    numWords = len(wordSet)
    numTags = len(tagSet)

    tagSing = createTagSing(tags, tagPairDict.hapaxes())
    wordSing = createWordSing(words, tags, pairDict.hapaxes())

    # Build transition table
    for i in range(0, numTags):
        x = []
        lam = 1.0 + float(tagSing[tags[i]])
        for j in range(0, numTags):
            #   p_tt-backoff(t_i | t_i-1) = p_t-unsmoothed(t_i) = c(t_i)/n
            backoff = calcTagBackoff(tags[j], tagDict, numTokens)
            calc = (tagPairDict[(tags[i], tags[j])]+lam*backoff) / float(tagDict[tags[i]]+lam)
            x.append(calc)
        transitions.append(x)

    # Build emissions table
    for i in range(0, numTags):
        x = []
        lam = 1.0 + float(wordSing[tags[i]])
        for j in range(0, numWords):
            #   p_tw-backoff(w_i | t_i) = p_w-addone(w_i) = c(w_i) + 1 / n+V
            backoff = calcWordBackoff(words[j], wordDict, numTokens, numWords)
            calc = (pairDict[(words[j], tags[i])]+lam*backoff) / float(tagDict[tags[i]]+lam)
            x.append(calc)
        emissions.append(x)

    # Build tag_dict
    for i in range(0, numWords):
        word = words[i]
        possible = []
        for j in range(0, numTags):
            if emissions[j][i] > 0.0:
                possible.append(j)
        tag_dict[word] = possible
    return words, tags

# Following the Viterbi algorithm, parse the given text and determine a tag for
# each observation
def Viterbi(text, words, tags, numTags, lam):
    testWords = []
    testTags = []
    lines = text.splitlines()
    for line in lines:
        tokens = line.split("/")
        testWords.append(tokens[0])
        testTags.append(tokens[1])

    # For each word in the sentence, determine the tag
    tagGuesses = []
    trellis = []
    n = len(testWords)
    prevState = "###"
    currentState = ""
    for t in range(0, n):
        if n % 1000 == 0:
            print "."
        if (t > 0):
            prevState = tagGuesses[t - 1]
        currentWord = testWords[t]
        if (testWords[t] == "###"):
            tagGuesses.append("###")
            trellis.append(initials)
            continue
        # Build the trellis
        else:
            currentTrellis = [0.0] * numTags
            if (currentWord not in words):
                for j in range(0, numTags):
                    maxProb = 0.0
                    for i in range(0, numTags):
                        prob1 = transitions[i][j] * lam  # p_tt(i_j | t_i)
                        totalProb = prob1 * trellis[t - 1][i]
                        if (totalProb > maxProb):
                            maxProb = totalProb
                    currentTrellis[j] = maxProb
            else:

                for j in tag_dict[currentWord]:
                    # Calculate v_t-1(j)a_ijb_j(o_t)
                    maxProb = 0.0
                    for i in tag_dict[currentWord]:
                        prob1 = transitions[i][j]  # p_tt(i_j | t_i)
                        prob2 = emissions[j][words.index(currentWord)]  # p_tw(w_j | t_j)

                        p12 = (prob1 * prob2)
                        totalProb = p12 * (trellis[t - 1][i])
                        if (totalProb > maxProb):
                            maxProb = totalProb

                    currentTrellis[j] = maxProb # Append to trellis

            trellis.append(currentTrellis)

            choice = tags[currentTrellis.index(max(currentTrellis))]
            tagGuesses.append(choice)

    correct = 0
    numKnown = 0
    knownCorrect = 0
    numNovel = 0
    novelCorrect = 0
    boundaries = 2
    for i in range(1, n - 1):
        if (testTags[i] == "###"):
            boundaries += 1
        if (tagGuesses[i] == testTags[i] and testTags[i] != "###"):
            correct += 1
        if(testWords[i] in words):
            numKnown += 1
            if(tagGuesses[i] == testTags[i] and testTags[i] != "###"):
                knownCorrect += 1
        else:
            numNovel += 1
            if(tagGuesses[i] == testTags[i] and testTags[i] != "###"):
                novelCorrect += 1

    acc = (round(correct / float(n - boundaries), 4)) * 100
    known = round(knownCorrect / float(numKnown), 4) * 100
    if(numNovel != 0):
        novel = round(novelCorrect / float(numNovel), 4) * 100
    else:
        novel = 0.0
    print "Tagging accuracy (Viterbi decoding): " + str(acc) + "% (known: " \
          + str(known) + "% novel: " + str(novel) +"%)"


def main():
    if (len(sys.argv) == 3):
        if (sys.argv[1] == "ictrain" and sys.argv[2] == "ictest"):
            o = open("data/ic/ictrain.txt", "r")
            text = o.read()
            words, tags = parseText(text, 0)
            # Process data
            print transitions
            print emissions
            o.close()

            test = open("data/ic/ictest.txt", "r")
            text = test.read()
            Viterbi(text, words, tags, len(tags), 0)
        elif ("entrain" in sys.argv[1] and "entest" in sys.argv[2]):
            o = open("data/en/" + str(sys.argv[1]) + ".txt", "r")
            text = o.read()
            # Process data
            words, tags = parseText(text, 1)
            o.close()

            test = open("data/en/" + sys.argv[2] + ".txt", "r")
            text = test.read()
            Viterbi(text, words, tags, len(tags), 1)
        else:
            print "error: wrong file names"


main()
