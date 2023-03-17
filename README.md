# OpenWeatherMap Telegram Bot

This Telegram bot provides weather information and clothing suggestions based on the current weather and forecast for a specified city and country code. 
Stack: Aiogram, Telegram, OpenWeatherMap API.

## Features
* Get current weather information for a specified city and country code
* Get weather forecast for up to 4 days in the future
* Receive clothing suggestions based on the current weather and forecasted weather conditions

## Installation
1. Clone the repository:

```bash
git clone https://github.com/The-WildWolf/OWMTelegramBot.git
cd OWMTelegramBot
```
2. Install Poetry to manage dependencies.
3. Install the required dependencies using Poetry:

```bash
poetry install
```

4. Set the environment variable TELEGRAM_API_TOKEN with your Telegram bot API token:

```bash
export TELEGRAM_API_TOKEN="your_telegram_api_token_here"
```

5. Run the bot:
```bash
poetry run python your_bot_file.py
```

## Usage
1. Start a conversation with the bot on Telegram.
2. Send the /start command.
3. Enter the city name and country code separated by a comma (e.g., New York, US).
4. Choose an option: "CurrentWeather" or "Forecast".
5. If you choose "Forecast", select a date for the forecast.
6. The bot will send you the weather information and clothing suggestions based on the selected option.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue. If you want to contribute code, feel free to fork the repository and submit a pull request.
License

This project is licensed under the MIT License. See the LICENSE file for details.