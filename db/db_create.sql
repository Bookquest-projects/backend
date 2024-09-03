--
-- Table structure for table [bookshelf]
--
DROP TABLE IF EXISTS [bookshelf];
CREATE TABLE [bookshelf] (
    [id_bookshelf] INT NOT NULL IDENTITY(1,1),
    [name] NVARCHAR(45) NOT NULL,
    PRIMARY KEY ([id_bookshelf]),
    UNIQUE ([name])
);


--
-- Table structure for table [user]
--
DROP TABLE IF EXISTS [user];
CREATE TABLE [user] (
    [id_user] INT NOT NULL IDENTITY(1,1),
    [username] NVARCHAR(45) NOT NULL,
    [password] NVARCHAR(255) NOT NULL,
    PRIMARY KEY ([id_user]),
    UNIQUE ([username])
);


--
-- Table structure for table [review]
--
DROP TABLE IF EXISTS [review];
CREATE TABLE [review] (
    [id_review] INT NOT NULL IDENTITY(1,1),
    [isbn_13] NVARCHAR(13) NULL,
    [isbn_10] NVARCHAR(10) NULL,
    [ratings] TINYINT NULL,
    [favorite] BIT NULL,
    [owned] BIT NULL,
    [reading_date] DATE NULL,
    [reading_number] TINYINT DEFAULT 0,
    [comment] TEXT,
    [fk_user] INT NULL,
    [fk_bookshelf] INT NULL,
    PRIMARY KEY ([id_review]),
    FOREIGN KEY ([fk_user]) REFERENCES [user] ([id_user]),
    FOREIGN KEY ([fk_bookshelf]) REFERENCES [bookshelf] ([id_bookshelf])
);