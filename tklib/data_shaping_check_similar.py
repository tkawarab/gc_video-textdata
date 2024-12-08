# -*- coding: utf-8 -*-
import numpy as np
 
#わかち書き関数
def wakachi(text):
    from janome.tokenizer import Tokenizer
    t = Tokenizer()
    tokens = t.tokenize(text)
    docs=[]
    for token in tokens:
        docs.append(token.surface)
    return docs
 
#文書ベクトル化関数
def vecs_array(documents):
    from sklearn.feature_extraction.text import TfidfVectorizer
 
    docs = np.array(documents).astype('str')
    vectorizer = TfidfVectorizer(analyzer=wakachi,binary=True,use_idf=False)
    vecs = vectorizer.fit_transform(docs)
    return vecs.toarray()

def check_similar(array_data):
    from sklearn.metrics.pairwise import cosine_similarity
    #類似度行列作成
    cs_array = np.round(cosine_similarity(vecs_array(array_data), vecs_array(array_data)),3) 
    return cs_array
if __name__ == '__main__':  
    docs = [
    "今日は曇りです。",
    "今日は、2階のパントリーだけでなく、"]
    ret = check_similar(docs)
    print(ret)