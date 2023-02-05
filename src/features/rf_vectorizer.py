import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import StandardScaler
from scipy.sparse import vstack, hstack, csr_matrix
import numpy as np
import pickle
from nltk import everygrams
from sklearn.utils import shuffle
import sys
import os

with open (".\\data\\processed\\rfdata.csv", "r", encoding = "utf-8") as file0:
    df = pd.DataFrame(pd.read_csv(file0, keep_default_na=False))

vectorizer = CountVectorizer(ngram_range=(2, 4),
                            analyzer='char',
                            stop_words=None)

ngram_features = vectorizer.fit_transform(df['words'])


vowel_feature = csr_matrix(np.array(df["vowel rt"]).reshape(-1,1))
consonant_feature = csr_matrix(np.array(df["consonant rt"]).reshape(-1,1))
ttr_feature = csr_matrix(np.array(df["ttr"]).reshape(-1,1))

lexical_features = hstack((vowel_feature, consonant_feature, ttr_feature))
features = hstack((lexical_features, ngram_features))

scaler = StandardScaler(with_mean=False)
features = scaler.fit_transform(np.abs(features))

#Exportação dos dados vetorizados como um pickle
with open('.\\data\\processed\\rf_vectfeatures.pkl', 'wb') as file:  
    pickle.dump(features, file)

#Exportação do vetorizador
with open('.\\models\\randomforest_count_vectorizer.pkl', 'wb') as file1:  
    pickle.dump(vectorizer, file1)