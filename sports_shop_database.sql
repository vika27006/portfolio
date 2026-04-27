-- Создание таблицы "Категория"
CREATE TABLE Category (
    CategoryID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE,
    Description VARCHAR(1000)
);

-- Создание таблицы "Клиент"
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    Email VARCHAR(255),
    Address VARCHAR(500)
);

-- Создание таблицы "Товар"
CREATE TABLE Product (
    ProductID INT PRIMARY KEY,
    CategoryID INT NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Brand VARCHAR(100),
    Price DECIMAL(10,2) NOT NULL,
    StockQuantity INT NOT NULL,
    Description VARCHAR(1000),
    CONSTRAINT CHK_Price CHECK (Price >= 0),
    CONSTRAINT CHK_Stock CHECK (StockQuantity >= 0)
);

-- Создание таблицы "Заказ"
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATE NOT NULL,
    Status VARCHAR(50) NOT NULL,
    TotalAmount DECIMAL(10,2) NOT NULL,
    DeliveryAddress VARCHAR(500) NOT NULL,
    CONSTRAINT CHK_TotalAmount CHECK (TotalAmount >= 0)
);

-- Создание таблицы "Позиция заказа" 
CREATE TABLE OrderItem (
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    CONSTRAINT PK_OrderItem PRIMARY KEY (OrderID, ProductID),
    CONSTRAINT CHK_Quantity CHECK (Quantity > 0),
    CONSTRAINT CHK_UnitPrice CHECK (UnitPrice >= 0)
);

-- Добавление ограничений через ALTER TABLE
-- Внешний ключ: Товар -> Категория
ALTER TABLE Product
ADD CONSTRAINT FK_Product_Category 
FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID);

-- Внешний ключ: Заказ -> Клиент
ALTER TABLE Orders
ADD CONSTRAINT FK_Order_Customer 
FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID);

-- Внешний ключ: Позиция заказа -> Заказ
ALTER TABLE OrderItem
ADD CONSTRAINT FK_OrderItem_Order 
FOREIGN KEY (OrderID) REFERENCES Orders(OrderID);

-- Внешний ключ: Позиция заказа -> Товар
ALTER TABLE OrderItem
ADD CONSTRAINT FK_OrderItem_Product 
FOREIGN KEY (ProductID) REFERENCES Product(ProductID);

-- Добавление ограничения CHECK для статуса заказа
ALTER TABLE Orders
ADD CONSTRAINT CHK_OrderStatus 
CHECK (Status IN ('Обрабатывается', 'Оплачен', 'Доставляется', 'Выполнен', 'Отменен'));

-- Вставка тестовых данных 
-- Сначала добавляем категории с явными ID
INSERT INTO Category (CategoryID, Name, Description) VALUES
(1, 'Футбол', 'Мячи, форма, бутсы, аксессуары для футбола'),
(2, 'Фитнес', 'Гантели, коврики, экипировка для тренировок'),
(3, 'Туризм', 'Палатки, рюкзаки, спальные мешки');

-- Добавляем клиентов с явными ID
INSERT INTO Customer (CustomerID, FullName, Phone, Email, Address) VALUES
(101, 'Иванов Петр Сергеевич', '+7(999)123-45-67', 'ivanov@mail.ru', 'г. Москва, ул. Ленина, д. 10'),
(102, 'Сидорова Анна Владимировна', '+7(999)765-43-21', 'sidorova@gmail.com', 'г. Санкт-Петербург, пр. Мира, д. 5');

-- Добавляем товары с явными ID
INSERT INTO Product (ProductID, CategoryID, Name, Brand, Price, StockQuantity, Description) VALUES
(1001, 1, 'Футбольный мяч Champions League', 'Adidas', 2999.99, 15, 'Официальный мяч для матчей Лиги Чемпионов'),
(1002, 2, 'Гантели разборные 20 кг', 'Torres', 3499.50, 8, 'Набор гантелей с блинами'),
(1003, 3, 'Палатка 4-местная Trekker', 'Tramp', 8999.00, 3, 'Палатка для кемпинга с москитной сеткой');

-- Добавляем заказы с явными ID
INSERT INTO Orders(OrderID, CustomerID, OrderDate, Status, TotalAmount, DeliveryAddress) VALUES
(5001, 101, '2024-03-10 14:30:00', 'Выполнен', 2999.99, 'г. Москва, ул. Ленина, д. 10'),
(5002, 102, '2024-03-12 10:15:00', 'Доставляется', 12498.50, 'г. Санкт-Петербург, пр. Мира, д. 5');

-- Добавляем позиции заказов
INSERT INTO OrderItem (OrderID, ProductID, Quantity, UnitPrice) VALUES
(5001, 1001, 1, 2999.99),
(5002, 1002, 2, 3499.50),
(5002, 1003, 1, 8999.00);
