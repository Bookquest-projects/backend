from sqlalchemy import select, and_


class ReviewManager:

    def get_first_review(self, params):
        """
            params (dict): A dictionary containing the fields to filter on.
            Accepted keys:
                - isbn_13 (str)
                - isbn_10 (str)
                - rating (int)
                - favorite (bool)
                - owned (bool)
                - reading_date (str)
                - reading_number (int)
                - comment (str)
                - fk_user (int)
                - fk_bookshelf (int)
            """
        from __init__ import session, Review

        # Build the filter based on the params provided
        filter_conditions = []
        for key, value in params.items():
            # Check that the attribut exist in the Review class
            if hasattr(Review, key):
                filter_conditions.append(getattr(Review, key) == value)

        # Apply the filter and get the review
        query = session.query(Review).filter(and_(*filter_conditions))
        review = query.first()
        return review

    def get_all_reviews(self, params):
        """
            params (dict): A dictionary containing the fields to filter on.
            Accepted keys:
                - isbn_13 (str)
                - isbn_10 (str)
                - rating (int)
                - favorite (bool)
                - owned (bool)
                - reading_date (str)
                - reading_number (int)
                - comment (str)
                - fk_user (int)
                - fk_bookshelf (int)
            """
        from __init__ import session, Review

        # Build the filter based on the params provided
        filter_conditions = []
        for key, value in params.items():
            # Check that the attribut exist in the Review class
            if hasattr(Review, key):
                filter_conditions.append(getattr(Review, key) == value)

        # Apply the filter and get the review
        query = session.query(Review).filter(and_(*filter_conditions))
        reviews = query.all()
        return reviews

    def insert_review(self, params):
        """
            params (dict): A dictionary containing the fields to filter on.
            Accepted keys:
                - isbn_13 (str)
                - isbn_10 (str)
                - rating (int)
                - favorite (bool)
                - owned (bool)
                - reading_date (str)
                - reading_number (int)
                - comment (str)
                - fk_user (int)
                - fk_bookshelf (int)
            """
        from __init__ import session, Review

        # Create a new Review instance with the provided parameters
        new_review = Review()
        for key, value in params.items():
            # Check that the attribute exists in the Review class
            if hasattr(new_review, key):
                setattr(new_review, key, value)

        # Add the new review to the session
        session.add(new_review)

        # Commit the transaction to save the review in the database
        session.commit()
        return new_review

    def update_review(self, review, params):
        """
            params (dict): A dictionary containing the fields to filter on.
            Accepted keys:
                - isbn_13 (str)
                - isbn_10 (str)
                - rating (int)
                - favorite (bool)
                - owned (bool)
                - reading_date (str)
                - reading_number (int)
                - comment (str)
                - fk_user (int)
                - fk_bookshelf (int)
            """
        from __init__ import session, Review
        for key, value in params.items():
            # Check that the attribut exist in the Review class
            if hasattr(Review, key):
                setattr(review, key, value)

        # Commit the transaction to save the review in the database
        session.commit()
        return True

    def get_userid_by_reviewid(self, review_id):
        from __init__ import session, Review
        user_id = session.query(Review).with_entities(
            Review.fk_user).filter_by(id_review=review_id).first()
        return user_id

    def get_reviewids_by_userid(self, user_id):
        from __init__ import session, Review
        review_id = session.query(Review).with_entities(
            Review.id_review).filter_by(fk_user=user_id)
        return review_id

    def get_bookshelfids_by_userid(self, user_id):
        from __init__ import session, Review
        bookshelf_id = session.query(Review).with_entities(
            Review.fk_bookshelf).filter_by(fk_user=user_id)
        return bookshelf_id

    def get_reviews_by_userid_and_bookshelfid(self,
                                              user_id,
                                              bookshelf_id):
        from __init__ import session, Review
        reviews = session.query(Review).filter_by(
            fk_user=user_id,
            fk_bookshelf=bookshelf_id)
        return reviews

    def get_isbns13_by_userid_and_bookshelfid(self,
                                              user_id,
                                              bookshelf_id):
        from __init__ import session, Review

        query = select(Review.isbn_13).where(and_(
            Review.fk_user == user_id,
            Review.fk_bookshelf == bookshelf_id))
        result = session.execute(query)
        isbns_13 = result.scalars().all()

        return isbns_13
