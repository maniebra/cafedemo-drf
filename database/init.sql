DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS Items CASCADE;
DROP TABLE IF EXISTS Carts CASCADE;
DROP TABLE IF EXISTS Drink CASCADE;
DROP TABLE IF EXISTS Food CASCADE;
DROP TABLE IF EXISTS CartItems CASCADE;

CREATE TABLE Users (
    user_id         SERIAL PRIMARY KEY,
    first_name      VARCHAR(64) NOT NULL,
    last_name       VARCHAR(64),
    phone_number    VARCHAR(13) UNIQUE NOT NULL,
    email           VARCHAR(64) UNIQUE NOT NULL,
    password        VARCHAR(64) NOT NULL,
    is_admin        BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE Items (
    item_id         SERIAL PRIMARY KEY,
    title           VARCHAR(64),
    description     VARCHAR(255),
    image_url       VARCHAR(255),
    price           INTEGER,
    stock           INTEGER,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE Food (
    prep_time       INTEGER
) INHERITS(Items);

CREATE TABLE Drink (
    is_hot          BOOLEAN
) INHERITS(Items);

CREATE TABLE Carts (
    cart_id         SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES Users(user_id),
    checked_out     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

CREATE TABLE CartItems (
    cart_id         INTEGER REFERENCES Carts(cart_id),
    item_id         INTEGER REFERENCES Items(item_id),
    amount          INTEGER,
    added_at        TIMESTAMP DEFAULT NOW()
);