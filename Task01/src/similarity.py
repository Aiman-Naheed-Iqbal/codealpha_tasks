from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit(self, corpus):
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def get_best_match(self, query):
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix)
        index = scores.argmax()
        return index, scores[0][index]