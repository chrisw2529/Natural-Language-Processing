# Shawn Davidson, Chris White
# Final Project - Sarcasm Detection
# train.py - Create a training and testing data set and runs naive bays and cosine similarity on the data sets
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from math import acos
from dict import Dictionary
import math
import nltk

stopwords = []
fullDict = []

#what type of characters are removed from the comments
splitBy = '[; "^.*,\n|><()?!@#&[/:_=\]]'
weight = 1

# Process the set of regular comments
# breaks up all of the comments based on the start tag ~cmt~ and the end tag ~end~ and returns a list of all of them
# only returns the same amount of regular comments as sarcastic comments
# train is a boolean that indicates weather or not we are processing training or testing data
def processReg(regComments, train):
    regDictCollect = []
    currComment = ""
    currDoc = -1
    words = re.split(splitBy, regComments)
    for i in range(len(words)):
        #print words[i]
        if(words[i] == "~cmt~"):
            currDict = {}
            currComment = ""
        elif(words[i] == "~end~"):
            if(currComment != ""):
                regDictCollect.append(currComment)
                currDoc += 1
                if(currDoc > (107)   and (train == False)):

                    return regDictCollect
                if(currDoc > (3232)  and train):
                    return regDictCollect


        else:
            if(words[i] not in stopwords and words[i] != '' and words[i] != "~cmt~" and words[i].isdigit() == False):
                currComment += words[i] + " "
                if(train and words[i] not in fullDict):
                    fullDict.append(words[i])

    return regDictCollect


def dictToFile(dict, file):
    length = len(dict)
    for i in range(0, length):
        file.write("~start~  \n")
        for entry in dict[i]:
            #TODO: there are multiple types of quotes that we can't search for and emojis
            file.write(entry + ": " + str(dict[i][entry]) + "\n")
        file.write("~end~  \n")
    file.close()

# Process the sarcastic comments
# breaks up all of the comments based on the start tag ~cmt~ and the end tag ~end~ and returns a list of all of them
# train is a boolean that indicates weather or not we are processing training or testing data
def processSarc(sarcComments, train):
    sepSarcComments = []
    currComment = ""
    currDoc = -1
    words = re.split(splitBy, sarcComments)
    for word in words:

        if (word == "~end~"):
            if(currComment != ""):
                sepSarcComments.append(currComment)
                currDoc += 1
            currComment = ""

        else:
            if (word not in stopwords and word != '' and word != "~cmt~" and word.isdigit() == False):
                currComment += word + " "
                if (train and word not in fullDict):
                    fullDict.append(word)

    return sepSarcComments


# cosineSimilarity calculats the average cosine angle between a the test comment and all comments in trainMatrix
# (comments must be passed in vector form)
# testComment: the comment that is going to be compared to the the trainMatrix
# trainMatrix: the list of comments that the test comment is compated to
# returns the average cosine angle between the testComment and the list of comments
def cosineSimilarity(testComment, trainMatrix):
    cosim = cosine_similarity(testComment, trainMatrix)
    sum = 0.0
    length = len(cosim[0])
    divisor = length
    for i in range(0, length):
        if((cosim[0][i]) <= 1.0):
            cosval = acos(cosim[0][i])
            if(cosim[0][i] >= .1 ):
                sum += cosval * weight
            else:
                sum += cosval
            if (cosim[0][i] == 0 ):
                divisor = divisor - 1
    if(divisor == 0):
        return 0
    ave = sum / float(divisor)

    return ave

######## from test assgn4 #########

# findProbs returns the amount of occurrences of a word in the dictionary (probs)
# returns 0 if the word is not found in the dictionary
# word: the word to be found in the dictionary
# : the dictionary to look for the word in
def findProbs(word, probs):
    for (allWords, count) in probs:
        if allWords == word:
            return count
    return 0

# calculates the naiveBays of a text file
# returns a boolean true for if the document was sarcastic and false if it wasn't
# file: file being processed
# sarcProbs: probabilities a word is in a sarcastic comment
# regProbs: probabilities a word is in a regular comment
# dict: dict of the most common words (size determined by variable size in train.py)
def naiveBays(comment, sarcProbs, regProbs, dict):
    passedComment = nltk.word_tokenize(comment)
    fileSarcProb = math.log(.5, 2)
    fileRegProb = math.log(.5, 2)

    for word in passedComment:
        count = float(find(dict, word))
        if (count != 0.0):
            probWord = count / float(dict.tokens)

            #checks if word in sarc and calculates prob
            probSarc = findProbs(word, sarcProbs)
            if(probSarc != 0.0 and probWord != 0.0):
                wordSarcProb = math.log(probSarc, 2)
                fileSarcProb += wordSarcProb

            #checks if word is in reg and calculates prob
            probReg = findProbs(word, regProbs)
            if (probReg != 0.0 and probWord != 0.0):
                wordRegProb = math.log(probReg, 2)
                fileRegProb += wordRegProb


    if(fileSarcProb >= fileRegProb):
        return True
    else:
        return False


######## From train Assgn4 ########

# Find the given word, return the # of occurrences,
# return 0 if not found
def find(dict, findWord):
    for (word, count) in dict.dict:
        if word == findWord:
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

def main():
    trainReg = open("textfiles/actualData/regComments.txt", "r")
    trainSarc = open("textfiles/actualData/sarcComments.txt", "r")
    stop = open("textfiles/stopwords.txt", "r")
    testReg = open("textfiles/actualData/regTestComments.txt", "r")
    testSarc = open("textfiles/actualData/sarcTestComments.txt", "r")

    stopText = stop.readlines()
    for line in stopText:
        word = line.replace("\r", "")
        word = line.replace("\n", "")
        stopwords.append(word)

    # Process files
    regTrainComms = trainReg.read()
    sarcTrainComms = trainSarc.read()
    regTestComms = testReg.read()
    sarcTestComms = testSarc.read()
    # list of all comments in txt file
    sepRegTrainComms = processReg(regTrainComms.lower(), True)
    sepSarcTrainComms = processSarc(sarcTrainComms.lower(), True)
    sepRegTestComments = processReg(regTestComms.lower(), False)
    sepSarcTestComments = processSarc(sarcTestComms.lower(), False)

    # Creates a dictionary of a sarcastic and non-sarcastic comments
    sarcDict = Dictionary(sepSarcTrainComms)
    regDict = Dictionary(sepRegTrainComms)

    allTrain = sepSarcTrainComms + sepRegTrainComms
    dict = Dictionary(allTrain)

    # generates word probabilities based on occurences used to compute naive bayes
    sarcProbs = genProb(sarcDict, dict)
    regProbs = genProb(regDict, dict)

    tp = 0
    fp = 0
    for comment in sepSarcTestComments:
        isSarc = naiveBays(comment, sarcProbs, regProbs, dict)
        if (isSarc):
            tp += 1
        else:
            fp += 1

    fn = 0
    tn = 0
    for comment in sepRegTestComments:
        isSarc = naiveBays(comment, sarcProbs, regProbs, dict)
        if (isSarc):
            fn += 1
        else:
            tn += 1

    print("Naive Bayes")

    print ("True Positive= " + str(tp))
    print ("False positive= " + str(fp))
    print ("False Negative= " + str(fn))
    print ("True Negative= " + str(tn))

    precision = tp / float(tp + fp)
    recall = tp / float(tp + fn)
    print ("Precision= " + str(precision))
    print ("Recall= " + str(recall))

    fScore = 2 * precision * recall / (precision + recall)
    print ("F Score= " + str(fScore))

    ######## Cosine Similarity ########

    vec = TfidfVectorizer(min_df=4)
    vec.vocabulary = fullDict

    sarcTrainVectors = vec.fit_transform(sepSarcTrainComms)
    regTrainVectors = vec.fit_transform(sepRegTrainComms)

    sarcTestVectors = vec.fit_transform(sepSarcTestComments)
    regTestVectors = vec.fit_transform(sepRegTestComments)

    tpcs = 0.0
    fpcs = 0.0
    for i in range(len(sepSarcTestComments)):
        ave = cosineSimilarity(sarcTestVectors[i:i+1], regTrainVectors)
        sarcAve = cosineSimilarity(sarcTestVectors[i:i+1], sarcTrainVectors)
        if(sarcAve <= ave):
            tpcs += 1
        else:
            fpcs += 1

    tncs = 0.0
    fncs = 0.0
    for i in range(len(sepRegTestComments)):
        ave = cosineSimilarity(regTestVectors[i:i + 1], regTrainVectors)
        sarcAve = cosineSimilarity(regTestVectors[i:i + 1], sarcTrainVectors)
        if (ave <= sarcAve):
            tncs += 1
        else:
            fncs += 1

    print()
    print("Cosine Sim: ")

    print ("True Positive= " + str(tpcs))
    print ("False positive= " + str(fpcs))
    print ("False Negative= " + str(fncs))
    print ("True Negative= " + str(tncs))

    precision = tpcs / float(tpcs + fpcs)
    recall = tpcs / float(tpcs + fncs)
    print ("Precision= " + str(precision))
    print ("Recall= " + str(recall))

    fScore = 2 * precision * recall / (precision + recall)
    print ("F Score= " + str(fScore))

    trainReg.close()
    trainSarc.close()
    stop.close()
    testReg.close()
    testSarc.close()


main()
