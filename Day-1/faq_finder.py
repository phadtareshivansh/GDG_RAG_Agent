"""
Intelligent FAQ Finder
"""

from typing import List, Dict
from text_cleaner import TextCleaner
from semantic_similarity import SemanticSimilarity


class FAQFinder:
    """Simple FAQ matching using token overlap and synonyms."""

    def __init__(self):
        self.cleaner = TextCleaner()
        self.similarity = SemanticSimilarity()
        self.faqs = []

        # stop words (common tokens to ignore)
        self.stop_words = {
            'a', 'an', 'the', 'is', 'are', 'am', 'be', 'to', 'of', 'in',
            'on', 'at', 'for', 'with', 'do', 'does', 'i', 'you', 'we',
            'they', 'there', 'can', 'will', 'it', 'what', 'how', 'when', 'where'
        }

        # basic synonyms mapping
        self.synonyms = {
            'sign': ['register', 'signup', 'join', 'enroll'],
            'register': ['sign', 'signup', 'join', 'enroll'],
            'signup': ['sign', 'register', 'join', 'enroll'],
            'pay': ['fee', 'cost', 'price', 'money', 'charge'],
            'fee': ['pay', 'cost', 'price', 'money', 'charge'],
            'cost': ['pay', 'fee', 'price', 'money', 'charge'],
            'start': ['schedule', 'time', 'begin', 'when'],
            'time': ['schedule', 'start', 'when'],
            'when': ['time', 'schedule', 'start'],
            'where': ['venue', 'location', 'place'],
            'venue': ['where', 'location', 'place'],
            'location': ['where', 'venue', 'place']
        }

        print("[OK] FAQ Finder initialized with smart matching!")

    def add_faq(self, question: str, answer: str):
        entry = {
            'question': question,
            'answer': answer,
            'question_clean': self.cleaner.clean_text(question)
        }
        self.faqs.append(entry)

    def load_from_file(self, filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line and '|' in line:
                        q, a = line.split('|', 1)
                        self.add_faq(q.strip(), a.strip())
            print(f"\u2705 Loaded {len(self.faqs)} FAQs from {filepath}")
        except FileNotFoundError:
            print(f"\u274c File not found: {filepath}")
        except Exception as e:
            print(f"\u274c Error loading file: {e}")

    def expand_with_synonyms(self, words: set) -> set:
        expanded = set(words)
        for word in list(words):
            if word in self.synonyms:
                expanded.update(self.synonyms[word])
        return expanded

    def find_answer(self, user_question: str, threshold: float = 0.15) -> Dict:
        if not self.faqs:
            return {
                'answer': "\u274c No FAQs loaded yet! Please add some FAQs first.",
                'confidence': 0.0,
                'matched_question': None
            }

        user_clean = self.cleaner.clean_text(user_question)
        user_words_raw = set(user_clean.split()) - self.stop_words
        user_words = self.expand_with_synonyms(user_words_raw)

        if not user_words:
            user_words = set(user_clean.split())

        best_match = None
        best_score = 0.0

        for faq in self.faqs:
            faq_words_raw = set(faq['question_clean'].split()) - self.stop_words
            faq_words = self.expand_with_synonyms(faq_words_raw)

            if not faq_words:
                faq_words = set(faq['question_clean'].split())

            intersection = user_words.intersection(faq_words)
            union = user_words.union(faq_words)

            if len(union) > 0:
                score = len(intersection) / len(union)
            else:
                score = 0.0

            if score > best_score:
                best_score = score
                best_match = faq

        if best_score < threshold:
            return {
                'answer': "I couldn't find a good answer to that question. Could you rephrase it?",
                'confidence': best_score,
                'matched_question': None
            }

        return {
            'answer': best_match['answer'],
            'confidence': best_score,
            'matched_question': best_match['question']
        }


if __name__ == "__main__":
    finder = FAQFinder()

    gdg_faqs = [
        {'question': "How do I register for the event?",
         'answer': "Visit our website at gdg.community.dev and click the 'Register' button on the event page."},
        {'question': "What is the event schedule?",
         'answer': "The workshop runs from 2:00 PM to 5:00 PM with lunch break in between."},
        {'question': "Where is the venue located?",
         'answer': "The event is at Tech Hub Innovation Center, 123 Innovation Street, Downtown."},
        {'question': "Is there a registration fee?",
         'answer': "No, all GDG events are completely free to attend!"},
    ]

    for faq in gdg_faqs:
        finder.add_faq(faq['question'], faq['answer'])

    queries = ["How can I sign up?", "Do I need to pay anything?", "Where is it happening?"]
    for q in queries:
        res = finder.find_answer(q)
        print(q, '->', res['matched_question'], res['confidence'])