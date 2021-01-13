import json
import sys

#Read in the training file

input_path=sys.argv[1]

file = open(input_path, 'r')

#Variables
number_of_sentences = 0    # Number of sentences
tag_0_counts = dict()    # q0: counts of each tag in the first position of the sentence
tag_f_counts = dict()    # qf: counts of each tag in the last position of the sentence
transition_counts = dict()    #counts of each tag to tag for transition matrix
tag_counts = dict()    #Total count for each tag
transition_matrix = dict()    #The final transition matrix
word_counts = dict()    #Counts from each tag to word for emmission matrix
emmission_matrix = dict()    #The final Emmission matrix
wordsAskeys_emmission_matrix = dict()
vocabulary = list()
wordsAskeys_tag_counts = dict()    #{'cat':{VB:2, NN:3},'dog':{VB:7, IN:3},....}

lines=file.readlines()
for line in lines:
    number_of_sentences += 1
    line=line.rstrip()    #Get rid of newline characters
    
    ##############################
    ## Create transition matrix and Emmission matrix dictionaries ##
    ##############################
    
    words = line.split(' ')    #Put all words in the line into a list
    #print(words)
    
    ####Tags for creating q0 and qf
    tag_0 = words[0]
    tag_0 = tag_0.rsplit('/', 1)[-1]    #Gives us the tag of the first word in each sentence
    tag_f = words[-1]
    tag_f = tag_f.rsplit('/', 1)[-1]    #Gives us the tag of the last word in each sentence
    
    tag_0_counts[tag_0] = tag_0_counts.get(tag_0, 0) + 1    #Create ditionary of counts for initial tags
    tag_f_counts[tag_f] = tag_f_counts.get(tag_f, 0) + 1    #Create ditionary of counts for final tags
    
    
    for i in range(len(words)):
        word_list = words[i].rsplit('/', 1)
        tag = word_list[-1]      #For each word we now have the tag
        plain_word = word_list[0]    # and simply the word
        vocabulary.append(plain_word)

        if i == len(words)-1:
            next_tag = None
        else:
            next_tag = words[i+1].rsplit('/', 1)[-1]

        if next_tag is not None:    #Create the transition counts dictionary
            transition_counts_inner=transition_counts.get(tag,{})
            transition_counts_inner[next_tag]=transition_counts_inner.get(next_tag,0)+1
            transition_counts[tag]=transition_counts_inner

        
        tag_counts[tag]=tag_counts.get(tag, 0) + 1    #keep track of tag counts
        
        word_counts_inner = word_counts.get(tag,{})
        word_counts_inner[plain_word] = word_counts_inner.get(plain_word, 0)+1
        word_counts[tag]=word_counts_inner
        
        #wordsAskeys_emmision_matrix
        wordsAskeys_inner = wordsAskeys_tag_counts.get(plain_word, {})
        wordsAskeys_inner[tag] = wordsAskeys_inner.get(tag, 0) + 1
        wordsAskeys_tag_counts[plain_word]=wordsAskeys_inner
        
 

#Calculate q0
q0 = dict()

for tag, count in tag_0_counts.items():
    q0[tag] = count / number_of_sentences    #Create the q0 dictionary of initial state probabilities


#Calculate qf
qf = dict()

for tag, count in tag_f_counts.items():
    qf[tag] = count / tag_counts[tag]


#calculate Transition Matrix
for a,b in transition_counts.items():
    for j,k in b.items():
        probability = k / tag_counts[a]
        transition_matrix_inner = transition_matrix.get(a,{})
        transition_matrix_inner[j] = probability
        transition_matrix[a]=transition_matrix_inner

#calculate Emmission Matrix
for a,b in word_counts.items():
    for j,k in b.items():
        probability = k / tag_counts[a]
        emmission_matrix_inner = emmission_matrix.get(a,{})
        emmission_matrix_inner[j] = probability
        emmission_matrix[a]=emmission_matrix_inner

#Calculate words as keys emmission matrix
for a,b in wordsAskeys_tag_counts.items():
    for j,k in b.items():
        probability = k / tag_counts[j]
        wordsAskeys_emmission_matrix_inner = wordsAskeys_emmission_matrix.get(a,{})
        wordsAskeys_emmission_matrix_inner[j] = probability
        wordsAskeys_emmission_matrix[a]=wordsAskeys_emmission_matrix_inner
        
        
#keep only the unique characters from the vocabulary
vocabulary=list(set(vocabulary))








#Export to a text file
#Place all of the parameters in a dictionary to read into your text file

params=dict()

params['q0'] = q0
params['qf'] = qf
params['transition_matrix'] = transition_matrix
params['emmission_matrix'] = emmission_matrix
params['vocabulary'] = vocabulary
params['wordsAskeys_emmission_matrix'] = wordsAskeys_emmission_matrix
params['tag_counts'] = tag_counts


#Write the params dictionary to a text file
with open('hmmmodel.txt', 'w') as file:
     file.write(json.dumps(params)) # use `json.loads` to do the reverse



file.close()