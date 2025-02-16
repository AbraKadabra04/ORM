from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Publisher, Book, Shop, Sale, Stock  # Импорт ваших моделей

# Настройка подключения к базе данных (замените значения на ваши данные подключения)
DATABASE_URL = "postgresql+psycopg2://username:password@localhost/database_name"

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL)

# Создаем таблицы в базе данных (если они еще не существуют)
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()

def get_sales_by_publisher(publisher_name_or_id: str):
    """
    Получает информацию о продажах книг указанного издателя (по имени или id).
    :param publisher_name_or_id: Имя или идентификатор издателя
    """
    try:
        # Проверяем, введено ли имя издателя (строка) или id (число)
        if publisher_name_or_id.isdigit():
            publisher_filter = Publisher.id == int(publisher_name_or_id)
        else:
            publisher_filter = Publisher.name.ilike(publisher_name_or_id)

        # Выполняем запрос с использованием соединений таблиц
        query = (
            session.query(
                Book.title,  # Название книги
                Shop.name.label("shop_name"),  # Название магазина
                Sale.price,  # Стоимость покупки
                Sale.date_sale  # Дата покупки
            )
            .join(Publisher, Publisher.id == Book.publisher_id)  # Связь книги с издателем
            .join(Stock, Stock.book_id == Book.id)  # Связь книги со складом
            .join(Shop, Shop.id == Stock.shop_id)  # Связь склада с магазином
            .join(Sale, Sale.stock_id == Stock.id)  # Связь склада с продажей
            .filter(publisher_filter)  # Фильтр по издателю
        )

        # Выполняем запрос и обрабатываем результаты
        results = query.all()
        if not results:
            print(f"Нет данных для издателя: {publisher_name_or_id}")
            return

        print(f"Результаты для издателя: {publisher_name_or_id}")
        for title, shop_name, price, date_sale in results:
            # Форматируем дату и выводим результат
            print(f"{title} | {shop_name} | {price:.2f} | {date_sale.strftime('%d-%m-%Y')}")
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
    finally:
        # Закрываем сессию
        session.close()

if __name__ == "__main__":
    # Ввод имени или идентификатора издателя
    publisher_input = input("Введите имя или идентификатор издателя: ").strip()
    get_sales_by_publisher(publisher_input)