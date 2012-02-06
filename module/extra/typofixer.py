import sys
''' Required for Brunobot module'''
version = '3.2'
name    = 'typofixer'
author  = 'Vegard Veiset' # optional
url     = 'http://veiset.org/svn/bruno/module/typo.py' # optional
require = ['communication','recentdata']
listen  = ['channel','privmsg']

def distance(word1, word2):
    # Memeory optimization
    if len(word1) < len(word2): 
        return distance(word2, word1)
    if not word1:
        return len(word2)
 
    row = range(len(word2) + 1)
    for i, c1 in enumerate(word1):
        current = [i + 1]

        for j, c2 in enumerate(word2):
            # find the min cost of deletion, insertion and substitution
            current.append(min(row[j+1]+1, current[j]+1, row[j]+(c1 != c2)))

        row = current
 
    return row[-1]
           
def estimateTypo(sentence,typo):
    winner = [sys.maxint,None]

    for word in sentence.split():
        dist = distance(word,typo)
        if (0 < dist < winner[0]):
            winner = [dist,word]

    return winner[1]

def fixTypo(sentence,typo,match):
    if (match == None): return sentence
    else: return sentence.replace(match,typo,1)

def correctMe(sentence,typo):
    return fixTypo(sentence,typo,estimateTypo(sentence,typo))

def main(data):
    '''
    The communication and recentdata referances are injected
    by the moduleManager and defined by the require list of
    this class. The data object passed to this method
    is done by the core-parser (cparser) on privmsg and
    channel activities as definde by the listen list.
    '''
    nick = data[0]
    ident = data[1]
    host = data[2]
    channel = data[3]
    message = data[4]

    correct = False
    # Ensuring that the message to correct is long enough
    if (len(message) > 1):

        # Validating that the user is signaling that he/she did a typo
        if (message[0] == "*" and message[-1] != "*"):
            correct = message[1:]

        elif (message[0] == "*" and message[-1] != "*"):
            correct = message[:-1]

        if correct:
            # Using the injected recentdata object to get the previous
            # message the user typed
            user = recentdata.user(nick,ident,host)
            lastmsg = user.lastMsg()

            typo = correctMe(lastmsg['msg'],correct)
            if (typo):
                # Using the injected communication object to send messages
                # to the IRC server
                communication.say(channel,"%s meant: %s" % (nick,typo) )


