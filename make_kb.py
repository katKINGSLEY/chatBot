"""
    Name:   Kathryn Kingsley and Jonathan Yu
    UTID:   KLK170230 and JCY180000
    Class:  NLP CS4395.001
    Date:   Fall 2022
    Desc.:  This is the main .py file for the chatBot pair assignment. It creates the knowledge base
            using Doctor Mazidi's textbook for NLP.

"""
import pathlib  # to read the input file
from nltk import sent_tokenize  # needed in clean_text
import yake  # for key word identification
from nltk.corpus import stopwords  # to eliminate not functional words
import pickle  # for picklin'


def get_text(file):
    with open(file, 'r') as file:
        # remove new lines
        raw_text = file.read().replace('\n', '')
    # close the file
    file.close()
    return raw_text


def get_sentences(text):
    sentences = sent_tokenize(text, 'english')
    sentences = [sent for sent in sentences if not sent.__contains__('....') and not sent.__contains__('. . . .')
                 and not sent.__contains__('https://')]
    return sentences


def get_keywords(text):
    stop_words = stopwords.words('english')
    extractor = yake.KeywordExtractor(top=500, stopwords=stop_words)  # change number of keywords HERE!
    keywords = extractor.extract_keywords(text)
    # print(len(keywords))
    keywords = [kw for kw, v in keywords]  # get only the word
    return keywords


def make_dictionary(kw, sents):
    kw_dict = {}
    sentences = []
    for word in kw:
        sentences = [sent for sent in sents if word in sent]
        kw_dict[word] = sentences
        sentences = []  # reset sentences
    # print(kw_dict)
    return kw_dict


def pickle_it(dic):
    filename = 'nlp_dict.p'
    outfile = open(filename, 'wb')
    pickle.dump(dic, outfile)
    outfile.close()


def main():
    filepath = pathlib.Path.cwd().joinpath('nlpbook.txt')
    if not filepath:
        print("Issue with opening file. Exiting program...")
        exit(1)
    text = get_text(filepath).lower()
    sentences = get_sentences(text)
    key_words = get_keywords(text)
    kw_dict = make_dictionary(key_words, sentences)
    pickle_it(kw_dict)


if __name__ == '__main__':
    main()
