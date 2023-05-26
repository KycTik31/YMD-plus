# **Yandex Music Discord Rich Presence**
Discord RPC для приложения и веб версии Яндекс Музыки*

![src](https://img.shields.io/badge/source%20code-open-red)
![src2](https://img.shields.io/badge/language-python-blue)

Базовый код взят: https://github.com/maj0roff/YandexMusicDiscordRPC

Доработал и улучшил код: я :)

------------

*время до конца музыки не работает в веб версии (в этом случае не включайте эту функицю, в противном случае у вас в статусе будет "Моя волна", для веб версии существует https://premid.app/) 

## Требования
если вы не будете использовать ехе файл то:
1. Python 3.10+ (если на меньшей версии не будет работать, не отправляйте баг репорт)

иначе:
1. ничего не требуется 

## Как использовать?
1. Скачиваем файлы с репозитория (README.md и .gitignore можно удалить)

если пошли по пути без ехе файла:

2. Открываем файл start.bat и ждём пока установятся все необходимые пакеты (это может занять от нескольких секунд до нескольких минут, зависит от вашего интернета)

иначе:

2. запускаем YMD.exe


3. Ждём до того пока не вылезет окно о первом запуске
4. Далее авторизовываемся для получения токена
5. Радуемся т.к программа работает!


## А теперь немного разьяснений
Полное копирование программы с последующим распространением от своего имени запрещенно

Копирование программы с внесением доработок и распространнением разрешено (по возможности укажите автора)

Автор данной программы не несёт ответственность за данные ваших аккаунтов

Есть один известный баг, когда только заходишь в яндекс музыку, не запускаешь трек и сразу открываешь программу, если стоит галочка показывать время, то в статусе будет "Моя волна" (пофиксить это невозможно т.к это работа с памятью, а переменная появляется только после вкючения трека)

(да я слизал оформление с того гитхаба, ae))


## TODO
уменьшить размер ехе файла
