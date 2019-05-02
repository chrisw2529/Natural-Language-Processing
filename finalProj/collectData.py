import praw
from praw.models import MoreComments
import datetime

sarcComments = []

def readReplies(comment, regFile, sarcFile):
    replies = comment.replies
    for reply in replies:
        if isinstance(reply, MoreComments):
            continue
        body = reply.body.lower()
        tokens = body.split(". ")
        if ("/s" in reply.body  and "https" not in reply.body):
            pos = reply.body.index("/s")
            if (pos + 2 < len(reply.body) and reply.body[pos + 2].isalpha()):
                #dropped.write(reply.body + "\n")
                print("IN IF STATMENT")
                continue
            sarcFile.write("  ~cmt~ " + reply.body + " ~end~ \n")
        #else:
            #regFile.write("  ~cmt~ " + reply.body + " ~end~ \n")
        readReplies(reply, regFile, sarcFile)


def readComments(submission, regFile, sarcFile):
    #file = open("comments.txt", "w+")
    comments = submission.comments
    for comment in comments:
        if isinstance(comment, MoreComments):
            continue
        body = comment.body.lower()
        tokens = body.split(". ")
        if("/s" in comment.body and "https" not in comment.body):
            pos = comment.body.index("/s")
            if(pos+2 < len(comment.body) and comment.body[pos+2].isalpha()):
                #dropped.write(comment.body + "\n")
                print("IN IF STATMENT")
                continue
            sarcFile.write("  ~cmt~ " + comment.body + " ~end~ \n")
        else:
            regFile.write("  ~cmt~ " + comment.body + " ~end~ \n")
        readReplies(comment, regFile, sarcFile)
    #file.close()

def main():
    reddit = praw.Reddit(client_id='qGIyN9bTIN9q9Q',
                         client_secret='8Ikzq1_l4Nrx0bFtMYRXlalj0JE',
                         user_agent='SarcasmDetector',
                         username='NLPSarcasm',
                         password='CSCInlp404')
    sub = reddit.subreddit('politics')
    print(sub.title)

    # reg = open("regJokeComments.txt", "w+")
    # sarc = open("sarcJokeComments.txt", "w+")
    # currTime = datetime.datetime.now()
    # for submission in sub.top(limit=5000):
    #     print("================================")
    #     print(submission.title)
    #     print(submission.score)
    #     print(submission.id)
    #     print(submission.url)
    #     # reg.write(submission.title + "\n")
    #     # sarc.write(submission.title + "\n")
    #     readComments(submission, reg, sarc)
    # reg.close()
    # sarc.close()

    reg = open("regTestComments.txt", "w+")
    sarc = open("sarcTestComments.txt", "w+")
    currTime = datetime.datetime.now()
    for submission in sub.hot(limit=50):
        print("================================")
        print(submission.title)
        print(submission.score)
        print(submission.id)
        print(submission.url)
        # reg.write(submission.title + "\n")
        # sarc.write(submission.title + "\n")
        readComments(submission, reg, sarc)
    reg.close()
    sarc.close()
    print("Data retrieved at: " + str(currTime))

main()
