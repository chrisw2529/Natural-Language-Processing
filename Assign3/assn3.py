# Shawn Davidson
# Chris White
# CSCI 404 - Fall 2018
# Assignment 3
import random
import nltk
import math
from math import log10
from nltk import Text
import string



def generate_uni_model(fdist, word, vsize,  num=15):
    sentence = ""
    logProb = 0.0
    for i in range(num):
        sentence += word + " "
        if word in fdist:
            #print sentence
            word = random.choice(fdist.keys())
            wordCount = fdist[word]
            ratio = float(wordCount)/float(vsize)
            log = log10(ratio)
            logProb += log
            if (word == "</s>"):
                sentence += word + " "
                break
            elif (i == num - 1):
                sentence += "</s>"
        else:
            break
    print sentence
    print "probability (in log10 space) = " + str(logProb)



def generate_bi_model(cfdist, word, vsize, num=15):
    #print(cfdist[word])
    sentence = ""
    logProb = 0.0

    for i in range(num):
        sentence += word + " "
        if word in cfdist:
            temp = random.choice(cfdist[word].keys())
            wordCount = cfdist[word][temp]
            sum = 0.0
            for key in cfdist[word].keys():
                #print(cfdist[(word1,word2)][key])
                #print(key)
                sum += cfdist[word][key]
            ratio = (wordCount+0.01)/(sum + (vsize*0.01))
            log = log10(ratio)
            logProb += log
            word = temp
            if (word == "</s>"):
                sentence += word + " "
                break
            elif (i == num-1):
                sentence += "</s>"
        else:
            break
    print sentence
    print "probability (in log10 space) = " + str(logProb)
        # print(word + " ", end='')
        # randomNumber = random.randint(1,cfdist.N())
        # for j in cfdist:
        #     if(randomNumber == j):
        #         word = cfdist[word].max()
        # if(word == "</s>"):
        #     print(word + " ")
        #     break

def generate_tri_model(cfdist, word1, vsize, num=15):
    sentence = word1 + " "
    word2 = "<s>"
    logProduct = 0.0
    #keys = fdist.keys()
    for i in range(num):

        sentence += word2 + " "

        if (word1, word2) in cfdist:
            temp = random.choice(cfdist[(word1,word2)].keys())
            # print cfdist[(word1, word2)][temp]
            # print cfdist[(word1,word2)].keys()
            # generate log prob.


            sum = 0.0
            wordCount = cfdist[(word1, word2)][temp]
            for key in cfdist[(word1, word2)].keys():
                #print(cfdist[(word1,word2)][key])
                #print(key)
                sum += cfdist[(word1,word2)][key]
            #     if()
            ratio = (wordCount+0.01)/(sum + (vsize*0.01))
            log = log10(ratio)
            logProduct += log
            #print("sum= " + str(sum) + " wordCount= " + str(wordCount))


            word1 = word2
            word2 = temp
            #print word2



            #print sentence
            if (word2 == "</s>"):
                sentence +=  word2 + " "
                break
            elif (i == num - 1):
                sentence += "</s>"
        else:
            break


    print sentence
    print "probability (in log10 space) = " + str(logProduct)

def uni_perp(line, uniFreq, vocabSize):
    sum = 0.0
    words = line.split()

    for word in words:
        wordCount = uniFreq[word]
        #print "word: " + word + " " + str(wordCount)
        ratio = float(wordCount)/float(vocabSize)
        #print word + " " + str(wordCount) + " " + str(ratio)
        log = math.log(ratio, 2)
        sum += log

    # inv = -1 * (sum/float(len(testTokens)))
    # print "unicount= " + str(uniCount)
    return sum

def bi_perp(line, biFreq, vocabSize):
    sum = 0.0
    words = line.split()
    bigram = nltk.bigrams(words)
    for bgram in bigram:

        w1 = bgram[0]
        w2 = bgram[1]

        #print bgram
        wordCount = biFreq[w1][w2]

        w1Sum = 0.0
        for key in biFreq[w1].keys():
            # print "key frequency " + str(biFreq[w1][key])
            w1Sum += biFreq[w1][key]


        ratio = (float(wordCount)  + 0.01)/ (float(w1Sum ) + (0.01 * vocabSize))
        # print word + " " + str(wordCount) + " " + str(ratio)
        log = math.log(ratio, 2)
        sum += log
    # inv = -1 * (sum/float(len(testTokens)))
    # print "unicount= " + str(uniCount)
    return sum




    # sum = 0.0
    # ratioSum = 0.0
    # for bgram in test_bgram:
    #     w1 = bgram[0]
    #     w2 = bgram[1]
    #     wordCount = biFreq[w1][w2]
    #     # if (wordCount == 0):
    #     #     wordCount = biFreq[w1]["<UNK>"]
    #         #wordCount = 0.01
    #     w1Sum = 0.0
    #     for key in biFreq[w1].keys():
    #         #print "key frequency " + str(biFreq[w1][key])
    #         w1Sum += biFreq[w1][key]
    #     ratio = (float(wordCount)+0.01) / (w1Sum + (0.01*vocabSize))
    #     ratioSum += ratio
    #     log = math.log(ratio, 2)
    #     sum += log
    # inv = -1 * (sum / float(len(testTokens)))
    # print "ratioSum: " + str(ratioSum)
    # print sum
    # perp = math.pow(inv, 2)
    # print "Bigram Perplexity: " + str(perp)

def tri_perp(line, triFreq, tokenCount):
    sum = 0.0
    words = line.split()
    tgrams = nltk.trigrams(words)
    for tgram in tgrams:
        w1 = tgram[0]
        w2 = tgram[1]
        w3 = tgram[2]
        wordCount = triFreq[(w1,w2)][w3]

        # if (wordCount == 0):
        #     print "in statement"
        #     wordCount = triFreq[(w1,w2)]["<UNK>"]
            #wordCount = 0.01
        wSum = 0.0
        for key in triFreq[(w1,w2)].keys():
            wSum += triFreq[(w1,w2)][key]
        ratio = (float(wordCount) + 0.01) / (wSum + (0.01 * tokenCount))
        #print ratio
        log = math.log(ratio, 2)
        sum += log
    return sum


def main():
    trainIn = open("trainOutput.txt", "r")
    testText = trainIn.read()
    trainIn.close()

    # file = open("data/train.txt", "r")
    # lines = file.read()
    # sent = lines.splitlines()
    # print("# of sentences: " + str(len(sent)))
    # #testData = []
    # testText = ''
    # tokens = nltk.word_tokenize(lines)
    # print(len(set(tokens)))
    # freq = nltk.FreqDist(tokens)
    # singles = set(nltk.FreqDist.hapaxes(freq))
    #noSing = singles.sub("<UNK>", lines)
    # for i in range(0, len(singles)):
    #     for j in range(0, len(tokens)):
    #         if singles[i] == tokens[j]:
    #             tokens[j] = tokens[j].replace(tokens[j], "<UNK>")
    #print(noSing)
    word_dict = {}

    # file2 = open("data_export/train.txt", "r").read()
    # sent2 = file2.splitlines()
    # for i in sent2:
    #     for word in i.split():
    #         if word in word_dict:
    #             word_dict[word] += 1
    #         else:
    #             word_dict[word] = 1

    #print("# of singletons: " + str(len(singles)))



    # out = open("trainOutput.txt", "w+")
    # for line in sent:
    #     words = nltk.word_tokenize(line)
    #
    #     testText += "<s> "
    #
    #
    #     for i in range(0,len(words)):
    #        if words[i] in singles:
    #            words[i] = words[i].replace(words[i], "<UNK>")
    #        testText += words[i] + " "
    #     testText += "</s> "
    # out.write(testText)
    # out.close()

    vocab = testText.split()
    vocabFreq = nltk.FreqDist(vocab)
    print("# of tokens: " + str(len(vocab)))
    print("<s>" in set(vocab))
    print("</s>" in set(vocab))
    print("<UNK>" in set(vocab))
    totalTokens = len(vocab)
    vocabSize = len(set(vocab))
    print("vocabulary size: " + str(vocabSize))
    print "Generating Unigrams"
    print "=================================="
    for i in range(0,10):
        generate_uni_model(vocabFreq, "<s>", len(vocab))


    print "Generating Bigrams"
    print "=================================="
    bigrams = nltk.bigrams(vocab)
    # for pair in bigrams:
    #     print(pair)
    bigrmFreq = nltk.ConditionalFreqDist(bigrams)
    #print(bigrmFreq.most_common(15))
    for i in range (0,10):
        generate_bi_model(bigrmFreq, "<s>", len(vocab))

    print "Generating Trigrams"
    print "=================================="
    # out = open("trainTrigrams.txt", "w+")
    # triText = ""
    # for line in sent:
    #     words = nltk.word_tokenize(line)
    #     triText += "<s> <s> "
    #
    #     for i in range(0, len(words)):
    #         if words[i] in singles:
    #             words[i] = words[i].replace(words[i], "<UNK>")
    #         triText += words[i] + " "
    #     triText += "</s> "

    trainTri = open("trainTrigrams.txt", "r")
    triText = trainTri.read()
    tvocab = triText.split()
    tgrams = nltk.trigrams(tvocab)
    tgram_pairs = []
    for gram in tgrams:
        tgram_pairs.append(((gram[0], gram[1]), gram[2]))
    trifreq = nltk.FreqDist(tgrams)
    # out.write(triText)
    # out.close()
    #keys = trifreq.keys()

    # for key in keys:
    #     tgram_pairs.append(((key[0],key[1]), key[2]))

    tgFreq = nltk.ConditionalFreqDist(tgram_pairs)

    # print "first: "+str(tgFreq[("<s>", "<s>")]["also"])
    # print "second: "+str(tgFreq[("<s>", "<s>")].keys()[3])
    #print(tgFreq.keys()[0][0])
    # for key in tgFreq.keys():
    #     if key[0] == "<s>" and key[1] == "<s>":
    #         print str(key) + str(tgFreq[key])

    #print(tgFreq.most_common(20))
    for i in range(0,10):
        generate_tri_model(tgFreq, "<s>", len(tvocab))

    # Computing perplexities

    test = open("data/test.txt", "r")
    testLines = test.read()
    testSent = testLines.splitlines()

    testText = ""

    out = open("testOutput.txt", "w+")
    types = set(vocab)
    uniSum = 0.0
    biSum = 0.0
    triSum = 0.0
    totalWords = 0
    totalTriWords = 0
    for line in testSent:
        words = nltk.word_tokenize(line)
        oneLine = "<s> "
        triLine = "<s> <s>"
        totalWords += 1
        totalTriWords += 2
        for i in range(0,len(words)):
            if words[i] not in types:
                words[i] = words[i].replace(words[i], "<UNK>")
            oneLine += words[i] + " "
            triLine += words[i] + " "
            totalWords += 1
            totalTriWords += 1
        oneLine += "</s> "
        triLine += "</s> "
        totalWords += 1
        totalTriWords += 1
        testText += oneLine
        uniSum += uni_perp(oneLine, vocabFreq, totalTokens)
        biSum += bi_perp(oneLine, bigrmFreq, totalTokens)
        triSum += tri_perp(triLine, tgFreq, totalTokens)

    print "uni-perplexitySum= " + str(uniSum)
    inv = (-1/ float(totalWords) )* (uniSum)
    uniPlex = math.pow(2, inv)
    print "uniPlex= " + str(uniPlex)

    print "bi-perplexitySum= " + str(biSum)
    inv = -1 * (biSum / float(totalWords))
    biPlex = math.pow(2, inv)
    print "biPlex= " + str(biPlex)

    print "tri-perplexitySum= " + str(triSum)
    inv = -1 * (triSum / float(totalWords))
    triPlex = math.pow(2, inv)
    print "triPlex= " + str(triPlex)

    # testing = open("testOutput.txt", "r")
    # testText = testing.read()
    # testTokens = testText.split()
    out.write(testText)
    out.close()
    #uni_perp(testText, vocabFreq)

    #test_bgram = nltk.bigrams(testTokens)
    #bi_perp(set(test_bgram), bigrmFreq, len(vocab), testTokens)

    triText = ""
    triSum = 0.0
    totalWords = 0
    out = open("testOutputTrigrams.txt", "w+")
    for line in testSent:
        words = nltk.word_tokenize(line)
        oneLine += "<s> <s> "
        totalWords += 2
        for i in range(0, len(words)):
            if words[i] not in types:
                words[i] = words[i].replace(words[i], "<UNK>")
            oneLine += words[i] + " "
            totalWords += 1
        oneLine += "</s> "
        totalWords += 1
        triSum += tri_perp(oneLine, tgFreq, totalTokens)

    print "tri-perplexitySum= " + str(triSum)
    inv = -1 * (triSum / float(totalWords))
    triPlex = math.pow(2, inv)
    print "triPlex= " + str(triPlex)
    out.write(triText)
    out.close()

    #testTri = open("testOutputTrigrams.txt", "r")
    #triText = testTri.read()
    #t2vocab = triText.splitlines("</s>")
    #print(len(t2vocab))
    #test_tgram = nltk.trigrams(t2vocab)
    # for gram in test_tgram:
    #     print gram
    #tri_perp(set(test_tgram), tgFreq, len(tvocab))


main()
