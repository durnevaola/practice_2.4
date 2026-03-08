import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "ВАШ_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Ошибка", "Введите название города")
        return
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if data.get("cod") != 200:
            messagebox.showerror("Ошибка", f"Город не найден: {city}")
            return
        
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"].capitalize()
        icon_code = data["weather"][0]["icon"]
        
        weather_label.config(text=f"{city}: {temp}°C\n{description}")
        
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_image = Image.open(BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo  
        
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

root = tk.Tk()
root.title("Погода в городе")
root.geometry("300x300")

city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)

get_weather_button = tk.Button(root, text="Показать погоду", command=get_weather)
get_weather_button.pack(pady=5)

weather_label = tk.Label(root, text="", font=("Arial", 14))
weather_label.pack(pady=10)

icon_label = tk.Label(root)
icon_label.pack()

root.mainloop()
