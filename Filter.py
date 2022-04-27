# Racz Bence, 523/2
import collections as c
from math import log

stop_words = []
punctuation_tokens = [',', '.', '!', '"', '`', "'", '@', '#', '?', ':', ';', '|', '*', '+', '-', '0', '1',
                      '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '$', '/', '_', '%', '=', '>', '<']
dictionary_ham = c.Counter()
dictionary_spam = c.Counter()
probabilities = c.Counter()
prob_spam = 0
prob_ham = 0
alpha = 0.0000000000000000001


# The function removes unwanted tokens
def remove_tokens(text):
    j = 0
    while j < len(text):
        if text[j] in punctuation_tokens:
            text.remove(text[j])
        else:
            j += 1

    j = 0
    while j < len(text):
        if text[j] in stop_words:
            text.remove(text[j])
        else:
            j += 1

    return text

# The function reads given stop words from a file, the path is entered as a parameter
def fill_stop_words(path):
    file_1 = open(path, 'r')
    stop_words.append('subject:')
    for line in file_1:
        word = line.split('\n')
        stop_words.append(word[0])
    return


# This function evaluates given words and builds a dictionary for "hammy" and "spammy" words
def train():
    global prob_ham, prob_spam, dictionary_ham, dictionary_spam
    nr_of_ham = 0
    nr_of_spam = 1
    path_ham = "rsc/enron6/ham/"
    path_spam = "rsc/enron6/spam/"
    i = 0
    gym = open('rsc/train.txt')
    lines = gym.readlines()

    for line in lines:
        file = line.split('\n')
        if i < 1053:       # a ham file
            path = path_ham + file[0]
        else:
            path = path_spam + file[0]

        email = open(path, 'r', encoding='latin-1')

        text = email.read()

        text = text.lower()
        email_contents = text.split()
        email_contents = remove_tokens(email_contents)

        if i < 1053:
            dictionary_ham.update(email_contents)
            nr_of_ham += 1
        else:
            dictionary_spam.update(email_contents)
            nr_of_spam += 1

        i += 1

    for char in dictionary_ham:
        probabilities[char] = (dictionary_ham[char] / nr_of_ham, dictionary_spam[char] / nr_of_spam)

    for char in dictionary_spam:
        probabilities[char] = (dictionary_ham[char] / nr_of_ham, dictionary_spam[char] / nr_of_spam)

    prob_ham = nr_of_ham / (nr_of_ham + nr_of_spam)
    prob_spam = nr_of_spam / (nr_of_ham + nr_of_spam)

    return


# The function tests a mail and returns if it's spam or ham
#
# return < 1 ==> HAM
# return > 1 ==> SPAM
def test_mail(path):
    email = open(path, 'r', encoding='latin-1')
    mail = email.read()
    lnR = log(prob_spam) - log(prob_ham)
    mail = remove_tokens(mail.lower().split())
    word_occurrences = c.Counter(mail)

    for word in mail:
        if probabilities[word] == 0:
            prob1 = 0.0
            prob2 = 0.0
        else:
            prob1 = log(probabilities[word][1] + alpha)
            prob2 = log(probabilities[word][0] + alpha)
        lnR += word_occurrences[word] * (prob1 - prob2)

    return lnR


def test_test_mails():
    mails = open()
    return


def main():
    fill_stop_words('rsc/stopwords.txt')
    fill_stop_words('rsc/stopwords2.txt')
    train()
    test_test_mails()

    return


if __name__ == '__main__':
    main()
