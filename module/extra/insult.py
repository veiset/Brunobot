'''
Insult module!
'''

''' Required for Brunobot module'''
version = '0.1'
name    = 'insult'
author  = 'Vegard Veiset' # optional
require = ['communication']
listen  = ['cmd']
cmd     = ['insult']
usage   = "insult <nick>"
description = "Shouts a random insult to a person."

insults = ['Don\'t get lost in thought; you\'ll be a total stranger there.',
'You\'re good looking in a way, away off.',
'The more I think of you, the less I think of you.',
'When you were born something terrible happened, you lived.',
'You look like a professional blind date.',
'Don\'t you ever get tired of having you around?',
'I don\'t know what makes you tick, but I hope it\'s a time bomb.',
'Someday you\'ll find yourself, and will you be disappointed.',
'I know you have to be somebody, but why do you have to be you?',
'If you said what you thought, you\'d be speechless.',
'You think you\'re a wit, and you\'re probably half right.',
'Why don\'t you go blow your brains out, you\'ve got nothing to lose.',
'I like you, I have no taste, but I like you.',
'I\'d like to say I\'m glad you\'re here; I\'d like to say it.',
'If there\'s ever a price on your head, take it.',
'You were born at home, but when your mother saw you she went to the hospital.',
'Someday you\'ll go far, and I hope you stay there.',
'If you stop telling lies about me, I\'ll stop telling the truth about you.',
'I wish I had a lower I.Q., so that I could enjoy your company.',
'I\'m not going to get into a battle of wits with you; I never attack anyone who\'s unarmed.',
'Is your family happy, or do you go home at night?',
'You\'re someone who would make a perfect stranger.',
'Let\'s go some place were we can each be alone.',
'My I have the pleasure of you absence?',
'You have an open mind, and a mouth to match.',
'Next time you give your clothes away, stay in them.',
'Some people bring happiness wherever they go; you bring happiness whenever you go.',
'I like you better the more I see you less.',
'You\'re something that someone would only meet in a nightmare.',
'I wish your parents had never met.',
'The sooner I never see you again, the better it\'ll be for both of us when we meet.',
'You have such a big mouth; you could eat a banana sideways.',
'There\'s only one thing that keeps me from breaking you in half, I don\'t want two of you around.',
'Was the ground cold when you crawled out this morning?',
'Why don\'t you freeze your teeth and give your tongue a sleigh ride.',
'You\'ve got a great personality, but not for a human being.',
'I enjoy talking to you, my mind needs a rest.',
'If you ever need a friend, you\'ll have to get a dog.',
'You\'re outspoken, but not by anyone I know.',
'There\'s enough people in this world who hate you, without you working so hard to get another one.',
'Thank you; we\'re all challenged by your unique point of view.',
'I don\'t know what your problem is, but I\'ll bet it\'s hard to pronounce.',
'Any connection between your reality and mine is purely coincidental.',
'I will always cherish the initial misconception I had about you.',
'How about never? Is never good for you?',
'I\'ll try being nicer if you\'ll try being smarter.',
'I see you\'ve set aside this special time to humiliate yourself in public.',
'I don\'t know what makes you so screwed up, but whatever it is, it works.',
'You do serve at least one useful purpose in life, as a horrible example.',
'You\'ve got more talent in your little finger than you have in your big finger.',
'I\'m busy now; can I ignore you some other time?',
'Are you always this stupid, or are you making a special effort today?',
'Me, getting smart with you? How would you know?',
'It\'s too bad stupidity isn\'t painful.',
'Don\'t say things like that; it just makes you sound stupid. In fact, don\'t talk at all. It just makes you sound stupid.',
'Thinking isn\'t your strong point, is it?',
'I would probably find you more interesting had I studied psychology.',
'You\'re not being sensitive, I really don\'t like you.',
'You\'re good, being gone.',
'If I\'ve said anything to offend you, I mean it.',
'I would love to insult you, but you wouldn\'t understand.',
'Is there no beginning to your good taste?',
'One good thing about you, you\'re easy to ignore.',
'Why do you get up in the morning?',
'You\'re a person of rare intelligence; it\'s rare when you show any.',
'Hey, I\'m sorry, I\'m not being rude; it\'s just that you don\'t matter.',
'I\'d explain it to you, but I don\'t have any crayons with me.',
'I wish we were better strangers.',
'Why do you have to be that way, you seemed normal until I got to know you?',
'Do you want me to accept you as you are, or do you want me to like you?',
'You are no longer beneath my contempt.',
'Are you a moron, or are you possessed by a retarded ghost?',
'I can please only one person per day. Today is not your day. Tomorrow isn\'t looking good either.',
'So tell me, as an outsider, what do you think of the human race?',
'I notice that you never let an idea interrupt the flow of your conversation.',
'Don\'t try so hard, I couldn\'t like you any less.',
'You\'re having delusions of competence.']

import random

def main(data):
    channel = data['channel']
    argv    = data['argv']

    if argv:
        communication.say(channel,'%s: %s' % (argv[0], insults[random.randint(0,len(insults)-1)] ))

