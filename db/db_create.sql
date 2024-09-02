-- 
-- Delete existing tables
--
DROP TABLE IF EXISTS [author_work];
DROP TABLE IF EXISTS [review];
DROP TABLE IF EXISTS [book];
DROP TABLE IF EXISTS [work];
DROP TABLE IF EXISTS [user];
DROP TABLE IF EXISTS [author];
DROP TABLE IF EXISTS [serie];
DROP TABLE IF EXISTS [publisher];
DROP TABLE IF EXISTS [bookshelf];

--
-- Table structure for table [author]
--
CREATE TABLE [author] (
    [id_author] INT NOT NULL IDENTITY(1,1),
    [name] NVARCHAR(100) NOT NULL,
    [description] TEXT,
    PRIMARY KEY ([id_author]),
    UNIQUE ([name])
);

--
-- Table structure for table [bookshelf]
--
CREATE TABLE [bookshelf] (
    [id_bookshelf] INT NOT NULL IDENTITY(1,1),
    [name] NVARCHAR(45) NOT NULL,
    PRIMARY KEY ([id_bookshelf]),
    UNIQUE ([name])
);

--
-- Table structure for table [publisher]
--
CREATE TABLE [publisher] (
    [id_publisher] INT NOT NULL IDENTITY(1,1),
    [name] NVARCHAR(100) NOT NULL,
    [previous_id] INT DEFAULT 0,
    PRIMARY KEY ([id_publisher]),
    UNIQUE ([previous_id])
);

--
-- Table structure for table [serie]
--
CREATE TABLE [serie] (
    [id_serie] INT NOT NULL IDENTITY(1,1),
    [original_name] NVARCHAR(100) NOT NULL,
    PRIMARY KEY ([id_serie])
);

--
-- Table structure for table [user]
--
CREATE TABLE [user] (
    [id_user] INT NOT NULL IDENTITY(1,1),
    [username] NVARCHAR(45) NOT NULL,
    [email] NVARCHAR(100) NOT NULL,
    [password] NVARCHAR(45) NOT NULL,
    PRIMARY KEY ([id_user]),
    UNIQUE ([email])
);

--
-- Table structure for table [work]
--
CREATE TABLE [work] (
    [id_work] INT NOT NULL IDENTITY(1,1),
    [original_title] NVARCHAR(100) NOT NULL,
    [fk_serie] INT NULL,
    PRIMARY KEY ([id_work]),
    FOREIGN KEY ([fk_serie]) REFERENCES [serie] ([id_serie])
);

--
-- Table structure for table [book]
--
CREATE TABLE [book] (
    [id_book] INT NOT NULL IDENTITY(1,1),
    [ISBN_10] CHAR(10) DEFAULT '',
    [ISBN_13] CHAR(13) DEFAULT '',
    [title] NVARCHAR(100) NOT NULL,
    [lang] CHAR(3) NOT NULL,
    [page_count] SMALLINT NOT NULL,
    [volume_number] TINYINT NULL,
    [publication_date] DATE NULL,
    [summary] TEXT,
    [fk_publisher] INT NULL,
    [fk_work] INT NULL,
    PRIMARY KEY ([id_book]),
    UNIQUE ([ISBN_10]),
    UNIQUE ([ISBN_13]),
    FOREIGN KEY ([fk_publisher]) REFERENCES [publisher] ([id_publisher]),
    FOREIGN KEY ([fk_work]) REFERENCES [work] ([id_work])
);

--
-- Table structure for table [review]
--
CREATE TABLE [review] (
    [id_review] INT NOT NULL IDENTITY(1,1),
    [ratings] TINYINT NULL,
    [favorite] BIT NULL,
    [owned] BIT NULL,
    [reading_date] DATE NULL,
    [reading_number] TINYINT DEFAULT 0,
    [comment] TEXT,
    [fk_user] INT NULL,
    [fk_book] INT NULL,
    [fk_bookshelf] INT NULL,
    PRIMARY KEY ([id_review]),
    FOREIGN KEY ([fk_user]) REFERENCES [user] ([id_user]),
    FOREIGN KEY ([fk_book]) REFERENCES [book] ([id_book]),
    FOREIGN KEY ([fk_bookshelf]) REFERENCES [bookshelf] ([id_bookshelf])
);

--
-- Table structure for table [author_work]
--
CREATE TABLE [author_work] (
    [fk_author] INT NOT NULL,
    [fk_work] INT NOT NULL,
    PRIMARY KEY ([fk_work], [fk_author]),
    FOREIGN KEY ([fk_work]) REFERENCES [work] ([id_work]),
    FOREIGN KEY ([fk_author]) REFERENCES [author] ([id_author])
);
