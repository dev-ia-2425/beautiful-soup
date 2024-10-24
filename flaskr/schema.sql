DROP TABLE IF EXISTS country_pib;

CREATE TABLE country_pib (
   rank INTEGER PRIMARY KEY,
   country TEXT NOT NULL,
   pib INTEGER NOT NULL
);