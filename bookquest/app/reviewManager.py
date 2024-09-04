from sqlalchemy import select, or_, and_


class ReviewManager:

    def get_userid_by_reviewid(self, review_id):
        from bookquest.app import session, Review
        user_id = session.query(Review).with_entities(
            Review.fk_user).filter_by(id_review=review_id).first()
        return user_id

    def get_reviewids_by_userid(self, user_id):
        from bookquest.app import session, Review
        review_id = session.query(Review).with_entities(
            Review.id_review).filter_by(fk_user=user_id)
        return review_id

    def get_bookshelfids_by_userid(self, user_id):
        from bookquest.app import session, Review
        bookshelf_id = session.query(Review).with_entities(
            Review.fk_bookshelf).filter_by(fk_user=user_id)
        return bookshelf_id

    def get_reviews_by_userid_and_bookshelfid(self,
                                              user_id,
                                              bookshelf_id):
        from bookquest.app import session, Review
        reviews = session.query(Review).filter_by(
            fk_user=user_id,
            fk_bookshelf=bookshelf_id)
        return reviews

    def get_isbns13_by_userid_and_bookshelfid(self,
                                             user_id,
                                             bookshelf_id):
        from bookquest.app import session, Review

        query = select(Review.isbn_13).where(and_(
            Review.fk_user == user_id,
            Review.fk_bookshelf == bookshelf_id))
        result = session.execute(query)
        isbns_13 = result.scalars().all()

        return isbns_13
