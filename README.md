# Инструкция

## Настройка

1. Открыть nginx.conf по пути \nginx-1.27.1\conf

   Изменить в location proxy_pass на свой ip
2. Открыть pyvenv.cfg по пути \venv

   Изменить пути к интерпритаторам

## Запуск

1. Запустить виртуальное окружение:

         .\venv\Scripts\activate

1. Запустить nginx

   В \nginx-1.27.1 запускать nginx_start.exe

   Также можно остановить nginx_stop.exe

2. Запустить приложение:

         python app.py

    Стандартный запуск:

         python -m flask run

## Дополнительно:

Создаёт requirements.txt:

python -m pip freeze > requirements.txt

Установить requirements.txt:

python -m pip install -r requirements.txt

   powershell

   python -m pip freeze | ForEach-Object { python -m pip uninstall -y $_ }