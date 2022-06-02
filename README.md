#*Spam filter using a naive Bayes Theorem*

##The program contains: 
- Filter.py 
- 2 txt-s containing stop words and punctuation tokens 
- spam/ham emails stored in txt files

##Usage:
    The project was created using Pycharm, but something like VS Code could run the
    program. However you are going to need Python. Once the program is set up you are
    just going to have to run it. It will print some statistics about 2 tests it runs, after
    a learning phase. If you want to you can add new files for the test functions however
    the given files contain a known amount of ham emails and after the ham emails only spam emails.
    After the initial learning phase you can also test just 1 email using the test_mail
    function.

##Theory:
    The more "boring" part of the program. The program uses Bayes Theorem, during the initial
    learning phase it builds a dictionary out of the words in the emails. It calculates the probability
    of a word being inside a spam/ham email. The exact formulas used can be found in the Filter.py
    program (this is true for the rest of the formulas too). After it has built the dictionary,the program 
    is ready to be used, the test_email function uses the dictionary built in the initial learning phase. 
    Once again it calculates probability to determine wether or not the email it is currently working 
    with is either a spam or a ham. Thats about it :). One last feature of the program worth mentioning
    is the Lidstone smoothing feature. If this feature is turned on via the Flag in the begining of the 
    program then the program will calculate the probabilities in a different way.

##Output Statistics:
    - With the Lidstone smoothing turned off:
        Testing it on the emails it learned on it produces a miss percentage of: 0.19166267369429804
        This means the program got the email wrong 9 times out of the 4174 emails.

        Testing on new emails it produces a miss percentage of: 2.8477546549835706
        This means the program got the email wrong 44 times out of 1826 emails.

    - With the Lidstone smoothing turned on:
        Testing it on the emails it learned on it produces a miss percentage of: 0.7187350263536176
        This means the program got the email wrong 53 times out of the 4174 emails.

        Testing on new emails it produces a miss percentage of: 1.095290251916758
        This means the program got the email wrong 40 times out of 1826 emails.

    - Now the program can be (might be) optimised later if the dictionary and the probabilities would
    be updated after every tested email. Also the statistics are printed out in more detail by the
    program.

###Author: Bence Racz