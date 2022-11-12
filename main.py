#import nltk
#import spacy
import random
from screen import Screen

class ChatBot:
    def __init__(self, name):
        self.name = name


    def say(self, msg):
        if isinstance(msg, str):
            lines = msg.split("\n")
        else:
            lines = msg
        sep = ''
        print(f"{self.name}: ", end='')
        for line in lines:
            print(sep + line)
            sep = ' ' * (len(self.name)+2)

    def start(self):
        nlp = spacy.load('en_core_web_md')

        done = False
        while not done:
            user_in = input("> ")

            # Process input
            doc = nlp(user_in)
            for token in doc:
                print('\t',token,token.lemma_, token.pos_, token.is_alpha, token.is_stop)
                if token.lemma_ == 'be':
                    print("BEBEBE")

            # Determine response
            response = random.choice(["Loser", "Find some tokens", "Buttlicker"])
            
            # Say it 
            done = True
if __name__ == "__main__":
    '''
    print(screen.logo)
    print("Please note that this conversation may be recorded for quality assurance.")
    print("\n\n")
    NLPete = ChatBot("NLPete")
    intro = ["Hi! I'm NLPete, your comprehensive guide on natural language processing!",
             "How can I help you today?"]
    NLPete.say(intro)'''
    Screen().start()
