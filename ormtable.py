from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.types import DateTime
from datetime import datetime

Base = declarative_base()

# Модель для издателей (авторов/издателей)
class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    # Связь с книгами
    books = relationship("Book", back_populates="publisher")

    def __repr__(self):
        return f"<Publisher(id={self.id}, name='{self.name}')>"

# Модель для книг
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=False)

    # Связь с издателем
    publisher = relationship("Publisher", back_populates="books")
    # Связь с складами через таблицу Stock
    stocks = relationship("Stock", back_populates="book")
    # Связь с продажами
    sales = relationship("Sale", back_populates="book")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', publisher_id={self.publisher_id})>"

# Модель для складов
class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    quantity = Column(Integer, nullable=False)  # Количество книг на складе

    # Связь с книгой
    book = relationship("Book", back_populates="stocks")
    # Связь с продажами
    sales = relationship("Sale", back_populates="stock")

    def __repr__(self):
        return f"<Stock(id={self.id}, book_id={self.book_id}, quantity={self.quantity})>"

# Модель для продаж
class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    sold_quantity = Column(Integer, nullable=False)  # Количество проданных книг
    sale_date = Column(DateTime, default=datetime.utcnow)  # Дата продажи
    price = Column(Float, nullable=False)  # Цена продажи

    # Связь с складом (Stock)
    stock = relationship("Stock", back_populates="sales")
    # Связь с книгой
    book = relationship("Book", back_populates="sales")

    def __repr__(self):
        return f"<Sale(id={self.id}, stock_id={self.stock_id}, book_id={self.book_id}, " \
               f"sold_quantity={self.sold_quantity}, sale_date={self.sale_date}, price={self.price})>"