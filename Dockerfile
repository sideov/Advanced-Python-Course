# Чтобы работало - надо переместить в корень проекта
# Локально проверил - работает: после запсука контейнера получаю вывод в консоли:
#Table saved to artifacts/table.tex
#PDF saved to artifacts/image_and_table.pdf

# Используем базовый образ Python 3.13 slim
FROM python:3.13-slim

# Устанавливаем системные зависимости, включая TeX Live
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Рабочая директория в контейнере
WORKDIR /app

# Копируем все файлы проекта в контейнер (чтобы pyproject.toml и другие файлы тоже попали)
COPY . .

# Отключаем создание виртуального окружения Poetry и устанавливаем зависимости
RUN poetry config virtualenvs.create false && poetry install --no-root

# Создаём папку для артефактов
RUN mkdir -p artifacts

RUN which pdflatex && pdflatex --version


# Команда по умолчанию для запуска генерации PDF
# Учтите, что в Dockerfile можно указать только один CMD. Если нужно запустить оба скрипта,
# можно создать скрипт-обёртку, который их вызовет или использовать docker-compose с несколькими сервисами.
CMD ["sh", "-c", "cd hw_2 && python save_table_and_pdf.py"]
