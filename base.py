import requests
import tkinter as tk

window = tk.Tk()
window.title("Weather App")
window.geometry("400x300")
window.configure(bg="lightblue")


API_KEY = "b9504f3d4e4ce7e7c9464542c56e6c53"
CITY = "Bangalore"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"   

response = requests.get(URL)


if response.status_code == 200:
    data = response.json()

    #weather info
    city_name = data["name"]
    temperature = data["main"]["temp"]
    weather_desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]  

    #weather info
    print(f"Weather in {city_name}:")   
    print(f"Temperature: {temperature}°C")
    print(f"Condition: {weather_desc}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")


    tk.Label(window, text=f"Weather in {city_name}:", bg="lightblue").pack()
    tk.Label(window, text=f"Temperature: {temperature}°C", bg="lightblue").pack()
    tk.Label(window, text=f"Condition: {weather_desc}", bg="lightblue").pack()
    tk.Label(window, text=f"Humidity: {humidity}%", bg="lightblue").pack()
    tk.Label(window, text=f"Wind Speed: {wind_speed} m/s", bg="lightblue").pack()

else:
    print("Can't get data right now:", response.status_code)

    tk.Label(window, text="Error fetching data", bg="lightblue").pack()



window.mainloop()
