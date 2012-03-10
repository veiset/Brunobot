import sys
''' Required for Brunobot module'''
version     = '4.0'
name        = 'typofixer'
author      = 'Vegard Veiset' # optional
url         = 'http://veiset.org/svn/bruno/module/typo.py' # optional
require     = ['communication','recentdata']
listen      = ['channel','privmsg']
description = 'correct a typo from the last sentence a user wrote'
usage       = '*correctWord' 

def distance(s1, s2):
    ''' 
    distance() -> levenshtein distance between two strings
    
    Keyword arguments:
    s1 -- string one
    s2 -- string two
    '''

    if len(s1) < len(s2):
        return distance(s2, s1)
    if not s1:
        return len(s2)
 
    row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current = [i + 1]

        for j, c2 in enumerate(s2):
            # find the min cost of deletion, insertion and substitution
            current.append(min(row[j+1]+1, current[j]+1, row[j]+(c1 != c2)))

        row = current
 
    return row[-1]


def sentenceDist(sentence, typo):
    ''' 
    sentenceDist() -> the best match against all the sentence combinations
                      

    Keyword arguments:
    s1  --  Sentence to match against 
    s2  --  Flagged typo 
    '''
    
    words = sentence.split(' ')
    results = []

    for start in range(len(words)):

        for end in range(start,len(words)+1):
            suggestedFix = " ".join(words[start:end])
            dist = distance(typo, suggestedFix)

            # assuming spaces aren't a part of the edit distance
            dist = dist - (end-start)
            if not distance == 0:
                results.append([dist, suggestedFix])

    results.sort()
    
    if results:
        return sentence.replace(results[0][1], typo, 1)
    else:
        return None


def estimateTypo(sentence, typo):
    ''' 
    estimateTypo -> corrected sentence
    
    Keyword arguments:
    sentence -- orginal sentence
    typo     -- the typo correction
    '''

    if len(typo.split()) > 1:
        return sentenceDist(sentence, typo)
    else:
        winner = [sys.maxint, None]

        for word in sentence.split():
            dist = distance(word, typo)
            if (0 < dist < winner[0]):
                winner = [dist, word]

        if winner[1]:
            return sentence.replace(winner[1], typo, 1)          
        else: 
            return None

def main(data):
    '''
    The communication and recentdata referances are injected
    by the moduleManager and defined by the require list of
    this class. The data object passed to this method
    is done by the core-parser (cparser) on privmsg and
    channel activities as definde by the listen list.
    '''

    nick = data['nick']
    ident = data['ident']
    host = data['host']
    channel = data['channel']
    message = data['msg']

    correct = False
    # Ensuring that the message to correct is long enough
    if (len(message) > 1):

        # Validating that the user is signaling that he/she did a typo
        if (message[0] == "*" and message[-1] != "*"):
            correct = message[1:]

        elif (message[-1] == "*" and message[0] != "*"):
            correct = message[:-1]

        if correct:
            # Using the injected recentdata object to get the previous
            # message the user typed
            user = recentdata.user(nick,ident,host)
            #lastmsg = user.data[-2]
            lastmsg = user.lastMsg()

            typo = estimateTypo(lastmsg['msg'],correct)
            if (typo):
                # Using the injected communication object to send messages
                # to the IRC server
                communication.say(channel,"%s meant: %s" % (nick,typo) )


