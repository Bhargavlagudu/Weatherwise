
from flask import Flask, request, jsonify, render_template
import requests
import urllib3
from flask_cors import CORS

# Disable SSL warnings (for local cert issues)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)

API_KEY = "65b7c5474e9f1f829d43342034fc8acd"  # Replace this with your OpenWeatherMap API key

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/weather')
def get_weather():
    city = request.args.get('city', '')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        data = response.json()

        return jsonify({
            'city': city.title(),
            'weather': data['weather'][0]['description'].title(),
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        })

    except requests.exceptions.HTTPError:
        return jsonify({'error': 'City not found or API error'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
