# Документация по проекту API для управления библиотекой

Этот проект представляет собой RESTful API для управления каталогом библиотеки,  
включая управление книгами, авторами, читателями и арендой книг. 
Система поддерживает аутентификацию пользователей с помощью JWT токенов, роли 
для администратора и читателя.

## Установка

### Требования

- Python 3.12+
- PostgreSQL

### Шаги

1. **Клонировать репозиторий**:

   ```
   git clone https://github.com/Ydtalel/library.git
   cd library
   ```
2. **Создать виртуальное окружение:**

   ```
   python3 -m venv venv
   source venv/bin/activate  # Для Windows используйте venv\Scripts\activate
   ```
3. **Установить зависимости:**

   ```
   pip install -r requirements.txt
   ```
4. **Настроить переменные окружения:**

   Создайте файл .env в корне проекта и добавьте следующие строки:
   ```
   DATABASE_URL=postgresql://user:password@localhost/dbname
   JWT_SECRET_KEY=your-secret-key
   ```
   Настройте DATABASE_URL в соответствии с вашей конфигурацией PostgreSQL.  

5. **Применить миграции:**

   ```
   alembic upgrade head
   ```
6. **Запуск приложения:**

   Для запуска сервера FastAPI выполните команду:

   ```
   uvicorn app.main:app --reload
   ```
   API будет доступно по адресу http://127.0.0.1:8000
7. **Документация API:**  
   Документация API будет доступна по адресу:
   ```
   http://127.0.0.1:8000/docs
   ```
8. **Использование Postman**  
   Подготовлена коллекция Postman для удобного тестирования API   
   [Скачать коллекцию Postman](library.postman_collection.json)