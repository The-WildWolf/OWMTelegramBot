# Use the official Python image as the base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files to the working directory
COPY pyproject.toml poetry.lock ./

# Install Poetry and the required dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

# Copy the rest of the application code
COPY ./owmtelegrambot/bot.py /app/bot.py

# Start the application
CMD ["python", "bot.py"]
