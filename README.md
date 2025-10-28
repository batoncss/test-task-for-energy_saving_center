## 📌 Ссылки
[Скачать текст задания](docs/exercise.xlsx)

[Скачать пример данных](data/sample.xlsx)

## 📦 Установка и запуск
$$
\text{Просроченная задолженность} = \max \big(0, 
\text{ДЗ}_{\text{конец}} - \text{КЗ}_{\text{конец}} - \text{Начислено} \big)
$$
ДЗ — дебиторская задолженность
КЗ — кредиторская задолженность

1. Клонировать репозиторий:
```bash
    git clone <URL_репозитория>
    cd my_project
```
2. Установить зависимости:
```bash
  pip install -r requirements.txt
```
3. Создать .env с SECRET_KEY
```bash
    SECRET_KEY=<Ваш ключ>
```
4. Запустить сервер:
```bash
    python manage.py runserver
```
5. Открыть в браузере: http://127.0.0.1:8000/report/

