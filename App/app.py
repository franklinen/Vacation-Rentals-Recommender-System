# Core Pkg
import streamlit as st 
import streamlit.components.v1 as stc 
# Load EDA
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel
from sklearn.decomposition import LatentDirichletAllocation
import re


st.write("# Rental Recommendation Engine")

message_text = st.text_input("Enter a rental")

pd.options.display.max_columns = 30
df = pd.read_csv('X.csv', encoding="latin-1", na_values='')
df.head()
print('We have ', len(df), 'rentals in the data')


df['Reviews']= df['Reviews'].astype(str)
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = re.sub('<[^>]*>', '', text) # Effectively removes HTML markup tags
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing. 
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwors from text
    return text
    
df['reviews_clean'] = df['Reviews'].apply(clean_text)

df.set_index('Title', inplace = True)
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df['reviews_clean'])
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df.index)

def recommendations(Title, cosine_similarities = cosine_similarities):
    
    recommended_rentals = []
    
    # getting the index of the hotel that matches the name
    idx = indices[indices == Title].index[0]

    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending = False)

    # getting the indexes of the 10 most similar hotels except itself
    top_10_indexes = list(score_series.iloc[1:11].index)
    
    # populating the list with the names of the top 10 matching hotels
    for i in top_10_indexes:
        recommended_rentals.append(list(df.index)[i])
        
    return recommended_rentals


if message_text != '':

	result = recommendations(message_text)

	st.write(result)













