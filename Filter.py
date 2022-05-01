# Author: Bence Racz
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
alpha = 1

# This flag turns the Lidstone smoothing option
SmoothingFlag = True


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


# This function calculates the probability of a word being "spammy" or "hammy"
def calculate_probability(dictionary):
    sum_ham = sum(c.Counter.values(dictionary_ham))
    sum_spam = sum(c.Counter.values(dictionary_spam))

    for char in dictionary:
        if not SmoothingFlag:
            probabilities[char] = (dictionary_ham[char] / sum_ham, dictionary_spam[char] / sum_spam)
        else:
            probabilities[char] = (
                (dictionary_ham[char] + alpha) / ((len(dictionary_ham) + len(dictionary_spam)) * alpha + sum_ham),
                (dictionary_spam[char] + alpha) / ((len(dictionary_ham) + len(dictionary_spam)) * alpha + sum_spam))
    return


# This function evaluates given words and builds a dictionary for "hammy" and "spammy" words
def train():
    global prob_ham, prob_spam, dictionary_ham, dictionary_spam
    nr_of_ham = 0
    nr_of_spam = 0
    path_ham = "rsc/enron6/ham/"
    path_spam = "rsc/enron6/spam/"
    i = 0
    gym = open('rsc/train.txt')
    lines = gym.readlines()

    for line in lines:
        file = line.split('\n')
        if i < 1053:  # a ham file
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

    calculate_probability(dictionary_ham)
    calculate_probability(dictionary_spam)

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
            if not SmoothingFlag:
                if probabilities[word][0] == 0:
                    add_0 = 0.000000000000001
                else:
                    add_0 = 0
                if probabilities[word][1] == 0:
                    add_1 = 0.000000000000001
                else:
                    add_1 = 0
                prob1 = log(probabilities[word][1] + add_1)
                prob2 = log(probabilities[word][0] + add_0)
            else:
                prob1 = log(probabilities[word][1])
                prob2 = log(probabilities[word][0])
        lnR += word_occurrences[word] * (prob1 - prob2)

    return lnR


# This function returns the name of the test
def get_test_name(path):
    aux = path.split('/')
    aux = aux[len(aux) - 1]
    aux = aux.split('.')
    return aux[0]


# This function tests a folder filled with emails, the first nr_of_ham are ham emails and the rest spam
# after the test is completed it prints a statistic on the screen
def test(path, nr_of_ham):
    original_path = path
    mails = open(path)
    mails = mails.readlines()
    path_ham = "rsc/enron6/ham/"
    path_spam = "rsc/enron6/spam/"
    i = 0

    tested_ham = 0
    tested_spam = 0
    missed_ham = 0
    missed_spam = 0
    got_ham = 0
    got_spam = 0
    false_positive = 0
    false_negative = 0

    for path in mails:
        if i < nr_of_ham:
            file = path.split()
            file_path = path_ham + file[0]
        else:
            file = path.split()
            file_path = path_spam + file[0]

        if i < nr_of_ham:
            if test_mail(file_path) < 0:  # the algorithm got the correct answer
                got_ham += 1
            else:
                missed_ham += 1
                false_positive += 1
            tested_ham += 1
        else:
            if test_mail(file_path) > 0:  # the algorithm got the correct answer
                got_spam += 1
            else:
                missed_spam += 1
                false_negative += 1
            tested_spam += 1

        i += 1

    test_name = get_test_name(original_path)

    print('------------------The results of testing the ' + test_name + ' files------------------')
    print('       -Tested:                 ' + str(tested_ham + tested_spam) + ' files')
    print('       -Tested ham / Got ham:   ' + str(tested_ham) + '  /  ' + str(got_ham))
    print('       -Got ham:                ' + str(got_ham / tested_ham) + '   %')
    print('       -Missed ham:                ' + str(tested_ham - got_ham))
    print('       -Missed ham:             ' + str(1 - got_ham / tested_ham) + ' %')
    print('       -Tested spam / Got spam: ' + str(tested_spam) + '  /  ' + str(got_spam))
    print('       -Got spam:               ' + str(got_spam / tested_spam) + '   %')
    print('       -Missed spam:               ' + str(tested_spam - got_spam))
    print('       -Missed spam:            ' + str(1 - got_spam / tested_spam) + ' %')
    print('       -False_positive / false_negative: ' + str(false_positive / false_negative), end="\n\n")
    print('------------------Miss percentage: ' +
          str((missed_ham + missed_ham) / (tested_ham + tested_spam) * 100) + '--------------------')

    return


def main():
    fill_stop_words('rsc/stopwords.txt')
    fill_stop_words('rsc/stopwords2.txt')
    train()
    test('rsc/train.txt', 1053)
    test('rsc/test.txt', 447)

    return


if __name__ == '__main__':
    main()
