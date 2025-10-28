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
2. Создать виртуальное окружение и активировать его:
```bash
    python3 -m venv venv
    source venv/bin/activate
```
3. Установить зависимости:
```bash
  pip install -r requirements.txt
```
4. Создать .env вида:
```
SECRET_KEY=<Ваш ключ>
```    
5. Запустить сервер:
```bash
    python3 manage.py runserver
```
6. Открыть в браузере: http://127.0.0.1:8000/report/

