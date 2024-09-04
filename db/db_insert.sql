--
-- Insert for table [bookshelf]
--
INSERT INTO [bookshelf] ([name])
VALUES
    ('read'),
    ('reading'),
    ('to_be_read'),
    ('not_finished'),
    ('no_way');

--
-- Insert a test user
--
INSERT INTO [user] ([username], [password])
VALUES ('Admin', '$argon2id$v=19$m=65536,t=3,p=4$PaCybJopVsaeeospmU7aKQ$2w0pIvd+VPRWAEohwv/DWIZSy/KbsJLrD8Op9Bvl2q4');

--
-- Insert 2 test review
--
INSERT INTO [review] (
    [isbn_13],
    [isbn_10],
    [ratings],
    [favorite],
    [owned],
    [reading_date],
    [reading_number],
    [comment],
    [fk_user],
    [fk_bookshelf]
) VALUES
    ('9781234567897',     -- isbn_13
     '123456789X',        -- isbn_10
     5,                   -- ratings
     1,                   -- favorite
     1,                   -- owned
     '2024-09-03',        -- reading_date
     1,                   -- reading_number
     'Great book!',       -- comment
     1,                   -- fk_user
     1                    -- fk_bookshelf
    );
INSERT INTO [review] (
    [isbn_13],
    [isbn_10],
    [ratings],
    [favorite],
    [owned],
    [reading_date],
    [reading_number],
    [comment],
    [fk_user],
    [fk_bookshelf]
) VALUES
    ('9781234567897',     -- isbn_13
     '123456789X',        -- isbn_10
     5,                   -- ratings
     1,                   -- favorite
     1,                   -- owned
     '2024-09-03',        -- reading_date
     1,                   -- reading_number
     'Great book!',       -- comment
     1,                   -- fk_user
     2                    -- fk_bookshelf
    );