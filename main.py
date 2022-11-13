import config as cfg
import pickle
import random
import spacy
import time

from nltk.corpus import stopwords
from screen import Screen

stop_words = stopwords.words("english")
nlp = spacy.load('en_core_web_md')
kb = pickle.load(open("mazidi_book_kb.p", "rb"))
choose = lambda arr: random.choice(arr)

def find_occurrence(list, text):
    for word in list:
        if word in text:
            return True
    return False

def prep(doc):
    return set([t.text 
                for t in doc 
                if t.text.isalpha() 
                and kb["words"].get(t.text)]) # filters stop words as well

#TODO: instead of this proportion, try something else
def similarity(doc1, doc2):
    t1 = prep(doc1)
    t2 = prep(doc2)
    # Union the sets. If they're very similar, this will reduce the size of t12,
    # which then increases the returned similarity.
    t12 = t1 | t2
    if len(t12) == 0:
        return 0
    else:
        return len(t1.intersection(t2))/len(t12)

class ChatBot:
    def __init__(self, name):        
        self.name = name       
        self.user_name = ""
        self.name_response_idx = 0
        self.confused_response_idx = 0
        self.screen = Screen()
        self.likes_list = []
        self.dislikes_list = []

    def respond(self, user_input):
        doc = nlp(user_input)
        
        response = None
        if new_name := self.find_name(doc):
            response = cfg.NAME_RESPONSES[self.name_response_idx].format(
                name=self.user_name,
                new_name=new_name
                )
            self.update_name(new_name)
        elif word := self.find_like(doc):

            changed = self.add_like(word)
            if changed:
                response = choose(cfg.LIKE_CHANGE).format(word=word)
            else:
                response = choose(cfg.LIKE_RESPONSES).format(word=word)
        elif word := self.find_dislike(doc):
            changed = self.add_dislike(word)
            if changed:
                response = choose(cfg.DISLIKE_CHANGE).format(word=word)
            else:
                response = choose(cfg.DISLIKE_RESPONSES).format(word=word)
        else:
            if self.likes(user_input):
                response = choose(cfg.LIKE_PREPENDS).format(word=word)
            elif self.dislikes(user_input):
                response = choose(cfg.DISLIKE_PREPENDS).format(word=word)
            if len(prep(doc)) > 0:
                matches = []
                for i, entry in cfg.index(kb["lookup"]):
                    s1 = nlp(entry[0])
                    sim = similarity(doc,s1)
                    if sim >= cfg.MIN_SIM:
                        matches.append(i)
                if len(matches) > 0:
                    response = str(len(matches))+kb["lookup"][choose(matches)]
        if response is None:
            response = choose(cfg.CONFUSED)
            self.confused_response_idx = (self.confused_response_idx + 1) % len(cfg.CONFUSED)
        self.chat(response)

  
    def likes(self, user_input):
        for word in self.likes_list:
            if word in user_input:
                return True
        return False

    def dislikes(self, user_input):
        for word in self.dislikes_list:
            if word in user_input:
                return True
        return False

    def find_like(self, doc):
        like = None
        if idx := find_occurrence(cfg.LIKE_VERBS, doc.text):
            for token in doc:
                if ("dobj" in token.dep_):
                    like = token.text
            print(f"Likes {like}")
        return like

    def find_dislike(self, doc):
        word = None
        if idx := find_occurrence(cfg.DISLIKE_VERBS, doc.text):
            for token in doc:
                if ("dobj" in token.dep_):
                    word = token.text
        return word

    def find_name(self, doc):
        name = None
        if find_occurrence(cfg.NAME_VERBS, doc.text):
            for token in doc:
                print
                if token.pos_ == "PROPN":
                    name = token.text
        return name

    def add_like(self, word):
        self.likes_list.append(word)
        if word in self.dislikes_list:
            self.dislikes_list.remove(word)
            return True
        else:
            return False
       

    def update_name(self, new_name):
        self.screen.user_name = new_name
        # Progress name shtick
        if self.name_response_idx < len(cfg.NAME_RESPONSES)-1:
            self.name_response_idx += 1


    def chat(self, msg):
        # Make it look like he's thinking
        time.sleep(random.uniform(0.5, 1.5))
        self.screen.add_chat(self.name, msg)


    def run(self):
        self.screen.update()
        self.chat("Hi! I'm NLPete, your comprehensive guide on natural language processing! How can I help you today?")
        self.screen.update()
        while True:
            self.screen.update()
            res = self.screen.step()
            self.screen.update()
            if res == "break":
                break
            elif res is not None:
                # Otherwise it returned
                self.screen.update(True)
                self.respond(res)
                #break

if __name__ == "__main__":
    chatbot = ChatBot("NLPete")
    chatbot.run()