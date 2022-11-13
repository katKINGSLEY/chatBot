import PyPDF2
import pickle
import spacy
import re
from nltk import sent_tokenize
from nltk.corpus import stopwords

blacklist = [". . . . . . . ", "Section", "Chapter", "http:", "https"]
stop_words = stopwords.words("english")

def filter(sent):
	sent = " ".join(sent)
	for b in blacklist:
		if b in sent:
			return False
	try:
		str(sent)
	except:
		print("Clip bytes")
		return False
	return ((len(sent) > 200 and len(sent) > 20)
	   	and (sent.count(".") > 15))


if __name__ == "__main__":
	nlp = spacy.load("en_core_web_md")
	pdf_file = open("MazidiBook.pdf", "rb")
	pdf_reader = PyPDF2.PdfFileReader(pdf_file)

	# content is on pages [13,263]
	start_page = 13
	end_page = 263
	pages = [p for p in range(start_page, end_page+1)]

	# Ignore the index pages
	page_blacklist = [15,55,99,131,173,231,261]
	text = ""
	for i in [p for p in pages if p not in page_blacklist]:
		page = pdf_reader.getPage(i)
		text += " " + page.extractText().encode('utf-8').decode('ascii', 'ignore')
	pdf_file.close()


	kb = {}
	kb["words"] = {}
	for word in text.split():
		if word.isalpha() and word not in stop_words:
			kb["words"][word] = True

	text = ' '.join(text.split())
	text = text.replace("*** Draft copy of NLP with Python by Karen Mazidi: Do not distribute ***", "")	
	sents = sent_tokenize(text)
	kb["lookup"] = []
	for i in range(1,len(sents)):
		s0 = sents[i-1]
		#s1 = sents[i]
		if not filter(s0):# and not filter(s1):
			kb["lookup"].append(s0)#(s0, s1))
	print(kb)
	open("out.txt","w").write("\n".join([f"<{k}" for k in kb["lookup"]]))
	pickle_file = open("mazidi_book_kb.p", "wb")
	pickle.dump(kb, pickle_file)
	pickle_file.close()
