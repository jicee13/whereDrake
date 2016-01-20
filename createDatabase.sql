CREATE TABLE relevantArticles
(
  ID int NOT NULL AUTO_INCREMENT,
  Timestamp int NOT NULL,
  Title varchar(255) NOT NULL UNIQUE,
  Link varchar(255) NOT NULL UNIQUE,
  PRIMARY KEY (ID)
);

CREATE TABLE musicVids
(
  ID int NOT NULL AUTO_INCREMENT,
  Timestamp int NOT NULL,
  Title varchar(255) NOT NULL UNIQUE,
  Link varchar(255) NOT NULL UNIQUE,
  PRIMARY KEY (ID)
);
