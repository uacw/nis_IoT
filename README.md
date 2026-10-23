# Raspberry Pi: лабораторные №1–3

- `raspberry/lab01_rgb.py` — RGB-светодиод и три кнопки.
- `raspberry/lab02_camera.py` — камера Picamera2 и серво, в том числе Raspberry Pi 5.
- `raspberry/lab02_camera_legacy.py` — вариант №2 для старого camera stack на Pi 3/4.
- `raspberry/lab03_weather.py` — BME280, температура, влажность и давление в мм рт. ст.

## Скачать на Raspberry

```sh
git clone https://github.com/uacw/nis_IoT.git ~/nis_IoT
```

**[Подробная инструкция: подключение, настройка, кнопки и результат](raspberry/START_HERE.md)**.

Открой нужный `.py` из `~/nis_IoT/raspberry` в Thonny и нажми F5.
Python, библиотеки и соединения сначала настроить по инструкции.

`requirements.txt` содержит pip-зависимости для №3. GPIO, Tkinter, Pillow и
Picamera2 устанавливаются системными пакетами Raspberry Pi OS, как описано в мануале.
Программы запускаются на Raspberry с графическим рабочим столом.

Код проверен на синтаксис и отдельные сценарии с программными заглушками.
Настоящая камера, GPIO, серво и датчики требуют проверки на учебном комплекте.
