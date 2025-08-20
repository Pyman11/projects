import requests
import tkinter as tk
from datetime import datetime

API_KEY = "b9504f3d4e4ce7e7c9464542c56e6c53"

forecast_data = []
current_page = 0

def get_weather():
    global forecast_data, current_page
    city = city_entry.get()
    if not city:
        story_label.config(text="⚠️ Please enter a city")
        return

    URL = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        forecast_data = []

        # pick forecast at 12:00 for each day
        for entry in data["list"]:
            time = entry["dt_txt"]
            if "12:00:00" in time:
                date = datetime.strptime(time, "%Y-%m-%d %H:%M:%S").strftime("%a, %d %b")
                temp = entry["main"]["temp"]
                desc = entry["weather"][0]["description"].capitalize()
                humidity = entry["main"]["humidity"]
                wind = entry["wind"]["speed"]

                forecast_data.append(
                    f"📅 {date}\n\n🌡️ {temp}°C\n🌤️ {desc}\n\n💧 Humidity: {humidity}%\n💨 Wind: {wind} m/s"
                )

        current_page = 0
        show_page()
    else:
        story_label.config(text="❌ City not found or API error")

def show_page():
    if forecast_data:
        story_label.config(text=forecast_data[current_page])

def next_page():
    global current_page
    if forecast_data and current_page < len(forecast_data) - 1:
        current_page += 1
        show_page()

def prev_page():
    global current_page
    if forecast_data and current_page > 0:
        current_page -= 1
        show_page()


# Tkinter window
window = tk.Tk()
window.title("Weather Stories")
window.geometry("400x600")
window.configure(bg="black")

# Search bar
city_entry = tk.Entry(window, width=25, font=("Arial", 14))
city_entry.pack(pady=15)

city_entry.bind("<Return>", lambda event: get_weather())
search_button = tk.Button(window, text="Search", command=get_weather)
search_button.pack()

# Story-style display
story_label = tk.Label(
    window,
    text="🔍 Search for a city",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="black",
    justify="center",
    wraplength=350
)
story_label.pack(expand=True)

# Navigation buttons
frame = tk.Frame(window, bg="black")
frame.pack(pady=10)

prev_button = tk.Button(frame, text="⬅️ Prev", command=prev_page)
prev_button.grid(row=0, column=0, padx=10)

next_button = tk.Button(frame, text="Next ➡️", command=next_page)
next_button.grid(row=0, column=1, padx=10)

window.mainloop()
