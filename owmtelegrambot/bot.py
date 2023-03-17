"""
This script provides weather information and clothing suggestions based on the current weather
and forecast for a specified city and country code using the Telegram bot framework Aiogram and
the OpenWeatherMap API wrapper.
"""

import logging
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from openweathermapwrapper.weather import Weather
from openweathermapwrapper.clothing import ClothingSuggestions

API_TOKEN = os.environ['TELEGRAM_API_TOKEN']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

weather = Weather()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """
    Bot /start command.
    Sends a message to the user asking for the city name and country code.

    Args:
        message (types.Message): The incoming message object from the user.
    """
    await message.reply("Please enter the city name and country code separated by a comma (e.g., New York, US):")


@dp.message_handler(lambda message: ',' in message.text)
async def process_location(message: types.Message):
    """
    Processes the user's input, extracting the city and country code, and sends an InlineKeyboard
    with options for current weather and forecast.

    Args:
        message (types.Message): The incoming message object containing the city name and country code.
    """
    city, country_code = [x.strip() for x in message.text.split(',')]
    country_code = country_code.upper()

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("CurrentWeather", callback_data=f"current_weather:{city}:{country_code}"),
        types.InlineKeyboardButton("Forecast", callback_data=f"forecast:{city}:{country_code}")
    )
    await message.reply("Please choose an option:", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith("current_weather"))
async def current_weather(callback_query: types.CallbackQuery):
    """
    Sends the current weather information and clothing suggestions for the specified city and country code.

    Args:
        callback_query (types.CallbackQuery): The incoming callback query object containing the city and country code.
    """
    _, city, country_code = callback_query.data.split(':')
    weather_temperature = weather.get_temperature(city,country_code)
    weather_conditions = weather.get_weather_condition(city, country_code)
    clothing_suggestions = ClothingSuggestions(weather, city, country_code)
    temperature_suggestions = clothing_suggestions.get_temperature_based_suggestions()
    condition_suggestions = clothing_suggestions.get_condition_based_suggestions()

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           f"Weather in {city}, {country_code}:\n"
                           f"Temperature: {weather_temperature}°C\n"
                           f"Condition: {weather_conditions}\n"
                           f"{temperature_suggestions}\n"
                           f"{condition_suggestions}",
                           parse_mode=ParseMode.HTML)


@dp.callback_query_handler(lambda c: c.data.startswith("forecast"))
async def forecast(callback_query: types.CallbackQuery):
    """
    Sends an InlineKeyboard with date options for the weather forecast.

    Args:
        callback_query (types.CallbackQuery): The incoming callback query object containing the city and country code.
    """
    await bot.answer_callback_query(callback_query.id)

    date_picker = types.InlineKeyboardMarkup()

    for i in range(1, 5):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        date_picker.add(types.InlineKeyboardButton(date, callback_data=f"date:{date}:{callback_query.data}"))

    await bot.send_message(callback_query.from_user.id, "Please select a date for the forecast:",
                           reply_markup=date_picker)


@dp.callback_query_handler(lambda c: c.data.startswith("date:"))
async def forecast_date(callback_query: types.CallbackQuery):
    """
    Sends the weather forecast for a specified date, city, and country code, along with clothing suggestions based on the
    forecasted weather conditions.

    Args:
    callback_query (types.CallbackQuery): The incoming callback query object containing the selected date, city, and
    country code.
    """
    _, date, _, city, country_code = callback_query.data.split(':')

    forecast_data = weather.client.get_forecast(city, country_code, date)
    forecast_temp = forecast_data["main"]["temp"]
    forecast_condition = forecast_data["weather"][0]["description"]
    clothing_suggestions = ClothingSuggestions(weather, city, country_code)
    temperature_suggestions = clothing_suggestions.get_temperature_based_suggestions()
    condition_suggestions = clothing_suggestions.get_condition_based_suggestions()

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           f"Forecast for {date} in {city}, {country_code}:\n"
                           f"Temperature: {forecast_temp}°C\n"
                           f"Condition: {forecast_condition}\n"
                           f"{temperature_suggestions}\n"
                           f"{condition_suggestions}",
                           parse_mode=ParseMode.HTML)


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
