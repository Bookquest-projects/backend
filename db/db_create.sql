-- 
-- Delete existing tables
--
DROP TABLE IF EXISTS `author_work`;
DROP TABLE IF EXISTS `review`;
DROP TABLE IF EXISTS `book`;
DROP TABLE IF EXISTS `work`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `author`;
DROP TABLE IF EXISTS `serie`;
DROP TABLE IF EXISTS `publisher`;
DROP TABLE IF EXISTS `bookshelf`;

--
-- Table structure for table `author`
--
CREATE TABLE `author` (
    `id_author` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
    `description` TEXT,
    PRIMARY KEY (`id_author`),
    UNIQUE KEY `id_author_UNIQUE` (`id_author`),
    UNIQUE KEY `name_UNIQUE` (`name`)
);

--
-- Table structure for table `bookshelf`
--
CREATE TABLE `bookshelf` (
    `id_bookshelf` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id_bookshelf`),
    UNIQUE KEY `name_UNIQUE` (`name`),
    UNIQUE KEY `id_bookshelf_UNIQUE` (`id_bookshelf`)
);

--
-- Table structure for table `publisher`
--
CREATE TABLE `publisher` (
    `id_publisher` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
    `previous_id` INT UNSIGNED DEFAULT 0,
    PRIMARY KEY (`id_publisher`),
    UNIQUE KEY `id_publisher_UNIQUE` (`id_publisher`),
    UNIQUE KEY `previous_id_UNIQUE` (`previous_id`)
);

--
-- Table structure for table `serie`
--
CREATE TABLE `serie` (
    `id_serie` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `original_name` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id_serie`),
    UNIQUE KEY `id_serie_UNIQUE` (`id_serie`)
);

--
-- Table structure for table `user`
--
CREATE TABLE `user` (
    `id_user` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(45) NOT NULL,
    `email` VARCHAR(45) NOT NULL,
    `password` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`id_user`),
    UNIQUE KEY `email_UNIQUE` (`email`),
    UNIQUE KEY `id_user_UNIQUE` (`id_user`)
);

--
-- Table structure for table `work`
--
CREATE TABLE `work` (
    `id_work` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `original_title` VARCHAR(255) NOT NULL,
    `fk_serie` INT UNSIGNED DEFAULT NULL,
    PRIMARY KEY (`id_work`),
    UNIQUE KEY `id_work_UNIQUE` (`id_work`),
    KEY `fk_serie_idx` (`fk_serie`)
);

--
-- Table structure for table `book`
--
CREATE TABLE `book` (
    `id_book` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `ISBN_10` INT UNSIGNED NOT NULL,
    `ISBN_13` INT UNSIGNED NOT NULL,
    `title` VARCHAR(45) NOT NULL,
    `lang` VARCHAR(2) NOT NULL,
    `page_count` SMALLINT UNSIGNED NOT NULL,
    `volume_number` TINYINT UNSIGNED DEFAULT NULL,
    `publication_DATE` DATE DEFAULT NULL,
    `summary` TEXT,
    `fk_publisher` INT UNSIGNED DEFAULT NULL,
    `fk_work` INT UNSIGNED DEFAULT NULL,
    PRIMARY KEY (`id_book`),
    UNIQUE KEY `ISBN_10_UNIQUE` (`ISBN_10`),
    UNIQUE KEY `ISBN_13_UNIQUE` (`ISBN_13`),
    CONSTRAINT `book_fk_publisher_idx` FOREIGN KEY (`fk_publisher`)
        REFERENCES `publisher` (`id_publisher`),
    CONSTRAINT `book_fk_work_idx` FOREIGN KEY (`fk_work`)
        REFERENCES `work` (`id_work`)
);

--
-- Table structure for table `review`
--
CREATE TABLE `review` (
    `id_review` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `ratings` TINYINT DEFAULT NULL,
    `favorite` TINYINT UNSIGNED DEFAULT NULL,
    `owned` TINYINT UNSIGNED DEFAULT NULL,
    `reading_DATE` DATE DEFAULT NULL,
    `reading_number` TINYINT DEFAULT NULL,
    `comment` TEXT,
    `fk_user` INT UNSIGNED DEFAULT NULL,
    `fk_book` INT UNSIGNED DEFAULT NULL,
    `fk_bookshelf` INT UNSIGNED DEFAULT NULL,
    PRIMARY KEY (`id_review`),
    UNIQUE KEY `id_review_UNIQUE` (`id_review`),
    CONSTRAINT `review_fk_user_idx` FOREIGN KEY (`fk_user`)
        REFERENCES `user` (`id_user`),
    CONSTRAINT `review_fk_book_idx` FOREIGN KEY (`fk_book`)
        REFERENCES `book` (`id_book`),
    CONSTRAINT `review_fk_bookshelf_idx` FOREIGN KEY (`fk_bookshelf`)
        REFERENCES `bookshelf` (`id_bookshelf`)
);

--
-- Table structure for table `auhtor_work`
--
CREATE TABLE `auhtor_work` (
    `fk_author` INT UNSIGNED NOT NULL,
    `fk_work` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`fk_work` , `fk_author`),
    CONSTRAINT `auhtor_work_fk_work_idx` FOREIGN KEY (`fk_work`)
        REFERENCES `work` (`id_work`),
    CONSTRAINT `auhtor_work_fk_auhtor_idx` FOREIGN KEY (`fk_author`)
        REFERENCES `author` (`id_author`)
);