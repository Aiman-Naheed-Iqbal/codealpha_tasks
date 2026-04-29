import json
from src.preprocess import clean_text
from src.similarity import SimilarityModel

class ChatBot:
    def __init__(self, faq_path="data/faqs.json"):
        with open(faq_path, "r") as f:
            self.data = json.load(f)

        self.questions = [clean_text(item["question"]) for item in self.data]
        self.answers = [item["answer"] for item in self.data]

        self.model = SimilarityModel()
        self.model.fit(self.questions)

    def get_response(self, user_input):
        user_input = clean_text(user_input)
        index, score = self.model.get_best_match(user_input)

        if score < 0.3:
            return "Sorry, I don't understand that. Can you rephrase?"
        return self.answers[index]