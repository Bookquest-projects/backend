from sqlalchemy import select


class BookshelfManager:
    def __init__(self):
        self.allowed_bookshelves = self.get_all_bookshelf_name()

    def is_bookshelf_name_allowed(self, name: str):
        print(self.allowed_bookshelves)
        print(name)
        print(f"Name is in list : {name in self.allowed_bookshelves}")
        return name in self.allowed_bookshelves

    def get_bookshelfid_by_name(self, name: str):
        from __init__ import session, Bookshelf

        query = select(Bookshelf.id_bookshelf).where(
            Bookshelf.name == name)
        result = session.execute(query)
        bookshelf_id = result.scalars().first()

        return bookshelf_id

    def get_all_bookshelf_name(self):
        from __init__ import session, Bookshelf

        # Get all bookshelf 's names
        names = session.query(Bookshelf.name).all()
        # Extract the names in a list
        bookshelf_names = [name[0] for name in names]
        return bookshelf_names