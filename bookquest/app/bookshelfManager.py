from sqlalchemy import select


class BookshelfManager:

    # def get_bookshelf_by_id(self, bookshelf_id):
    #     query = "SELECT * FROM bookshelf WHERE id_bookshelf = %s"
    #     result = self.db_manager.execute_select(query, (bookshelf_id,))
    #     return result

    def get_bookshelfid_by_name(self, name: str):
        from __init__ import session, Bookshelf

        query = select(Bookshelf.id_bookshelf).where(
            Bookshelf.name == name)
        result = session.execute(query)
        bookshelf_id = result.scalars().first()

        return bookshelf_id
    
    def get_all_bookshelf_name(self):
        from __init__ import session, Bookshelf

        query = select(Bookshelf.name)
        result = session.execute(query)
        bookshelf_names = result.scalars().all()

        return bookshelf_names
