DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS approve_list CASCADE;

CREATE TABLE product (
    id SERIAL NOT NULL
    product TEXT UNIQUE NOT NULL,
    textfield TEXT,
    related TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE approve_list (
    product TEXT UNIQUE NOT NULL,
    textfield TEXT,
    PRIMARY KEY (product)
);
