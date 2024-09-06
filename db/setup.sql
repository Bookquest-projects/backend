--
-- Table structure for table [bookshelf]
--
DROP TABLE IF EXISTS [bookshelf];
CREATE TABLE [bookshelf]
(
    [
    id_bookshelf]
    INT
    NOT
    NULL
    IDENTITY
(
    1,
    1
),
    [name] NVARCHAR
(
    45
) NOT NULL,
    PRIMARY KEY
(
[
    id_bookshelf]
),
    UNIQUE
(
[
    name]
)
    );


--
-- Table structure for table [user]
--
DROP TABLE IF EXISTS [user];
CREATE TABLE [user]
(
    [
    id_user]
    INT
    NOT
    NULL
    IDENTITY
(
    1,
    1
),
    [username] NVARCHAR
(
    45
) NOT NULL,
    [password] NVARCHAR
(
    255
) NOT NULL,
    PRIMARY KEY
(
[
    id_user]
),
    UNIQUE
(
[
    username]
)
    );


--
-- Table structure for table [review]
--
DROP TABLE IF EXISTS [review];
CREATE TABLE [review]
(
    [
    id_review]
    INT
    NOT
    NULL
    IDENTITY
(
    1,
    1
),
    [isbn_13] NVARCHAR
(
    13
) NULL,
    [isbn_10] NVARCHAR
(
    10
) NULL,
    [ratings] TINYINT NULL,
    [favorite] BIT NULL,
    [owned] BIT NULL,
    [reading_date] DATE NULL,
    [reading_number] TINYINT DEFAULT 0,
    [comment] TEXT,
    [fk_user] INT NULL,
    [fk_bookshelf] INT NULL,
    PRIMARY KEY
(
[
    id_review]
),
    FOREIGN KEY
(
[
    fk_user]
) REFERENCES [user]
(
[
    id_user]
),
    FOREIGN KEY
(
[
    fk_bookshelf]
) REFERENCES [bookshelf]
(
[
    id_bookshelf]
)
    );

--
-- Insert for table [bookshelf]
--
INSERT INTO [bookshelf] ([name])
VALUES ('read'), ('reading'), ('to_be_read'), ('not_finished'), ('no_way');

--
-- Insert a test user
--
INSERT INTO [user] ([username], [password])
VALUES ('Admin', '$argon2id$v=19$m=65536,t=3,p=4$PaCybJopVsaeeospmU7aKQ$2w0pIvd+VPRWAEohwv/DWIZSy/KbsJLrD8Op9Bvl2q4');

--
-- Insert 2 test review
--
INSERT INTO [review] ([isbn_13],
    [isbn_10],
    [ratings],
    [favorite],
    [owned],
    [reading_date],
    [reading_number],
    [comment],
    [fk_user],
[fk_bookshelf])
VALUES ('9781234567897', -- isbn_13
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
