# Hidden Markov Model Italian & Japanese Part-of-Speech Tagger

## Overview
In this assignment you will write a Hidden Markov Model part-of-speech tagger for Italian, Japanese, and a surprise language. The training data are provided tokenized and tagged; the test data will be provided tokenized, and your tagger will add the tags. The assignment will be graded based on the performance of your tagger, that is how well it performs on unseen test data compared to the performance of a reference tagger.

## Data
A set of training and development data is available as a compressed ZIP archive on Blackboard. The uncompressed archive will have the following files:

* Two files (one Italian, one Japanese) with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
* Two files (one Italian, one Japanese) with untagged development data, with words separated by spaces and each sentence on a new line.
* Two files (one Italian, one Japanese) with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.
* A readme/license file (which you won’t need for the exercise). <br>

The grading script will train your model on all of the tagged training and development data (separately for Italian and Japanese), and test the model on unseen data in a similar format. The grading script will do the same for the surprise language, for which all of the training, development and test data are unseen.

## Programs
You will write two programs in Python 3 (Python 2 has been deprecated): hmmlearn.py will learn a hidden Markov model from the training data, and hmmdecode.py will use the model to tag new data.

The learning program will be invoked in the following way:

> python hmmlearn.py /path/to/input

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. The format of the model is up to you, but it should follow the following guidelines:

* The model file should contain sufficient information for hmmdecode.py to successfully tag new data.
* The model file should be human-readable, so that model parameters can be easily understood by visual inspection of the file. <br>

The tagging program will be invoked in the following way:

> python hmmdecode.py /path/to/input

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

The accuracy of your tagger is determined by a scoring script which compares the output of your tagger to a reference tagged text. Note that the tagged output file hmmoutput.txt must match line for line and word for word with the input to hmmdecode.py. A discrepancy in the number of lines or in the number of words on corresponding lines could cause the scoring script to fail.
