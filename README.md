# SkyStore

Проект интернет-магазина с блогом на Django

## Installation

Установка зависимостей через pip

```bash
pip install -r requirements.txt
```

Заполнение товарами:
```bash
python3 manage.py fill_catalog
```

Заполнение блога:
```bash
python3 manage.py fill_blog
```


## Использование

Вся логика создания и управления товарами находится в приложении `backoffice`. На странице магазина перейти к управлению товарами и статьями можно по ссылке в меню "Панель управления".

## Версии товаров

Версии можно добавлять при редактировании товаров (Панель управления - Товары - Редактировать). 
