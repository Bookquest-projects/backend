class ReviewManager:

    def __init__(self):

    def get_userid_by_reviewid(self, review_id):
        query = "SELECT fk_user FROM review WHERE id_review = %s"
        result = self.db_manager.execute_select(query, (review_id,))
        return result

    def get_reviewids_by_userid(self, user_id):
        query = "SELECT id_review FROM review WHERE fk_user = %s"
        result = self.db_manager.execute_select(query, (user_id,))
        return result

    def get_bookshelfids_by_userid(self, user_id):
        query = "SELECT fk_bookshelf FROM review WHERE fk_user = %s"
        result = self.db_manager.execute_select(query, (user_id,))
        return result

    def get_review_by_userid_and_bookshelfid(self,
                                             user_id,
                                             bookshelf_id):
        query = "SELECT * FROM review WHERE fk_user = %s AND fk_bookshelf = %s"
        result = self.db_manager.execute_select(query,
                                                (user_id, bookshelf_id,))
        return result

    def get_isbn13_by_userid_and_bookshelfid(self,
                                             user_id,
                                             bookshelf_id):
        query = "SELECT isbn_13 FROM review WHERE fk_user = %s AND fk_bookshelf = %s"
        result = self.db_manager.execute_select(query,
                                                (user_id, bookshelf_id,))
        return result
