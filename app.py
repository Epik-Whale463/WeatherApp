from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_key = "49406edf8d9a4028b2c44215240903"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']

    current_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    current_response = requests.get(current_url)

    if current_response.status_code == 200:
        current_data = current_response.json()

        temperature = current_data['current']['temp_c']
        condition = current_data['current']['condition']['text']
        wind_speed = current_data['current']['wind_kph']
        feels_like = current_data['current']['feelslike_c']
        DayorNight = current_data['current']['is_day']

        day_or_night_js = 'true' if DayorNight else 'false'

        forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=5"  # You can adjust the number of days as needed

        forecast_response = requests.get(forecast_url)

        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()

            forecast_days = []

            for day in forecast_data['forecast']['forecastday']:
                date = day['date']
                temp = day['day']['avgtemp_c']
                condition = day['day']['condition']['text']

                forecast_days.append({
                    'date': date,
                    'temperature': temp,
                    'condition': condition
                })

            return render_template('weather.html', city=city, temperature=temperature, condition=condition,
                                   wind_speed=wind_speed, feels_like=feels_like, DayorNight=day_or_night_js,
                                   forecast_days=forecast_days)
        else:
            error_message = f"Forecast Error: {forecast_response.status_code}, {forecast_response.text}"
            return render_template('error.html', error_message=error_message)
    else:
        error_message = f"Current Weather Error: {current_response.status_code}, {current_response.text}"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
