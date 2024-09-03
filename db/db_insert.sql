--
-- Insert for table [bookshelf]
--
INSERT INTO [bookshelf] ([name])
VALUES
    ('Read'),
    ('Reading'),
    ('To be read'),
    ('Not finished'),
    ('No way');

--
-- Insert a test user
--
INSERT INTO [user] ([username], [password])
VALUES ('Admin', '$argon2id$v=19$m=65536,t=3,p=4$PaCybJopVsaeeospmU7aKQ$2w0pIvd+VPRWAEohwv/DWIZSy/KbsJLrD8Op9Bvl2q4');
