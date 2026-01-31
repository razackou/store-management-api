-- =========================
-- TABLE: Client
-- =========================
CREATE TABLE client (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    phone       VARCHAR(30),
    address     TEXT
);

-- =========================
-- TABLE: Category
-- =========================
CREATE TABLE category (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL UNIQUE
);

-- =========================
-- TABLE: Product
-- =========================
CREATE TABLE product (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(150) NOT NULL,
    description  TEXT,
    unit_price   NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    stock        INTEGER NOT NULL CHECK (stock >= 0),
    category_id  INTEGER NOT NULL,
    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id)
        REFERENCES category(id)
);

-- =========================
-- TABLE: Employee
-- =========================
CREATE TABLE employee (
    id        SERIAL PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    position  VARCHAR(100)
);

-- =========================
-- TABLE: Order
-- =========================
CREATE TABLE orders (
    id            SERIAL PRIMARY KEY,
    order_date    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount  NUMERIC(12,2) NOT NULL CHECK (total_amount >= 0),
    status        VARCHAR(50) NOT NULL,
    client_id     INTEGER NOT NULL,
    employee_id   INTEGER,
    CONSTRAINT fk_order_client
        FOREIGN KEY (client_id)
        REFERENCES client(id),
    CONSTRAINT fk_order_employee
        FOREIGN KEY (employee_id)
        REFERENCES employee(id)
);

-- =========================
-- TABLE: Order_Product (Contenir)
-- N:N relationship with Quantity
-- =========================
CREATE TABLE order_product (
    order_id    INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id),
    CONSTRAINT fk_op_order
        FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_op_product
        FOREIGN KEY (product_id)
        REFERENCES product(id)
);
