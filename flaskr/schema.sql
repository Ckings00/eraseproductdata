DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS approve_list CASCADE;

CREATE TABLE product (
    product = TEXT UNIQUE NOT NULL;
    textfield = TEXT;
    PRIMARY KEY (product);
);

CREATE TABLE approve_list (
    product = TEXT UNIQUE NOT NULL;
    textfield = TEXT;
    PRIMARY KEY (product);
);
