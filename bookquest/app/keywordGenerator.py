import spacy
from collections import Counter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from langdetect import detect


class KeywordGenerator:
    def __init__(self, language_model="fr_core_news_sm"):
        self.__nlp = spacy.load(language_model)
        self.__top_n = 10
        self.__use_mmr = True
        self.__diversity = 0.3
        self.__use_maxsum = True

        import nltk
        nltk.download('stopwords')

        self.__stopwords_french = set(stopwords.words('french'))
        self.__stopwords_english = set(stopwords.words('english'))

    def __get_stopwords(self, text):
        lang = detect(text)
        if lang == 'fr':
            print("frrrr")
            return self.__stopwords_french
        elif lang == 'en':
            print("ennnnnn")
            return self.__stopwords_english
        else:
            return set()

    def get_keyword(self, summary):
        try:
            stop_words = self.__get_stopwords(summary)
            doc = self.__nlp(summary)

            tokens = [token.lemma_ for token in doc if
                      not token.is_stop and
                      not token.is_punct and token.pos_ in
                      ["NOUN", "ADJ", "VERB"]]

            tokens = [token for token in tokens if
                      token.lower() not in stop_words]

            counter = Counter(tokens)
            candidates = [kw for kw, _ in
                          counter.most_common(self.__top_n * 2)]

            candidate_embeddings = np.array(
                [self.__nlp(kw).vector for kw in candidates])

            if self.__use_maxsum:
                return self.__max_sum_sim(candidates, candidate_embeddings,
                                          self.__top_n)

            if self.__use_mmr:
                return self.__mmr(candidates, candidate_embeddings,
                                  self.__top_n,
                                  self.__diversity)

            return candidates[:self.__top_n]

        except Exception as e:
            print(f"Keyword generation failed: {e}")
            return []

    def __max_sum_sim(self, candidates, candidate_embeddings, top_n):
        distances = cosine_similarity(candidate_embeddings,
                                      candidate_embeddings)

        min_distances = np.sum(distances, axis=1)
        candidate_indices = np.argsort(min_distances)[-2 * top_n:]

        selected_indices = []
        for _ in range(top_n):
            remaining = list(
                set(candidate_indices) - set(selected_indices))
            min_dist = np.inf
            best_index = None
            for idx in remaining:
                dist = sum([distances[idx][j] for j in selected_indices])
                if dist < min_dist:
                    best_index = idx
                    min_dist = dist
            selected_indices.append(best_index)

        return [candidates[i] for i in selected_indices]

    def __mmr(self, candidates, candidate_embeddings, top_n, diversity):
        doc_embedding = np.mean(candidate_embeddings, axis=0).reshape(1,
                                                                      -1)
        word_doc_similarity = cosine_similarity(candidate_embeddings,
                                                doc_embedding)

        word_similarity = cosine_similarity(candidate_embeddings)
        selected_keywords = [np.argmax(word_doc_similarity)]
        candidates_indices = [i for i in range(len(candidates))]

        for _ in range(top_n - 1):
            candidate_similarities = word_doc_similarity[
                candidates_indices]
            already_selected = word_similarity[selected_keywords, :]
            selected = np.argmax(
                (1 - diversity) * candidate_similarities -
                diversity * np.max(already_selected, axis=0)
            )
            selected_keywords.append(candidates_indices[selected])

        return [candidates[i] for i in selected_keywords]
