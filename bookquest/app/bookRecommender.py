from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import langid

from BookRepository import BookRepository


class BookRecommender:

    def __init__(self, isbn: str):
        self.target_isbn = isbn
        self.books_infos = []
        self.books_df = pd.DataFrame()

    def _prepare_features(self):
        self.books_df['combined_features'] = (
                self.books_df['title'] + " " +
                self.books_df['subtitle'] + " " +
                self.books_df['authors'].apply(
                    lambda x: ' '.join(x)) + " " +
                self.books_df['categories'].apply(
                    lambda x: ' '.join(x)) + " " +
                self.books_df['description']
        )

    def _get_similar_books_indices(self, lang='english',
                                   num_recommendations=7):

        if self.books_df.empty:
            raise ValueError(
                "Book data is not loaded. Call fetch_books() first.")

        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(stop_words=lang)
        tfidf_matrix = tfidf.fit_transform(
            self.books_df['combined_features'])

        # Cosine Similarity
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        # Get the index of the book that matches the target ISBN
        try:
            idx = self.books_df.index[
                (self.books_df['isbn_10'] == self.target_isbn) |
                (self.books_df['isbn_13'] == self.target_isbn)
                ].tolist()[0]
        except IndexError:
            raise ValueError(
                f"Book with ISBN '{self.target_isbn}' not found in the fetched data.")

        # Get similarity scores for all books
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the indices of the most similar books
        sim_scores = sim_scores[
                     1:num_recommendations + 1]  # Exclude the first entry as it's the same book
        book_indices = [i[0] for i in sim_scores]

        return book_indices

    def generate_recommendations(self):
        # Fetch the target book
        book_repository = BookRepository()
        target_book = book_repository.findBookByIsbn(self.target_isbn)
        target_category = target_book.get("categories")[0]
        target_language = target_book.get("languages")

        if not target_category:
            return None

        # Try to detect the lang if none is returned by the API
        if not target_language and target_book.get("description"):
            detected_language = langid.classify(
                target_book.get("description"))
            target_language = detected_language[0]

        # TODO : Remove already read books ?

        # Fetch books from the same category and language
        self.books_infos = book_repository.find_books_by_keyword_and_lang(
            target_category, target_language, 1000)
        if not self.books_infos or len(self.books_infos) == 0:
            return None

        # Regroup all datas in the dataframe
        books_data = self.books_infos
        books_data.append(target_book)
        self.books_df = pd.DataFrame(books_data)

        # Extract features for similarity analysis
        self._prepare_features()

        # Search for the most similar books in the selection
        try:
            indices = self._get_similar_books_indices()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        # Retrieve the book info from the selected indices
        recommended_books = self.books_df.iloc[indices]
        recommended_books_info = recommended_books.to_dict('records')

        return recommended_books_info
