import requests
import tkinter as tk

# API details
API_KEY = "b9504f3d4e4ce7e7c9464542c56e6c53"

# getting weather for searched city
def get_weather():


    # clear old results 
    for widget in result_frame.winfo_children():
        widget.destroy()

    city = city_entry.get()
    if not city:
        tk.Label(result_frame, text="Please enter a city", fg="red", bg="lightblue").pack()
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

        # Create new labels inside result_frame
        tk.Label(result_frame, text=f"Weather in {city_name}", bg="white", font=("Arial", 12)).pack(pady=5, fill="x")
        tk.Label(result_frame, text=f"Temperature: {temperature}°C", bg="white", font=("Arial", 12)).pack(pady=5, fill="x")
        tk.Label(result_frame, text=f"Condition: {weather_desc}", bg="white", font=("Arial", 12)).pack(pady=5, fill="x")
        tk.Label(result_frame, text=f"Humidity: {humidity}%", bg="white", font=("Arial", 12)).pack(pady=5, fill="x")
        tk.Label(result_frame, text=f"Wind Speed: {wind_speed} m/s", bg="white", font=("Arial", 12)).pack(pady=5, fill="x")

    else:
        tk.Label(result_frame, text="City not found or API error", fg="red", bg="lightblue").pack()


# Tkinter window
window = tk.Tk()
window.title("Weather App")
window.geometry("400x400")
window.configure(bg="lightblue")

# Search box
city_entry = tk.Entry(window, width=25, font=("Arial", 12))
city_entry.pack(pady=10)

# Enter key = search
city_entry.bind("<Return>", lambda event: get_weather())

search_button = tk.Button(window, text="Search", command=get_weather)
search_button.pack(pady=5)

# Frame to hold all results
result_frame = tk.Frame(window, bg="lightblue")
result_frame.pack(pady=10, fill="both", expand=True)

window.mainloop()
