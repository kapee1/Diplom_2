## Дипломный проект. Задание 2: API-Тесты

### Автотесты для проверки программы, которая помогает заказать бургер в Stellar Burgers


### Структура проекта

- `allure-report` - пакет, содержащий код программы
- `tests` - пакет, содержащий тесты, разделенные по разным классам
### Запуск автотестов

**Установка зависимостей**

> `$ pip install -r requirements.txt`

**Запуск тестов и сохранение результатов тестирования**

>  `$ pytest .\tests --alluredir=allure_report`  

**Создание HTML-отчета о результатах тестов**

>  `$ allure serve .\allure_report\   `
