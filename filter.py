import sys
import re 

#---features for training

features = {"words": [],     #list of words (need right order)
            "spam_probs": {},   #probabilities 
            "ham_probs": {}
            }
  

if __name__ == '__main__':
    # get words from spamebase.names
    names = open('names', 'r').readlines()
    reg = re.compile('((char)|(word))_(freq)_([^:]+):')
    
    words = features['words']
    spam_probs = features['spam_probs']
    ham_probs = features['ham_probs']
    
    for line in names:
        try:
            m = reg.match(line)
            word = m.group(5)
            words.append(word)
            spam_probs[word] = 0
            ham_probs[word] = 0
        except AttributeError:
            continue
    
    # build probabilities from spambase.data
    # because UCI database doesn't tell us the length of 
    # each email, for now just average the percentages
    data = open('spambase.data', 'r').readlines()
    count = 1
    for line in data:
        values = line.split(',')
        for i in range(0,len(words)):
            word = words[i]
            if values[-1] == '0': # non-spam (ham)              
                ham_probs[word] = (ham_probs[word] + float(values[i]))/count
            else:
                spam_probs[word] = (spam_probs[word] + float(values[i]))/count

            count += 1

    print ham_probs
    print spam_probs
    

