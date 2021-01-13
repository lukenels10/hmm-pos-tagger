import json
import sys

#Bring in the params from hmmmodel.txt
with open("hmmmodel.txt") as file:
    params = json.load(file)

q0=params['q0']
qf=params['qf']
transition_matrix=params['transition_matrix']
emmission_matrix_2=params['emmission_matrix']    #{'VB':{'cat':2,'dog':7}, 'NN':['cat':5,..],...}
vocabulary=params['vocabulary']
emmission_matrix=params['wordsAskeys_emmission_matrix']     #{'cat':{VB:2, NN:3},'dog':{VB:7, IN:3},....}
tag_counts = params['tag_counts']



#read in the test file
input_path=sys.argv[1]

file = open(input_path, 'r')

lines=file.readlines()
file.close()

#Create new txt file
text_file = open("hmmoutput.txt", "w")

sentence_counts=0

for line in lines:
    sentence_counts +=1
    #print('\nSTARTING A NEW SENTENCE!!!!!!!!!!!!!!!!!!!!!!\n')
    #print(sentence_counts)
    #print(line)
    line=line.rstrip()    #Get rid of newline characters
    words = line.split(' ')    #Put all words in the line into a list

    
    counter=1    #so that we know the first word and the last word
    last_word = len(words)    #How many words are there? if 8 words in the sentence, this will be 8
    probabilities = dict()
    
    for word in words:
        if word in vocabulary:
            emmissions = emmission_matrix[word]    #just the emmissions for the word we are looking at
        else:
            emmissions = None
        
        #######What we do for the first word##############
        if counter == 1:    #If we are looking at the first word
            if emmissions is None:
                for a,b in q0.items():    #If the word isnt in the vocab, then just use the initial probabilities
                    probabilities[(a,)] = b
            else:
                for a,b in emmissions.items():   #Otherwise multiply the first emmission state by the possible transitions
                    try:
                        probabilities[(a,)] = b * q0[a]
                    except:
                        probabilities[(a,)] = 0

            
            
        ########What we do for the remaining words###########            
        elif counter < last_word+1:
            if emmissions is None:
                new_probabilities = dict()
                for a,b in probabilities.items():
                    initial_tag = a[-1]
                    possible_transitions = transition_matrix[initial_tag]
                    #######################v3 Addition Here#######################
                    condense=list()
                    for r,s in possible_transitions.items():
                        condense.append((s,r))
                    condense.sort(reverse=True)
                    if len(condense) < 8:
                        condensed=condense
                    else:
                        condensed=condense[:7]
                    
                        
                    
                    #######################End of V3 Addition#####################
                    
                    for j,k in condensed:
                        prob = j
                        new_probabilities[a+(k,)] = prob * b    #Create a new tuple entry in probabilities dictionary which is the prob calculated by b (the probability already there)
                    ############# I changed the above a bit toooo###################
                    
                #print('\nPROBABILITIES:',probabilities)
                #Update the dictionary
                trimmed_probabilities = dict()
                possible_enders = list()


                for seq, pr in new_probabilities.items():
                    possible_enders.append(seq[-1])

                possible_enders = list(set(possible_enders))


                for g in possible_enders:
                    temp=list()
                    for seq, pr in new_probabilities.items():
                        if seq[-1] == g:
                            temp.append((pr,seq))

                    temp.sort(reverse=True)
                    best_seq=temp[0][1]
                    best_prob=temp[0][0]


                    trimmed_probabilities[best_seq]=best_prob
                
                
                
                
                probabilities = trimmed_probabilities
            
            
            else:

                new_probabilities = dict()    #New dictionary because we iterate through probabilities dict later and need this

                #Create a list of the possible tags for that word
                possible_tags = list()    #A list of the tags that the word has emmission probabilities for
                for m,n in emmissions.items():
                    possible_tags.append(m)
  

                for a,b in probabilities.items():
                    initial_tag = a[-1]
                    possible_transitions = transition_matrix[initial_tag]
                
                ###############Added to fix the unseen transition issue##############
                    checker=list()
                    for c,d in possible_transitions.items():
                        checker.append(c)
                    
                    for e in possible_tags:
                        if e not in checker:
                            possible_transitions[e]=1 / tag_counts[e]
                ###############End of my addition###################################    

                    #Go through the transitions to see if any of the new tags can be applied to the word at hand
                    for j,k in possible_transitions.items():
                        if j in possible_tags:
                            prob = k * emmissions[j]
                            new_probabilities[a+(j,)] = prob * b    #Create a new tuple entry in probabilities dictionary which is the prob calculated by b (the probability already there)
                
                #print('\nPROBABILITIES:',probabilities)
                #update the dictionary ###Get rid of the dupicate ends tags with lower probability
                trimmed_probabilities = dict()
                possible_enders = list()


                for seq, pr in new_probabilities.items():
                    possible_enders.append(seq[-1])

                possible_enders = list(set(possible_enders))


                for g in possible_enders:
                    temp=list()
                    for seq, pr in new_probabilities.items():
                        if seq[-1] == g:
                            temp.append((pr,seq))

                    temp.sort(reverse=True)
                    best_seq=temp[0][1]
                    best_prob=temp[0][0]


                    trimmed_probabilities[best_seq]=best_prob
                
                
                
                
                probabilities = trimmed_probabilities

        
        counter += 1                
                
    #print('\nPROBABILITIES:',probabilities)            
    #Calculate qf, the end state
    final_probabilities = dict()
    for a,b in probabilities.items():
        qf_tag = a[-1]
        try:
            final_prob = qf[qf_tag] * b
        except:    #If the tag does not exist in our qf dictionary we give the probability to be 0
            final_prob = b * (1/tag_counts[qf_tag])    #This was my v3 change
        
        final_probabilities[a] = final_prob
        
    #find the most likely sequence by sorting the dictionary from probabilities largest to smallest
    sorter=list()
    for a,b in final_probabilities.items():
        sorter.append((b,a))

    sorter.sort(reverse=True)
    #print('SORTED:',sorter)
    sequence = sorter[0][1]
    sequence = list(sequence)
    
    
    #Create line to be written to the text file:
    tagged_sentence=''
    for i in range(len(words)):
        tagged = words[i]+'/'+sequence[i]+' '
        tagged_sentence=tagged_sentence + tagged
        
    text_file.write(tagged_sentence+'\n')
        
    
    
            
        
text_file.close()        
        
        