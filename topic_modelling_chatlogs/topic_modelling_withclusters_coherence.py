from gensim import corpora, models, similarities
from gensim.corpora import TextCorpus, MmCorpus
from itertools import chain
import csv
import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from collections import OrderedDict



# convert the document csv file in a documents per line, Each row read from the csv file is returned as a list of strings

X = open(r"/home/deeppixel/ecobee_analysis/Ecobee_analysis-master-629b83ff8fab52251c2e1a4eac38f57826107f44/upwork_chatlogs_sample.csv", encoding="utf-8-sig")


# compile documents
doc_complete = [] 
for line in X:
    doc_complete.append(line)

#Cleaning and Preprocessing in this step, we will remove the punctuations, stopwords and normalize the corpus.


stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete] 

list_of_tokens=[]
for line in X:
    list_of_tokens+=nltk.word_tokenize(line)




Max_Topics = 10


# Preparing Document-Term Matrix 
#it is a good practice to convert it into a matrix representation. 
#LDA model looks for repeating term patterns in the entire DT matrix. 
#Python provides many great libraries for text mining practices, “gensim” is one such clean and beautiful library to handle text data. 
#It is scalable, robust and efficient. Following code shows how to convert a corpus into a document-term matrix.


# Creating the term dictionary of our corpus, where every unique term is assigned an index.

dictionary = corpora.Dictionary(doc_clean)

# Create a bag of Word corpus
mm = [dictionary.doc2bow(text) for text in doc_clean]

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=Max_Topics, id2word = dictionary, passes=100)

#Results
#print(ldamodel.print_topics(num_topics=Max_Topics, num_words=3))
keywords = ldamodel.print_topics(num_topics=Max_Topics, num_words=3)


# Assigns the topics to the documents in corpus
lda_corpus = ldamodel[mm]

# Find the threshold, let's set the threshold to be 1/#clusters,
# To prove that the threshold is sane, we average the sum of all probabilities:
scores = list(chain(*[[score for topic_id,score in topic] \
                      for topic in [doc for doc in lda_corpus]]))
threshold = sum(scores)/len(scores)
#print(threshold)
#print

cluster = []

for k in range (Max_Topics):
    subcluster = [j for i,j in zip(lda_corpus,doc_complete) if len(i) > k and len(i[k]) > 0 and i[k][1] > threshold]
    cluster.append(subcluster)
    print(subcluster)
    
    for l in range (len(subcluster)):
        phrase = subcluster[l]
        if phrase.startswith("Agent") or phrase.startswith("Visitor"):
            phrase = re.sub('Visitor,chat.msg,', '', phrase)
            phrase = re.sub('Agent,chat.msg,', '', phrase)
            phrase = re.sub('["]', '', phrase)
            phrase = re.sub('\n', '', phrase) 
            keyw = str(keywords[k])
            keyw = re.sub('["]', '', keyw)
            print(str(k) + ',"' + str(keywords[k])+ '","' + phrase + '","' + phrase + '"')
				  
				  
					  
					
#time

# Now estimate the probabilities for the CoherenceModel.
# This performs a single pass over the reference corpus, accumulating
# the necessary statistics for all of the models at once.


trained_models = OrderedDict()
for num_topics in range(20, 101, 10):
    print("Training LDA(k=%d)" % num_topics)
    lda = models.LdaMulticore(
        mm, id2word=dictionary, num_topics=Max_Topics, workers=4,
        passes=10, iterations=100, random_state=42, eval_every=None,
        alpha='asymmetric',  # shown to be better than symmetric in most cases
        decay=0.5, offset=64  # best params from Hoffman paper
    )
    trained_models[num_topics] = lda
	
		 
cm = models.CoherenceModel.for_models(
    trained_models.values(), dictionary, texts=list_of_tokens, coherence='c_v')
		
			
		
#time
coherence_estimates = cm.compare_models(trained_models.values())
coherences = dict(zip(trained_models.keys(), coherence_estimates))

def print_coherence_rankings(coherences):
    avg_coherence = \
        [(num_topics, avg_coherence)
         for num_topics, (_, avg_coherence) in coherences.items()]
    ranked = sorted(avg_coherence, key=lambda tup: tup[1], reverse=True)
    print("Ranked by average '%s' coherence:\n" % cm.coherence)
    for item in ranked:
        print("num_topics=%d:\t%.4f" % item)
    print("\nBest: %d" % ranked[0][0])
print_coherence_rankings(coherences)
  
    			
