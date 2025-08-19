import requests
import tkinter as tk

# API details
API_KEY = "b9504f3d4e4ce7e7c9464542c56e6c53"

# getting weather for searched city
def get_weather():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city")
        return

    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()

        city_name = data["name"]
        temperature = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Update labels
        city_label.config(text=f"Weather in {city_name}")
        temp_label.config(text=f"Temperature: {temperature}°C")
        condition_label.config(text=f"Condition: {weather_desc}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")

    else:
        result_label.config(text="City not found or API error")


# Tkinter window
window = tk.Tk()
window.title("Weather App")
window.geometry("400x400")
window.configure(bg="lightblue")

# Search box
city_entry = tk.Entry(window, width=25, font=("Arial", 12))
city_entry.pack(pady=10)

search_button = tk.Button(window, text="Search", command=get_weather)
search_button.pack(pady=5)

# Frames for each info block
city_frame = tk.Frame(window, bg="white", padx=10, pady=5)
city_frame.pack(pady=5, fill="x")

temp_frame = tk.Frame(window, bg="white", padx=10, pady=5)
temp_frame.pack(pady=5, fill="x")

condition_frame = tk.Frame(window, bg="white", padx=10, pady=5)
condition_frame.pack(pady=5, fill="x")

humidity_frame = tk.Frame(window, bg="white", padx=10, pady=5)
humidity_frame.pack(pady=5, fill="x")

wind_frame = tk.Frame(window, bg="white", padx=10, pady=5)
wind_frame.pack(pady=5, fill="x")

# Labels inside frames
city_label = tk.Label(city_frame, text="Weather info will appear here", bg="white", font=("Arial", 12))
city_label.pack()

temp_label = tk.Label(temp_frame, text="", bg="white", font=("Arial", 12))
temp_label.pack()

condition_label = tk.Label(condition_frame, text="", bg="white", font=("Arial", 12))
condition_label.pack()

humidity_label = tk.Label(humidity_frame, text="", bg="white", font=("Arial", 12))
humidity_label.pack()

wind_label = tk.Label(wind_frame, text="", bg="white", font=("Arial", 12))
wind_label.pack()

# Result label (for errors)
result_label = tk.Label(window, text="", bg="lightblue", fg="red", font=("Arial", 10))
result_label.pack(pady=5)

window.mainloop()
