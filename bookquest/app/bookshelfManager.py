class BookshelfManager:

    def __init__(self):

    def get_bookshelf_by_id(self, bookshelf_id):
        query = "SELECT * FROM bookshelf WHERE id_bookshelf = %s"
        result = self.db_manager.execute_select(query, (bookshelf_id,))
        return result

    def get_bookshelfid_by_name(self, name):
        query = "SELECT id_bookshelf FROM bookshelf WHERE name = %s"
        result = self.db_manager.execute_select(query, (name,))
        return result

    def get_all_bookshelf_name(self):
        query = "SELECT name FROM bookshelf"
        result = self.db_manager.execute_select(query)
        return result
