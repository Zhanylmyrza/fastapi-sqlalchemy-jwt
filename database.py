from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base



# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:A78J79Zh001@localhost/TodoAplicationDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:a78j79zh001@127.0.0.1:3306/TodoApplicationDatabase'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
                                                             


SessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
















'''

Движок (engine) — это всего лишь мост между твоим кодом и базой данных. 

это объект SQLAlchemy, который управляет подключением к базе данных.

Он:

Управляет соединением с базой данных.
Определяет, какие SQL-запросы отправлять.
Обеспечивает работу с разными типами баз данных (PostgreSQL, SQLite, MySQL и т. д.).



Сессия (SessionLocal) — это объект, через который мы выполняем CRUD-операции (добавление, удаление, изменение, чтение данных).

Она хранит подключение к базе и управляет транзакциями.
Позволяет работать с ORM-моделями (например, User, Todo и т. д.).


🔹 Токен (например, JWT-токен) — это ключ, который используется для аутентификации и авторизации пользователей. Он не связан с работой базы данных напрямую.


Что делает Base?

Он не создает объект, а создает базовый класс для всех моделей базы данных.
Все будущие модели унаследуют этот класс и станут таблицами в базе.





Движок (engine управляет соединением, а CRUD-операции делает сессия.
Сессия (SessionLocal) управляет работой с базой, а токен — это ключ для аутентификации.
Base — это родительский класс для всех моделей, а не объект.

'''