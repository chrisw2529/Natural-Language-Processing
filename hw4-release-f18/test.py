#Chris White
#Shawn Davidson
#CSCI 404 assignment 4
#test.py: calculates the precision recall and fscore of a group of test documents using the naive bays formula

import os
import train
import nltk
import math

#findProbs returns the amount of occurences of a word in the dictionary (probs)
#returns 0 if the word is not found in the dictionary
#word: the word to be found in the dictionary
#probs: the dictionary to look for the word in
def findProbs(word, probs):
    for (allWords, count) in probs:
        if allWords == word:
            return count
    return 0

# calculates the naiveBays of a text file
# returns a boolean true for if the document was spam and false if it wasn't
# file: file being processed
# spamProbs: probabilities a word is spam
# nonSpamProbs: probabilities a word is not spam
# dict: dict of the most common words (size determined by variable size in train.py)
def naiveBays(fileName, spamProbs, nonSpamProbs, dict):
    fileText = open(fileName).read()
    fileText = nltk.word_tokenize(fileText)
    fileSpamProb = math.log(.5, 2)
    fileNotSpamProb = math.log(.5, 2)

    for word in fileText:
        count = float(train.find(dict, word))
        if (count != 0.0):
            probWord = count / float(dict.tokens)

            #checks if word in spam and calculates prob
            probSpam = findProbs(word, spamProbs)
            if(probSpam != 0.0 and probWord != 0.0):
                wordSpamProb = math.log(probSpam, 2)
                fileSpamProb += wordSpamProb



            #checks if word NOT in spam and calculates prob
            probNotSpam = findProbs(word, nonSpamProbs)
            if (probNotSpam != 0.0 and probWord != 0.0):
                wordNotSpamProb = math.log(probNotSpam, 2)
                fileNotSpamProb += wordNotSpamProb


    if(fileSpamProb >= fileNotSpamProb):
        return True
    else:
        return False





def main():
    spamProbs, nonSpamProbs, dict = train.main()

    # spamFile = open("data/spamProbs.txt", "w+")
    # spamFile.write(str(spamProbs))
    #
    # nonspamFile = open("data/nonSpamProbs.txt", "w+")
    # nonspamFile.write(str(nonSpamProbs))
    #
    # dictFile = open("data/dict.txt", "w+")
    # dictFile.write(str(dict.dict))

    #true positve and false positive
    tp = 0
    fp = 0
    for file in os.listdir("data/spam-test/"):
        if file.endswith(".txt"):
            isSpam = naiveBays("data/spam-test/" + str(file), spamProbs, nonSpamProbs, dict)
            if(isSpam):
                tp += 1
            else:
                fp += 1


    print "True Positive= " + str(tp)
    print "False Positive= " + str(fp)

    #false negative and true negative
    fn = 0
    tn = 0
    for file in os.listdir("data/nonspam-test/"):
        if file.endswith(".txt"):
            isSpam = naiveBays("data/nonspam-test/" + str(file), spamProbs, nonSpamProbs, dict)
            if(isSpam):
                fn += 1
            else:
                tn += 1


    print "False Negative= " + str(fn)
    print "True Negative= " + str(tn)

    precision = tp/ float(tp + fp)
    recall = tp/float(tp + fn)
    print "Precision= " + str(precision)
    print "Recall= " + str(recall)

    fScore = 2*precision * recall / (precision + recall)
    print "F Score= " + str(fScore)




main()