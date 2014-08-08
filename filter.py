import sys
import re 

#---features for training

features = {"words": [],     #list of words (need right order)
            "spam_probs": {},   #probabilities 
            "ham_probs": {}
            }


def classify(message):
    words = features['words']
    spam_probs = features['spam_probs']
    ham_probs = features['ham_probs']

    print('Computing Probabilities...')

    w = message.split()
    for word in w:
        try:
            # P(S|W) = P(W|S)/( P(W|S) + P(W|H) )
            if word in words:
                prob = spam_probs[word] / (spam_probs[word] + ham_probs[word])
                print word + ': ' + str(prob)
        except ZeroDivisionError:
                print word + ': underflow'
    

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
            if values[-1][0] == '1': 
                spam_probs[word] = (spam_probs[word] + float(values[i]))/count
            else:
                ham_probs[word] = (ham_probs[word] + float(values[i]))/count

            count += 1

    classify('your credit report is overdue!')
    classify('hey, did you send me the files yet?')
    

