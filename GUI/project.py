import customtkinter
from tkintermapview import TkinterMapView
import requests
from urllib.parse import quote  # Add this import
import requests
import pandas as pd
import numpy as np
import tensorflow as tf
from APIResponse import APIResponse 
import datetime
import os 
customtkinter.set_default_color_theme("blue")

def get_forecast(lat , lon):
    
    base= f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,sunshine_duration,relative_humidity_2m,dew_point_2m,apparent_temperature,rain,snowfall,snow_depth,pressure_msl,surface_pressure,cloud_cover,evapotranspiration,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_80m,wind_direction_80m,soil_temperature_54cm,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance,terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,global_tilted_irradiance_instant,terrestrial_radiation_instant&daily=sunshine_duration&forecast_days=16"
    response = requests.get(base)
    data = response.json()
    return data

def get_information_from_last_year(lat , lon, year):
    current_date = datetime.datetime.now() - datetime.timedelta(days=(365*year))
    last_year_date = datetime.datetime.now() - datetime.timedelta(days=365*(year+1))
     
    base= f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={last_year_date.strftime('%Y-%m-%d')}&end_date={current_date.strftime('%Y-%m-%d')}&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,rain,snowfall,snow_depth,pressure_msl,surface_pressure,cloud_cover,et0_fao_evapotranspiration,vapour_pressure_deficit,wind_speed_100m,wind_direction_100m,soil_temperature_100_to_255cm,sunshine_duration,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,global_tilted_irradiance,terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,direct_normal_irradiance_instant,global_tilted_irradiance_instant,terrestrial_radiation_instant&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,apparent_temperature_max,apparent_temperature_min,apparent_temperature_mean,daylight_duration,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours"
    response = requests.get(base)
    data = response.json()
    return data

def get_elevation(lat, lon):
        base_url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key=AIzaSyCZ734PDZl-Yv8e710uAq7D6h-d3E9SIAE"
        response = requests.get(base_url)
        data = response.json()
        if data['status'] == 'OK':
            elevation = data['results'][0]['elevation']
            return elevation
    
def add_values_to_futher_dataframe(lat , lon):
        api_information= get_forecast(lat,lon)
        instance = APIResponse(api_information)
        climatic_data_frame = pd.DataFrame()

        data = {
            'Latitude': [lat] * len(instance.hourly['time']),
            'Longitude': [lon] * len(instance.hourly['time']),
            'date': [t.split('T')[0] for t in instance.hourly['time']],
            'time': [t.split('T')[1] + ':00' for t in instance.hourly['time']],
            'Temperature': instance.hourly['temperature_2m'],
            'Humidity': instance.hourly['relative_humidity_2m'],
            'Dew Point': instance.hourly['dew_point_2m'],
            'Apparent Temperature': instance.hourly['apparent_temperature'],
            'Rain': instance.hourly['rain'],
            'Snowfall': instance.hourly['snowfall'],
            'Snow Depth': instance.hourly['snow_depth'],
            'Pressure MSL': instance.hourly['pressure_msl'],
            'Surface Pressure': instance.hourly['surface_pressure'],
            'Cloud Cover': instance.hourly['cloud_cover'],
            'ET0 FAO Evapotranspiration': instance.hourly['et0_fao_evapotranspiration'],
            'Vapour Pressure Deficit': instance.hourly['vapour_pressure_deficit'],
            'Wind Speed': instance.hourly['wind_speed_80m'],
            'Wind Direction': instance.hourly['wind_direction_80m'],
            'Soil Temperature': instance.hourly['soil_temperature_54cm'],
            'Sunshine Duration': instance.hourly['sunshine_duration'],
            'Shortwave Radiation': instance.hourly['shortwave_radiation'],
            'Direct Radiation': instance.hourly['direct_radiation'],
            'Diffuse Radiation': instance.hourly['diffuse_radiation'],
            'Direct Normal Irradiance': instance.hourly['direct_normal_irradiance'],
            'Global Tilted Irradiance': instance.hourly['global_tilted_irradiance'],
            'Terrestrial Radiation': instance.hourly['terrestrial_radiation'],
            'Shortwave Radiation Instant': instance.hourly['shortwave_radiation_instant'],
            'Direct Radiation Instant': instance.hourly['direct_radiation_instant'],
            'Diffuse Radiation Instant': instance.hourly['diffuse_radiation_instant'],
            'Direct Normal Irradiance Instant': instance.hourly['direct_normal_irradiance_instant'],
            'Global Tilted Irradiance Instant': instance.hourly['global_tilted_irradiance_instant'],
            'Terrestrial Radiation Instant': instance.hourly['terrestrial_radiation_instant'],
            'hour': [int(t.split('T')[1].split(':')[0]) for t in instance.hourly['time']]
        }
        climatic_data_frame = pd.DataFrame(data) 
        return climatic_data_frame

def add_values_to_climatic_data_frame_from_last_year(lat , lon, year):
    api_information= get_information_from_last_year(lat,lon, year)
    instance = APIResponse(api_information)
    print(instance)
    climatic_data_frame = pd.DataFrame()

    data = {
        'Latitude': [lat] * len(instance.hourly['time']),
        'Longitude': [lon] * len(instance.hourly['time']),
        'date': [t.split('T')[0] for t in instance.hourly['time']],
        'time': [t.split('T')[1] + ':00' for t in instance.hourly['time']],
        'Temperature': instance.hourly['temperature_2m'],
        'Humidity': instance.hourly['relative_humidity_2m'],
        'Dew Point': instance.hourly['dew_point_2m'],
        'Apparent Temperature': instance.hourly['apparent_temperature'],
        'Rain': instance.hourly['rain'],
        'Snowfall': instance.hourly['snowfall'],
        'Snow Depth': instance.hourly['snow_depth'],
        'Pressure MSL': instance.hourly['pressure_msl'],
        'Surface Pressure': instance.hourly['surface_pressure'],
        'Cloud Cover': instance.hourly['cloud_cover'],
        'ET0 FAO Evapotranspiration': instance.hourly['et0_fao_evapotranspiration'],
        'Vapour Pressure Deficit': instance.hourly['vapour_pressure_deficit'],
        'Wind Speed': instance.hourly['wind_speed_100m'],
        'Wind Direction': instance.hourly['wind_direction_100m'],
        'Soil Temperature': instance.hourly['soil_temperature_100_to_255cm'],
        'Sunshine Duration': instance.hourly['sunshine_duration'],
        'Shortwave Radiation': instance.hourly['shortwave_radiation'],
        'Direct Radiation': instance.hourly['direct_radiation'],
        'Diffuse Radiation': instance.hourly['diffuse_radiation'],
        'Direct Normal Irradiance': instance.hourly['direct_normal_irradiance'],
        'Global Tilted Irradiance': instance.hourly['global_tilted_irradiance'],
        'Terrestrial Radiation': instance.hourly['terrestrial_radiation'],
        'Shortwave Radiation Instant': instance.hourly['shortwave_radiation_instant'],
        'Direct Radiation Instant': instance.hourly['direct_radiation_instant'],
        'Diffuse Radiation Instant': instance.hourly['diffuse_radiation_instant'],
        'Direct Normal Irradiance Instant': instance.hourly['direct_normal_irradiance_instant'],
        'Global Tilted Irradiance Instant': instance.hourly['global_tilted_irradiance_instant'],
        'Terrestrial Radiation Instant': instance.hourly['terrestrial_radiation_instant'],
        'hour': [t.split('T')[1].split(':')[0] for t in instance.hourly['time']]
    }
    climatic_data_frame = pd.DataFrame(data)
    return climatic_data_frame



class App(customtkinter.CTk):

    APP_NAME = "Предсказване на мощност от фотоволтаична система"
    WIDTH = 1080
    HEIGHT = 1920

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)  # За левия frame
        self.grid_columnconfigure(1, weight=1)  # За десния frame
        self.grid_rowconfigure(0, weight=1)


        self.frame_left = customtkinter.CTkFrame(master=self, width=250, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.frame_left.grid_propagate(False)

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============
        self.frame_left.grid_rowconfigure(7, weight=1)
        

      

      #  self.button_2 = customtkinter.CTkButton(master=self.frame_left,
       #                                         text="Clear Markers",
        #                                        command=self.clear_marker_event)
       # self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.power_label = customtkinter.CTkLabel(self.frame_left, text="Максимална мощност (kW):", anchor="w", font=("Helvetica", 16))
        self.power_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 0))
        self.power_entry = customtkinter.CTkEntry(self.frame_left, font=("Helvetica", 12))
        self.power_entry.grid(row=1, column=0, padx=(20, 20), pady=(20, 0) )

        self.button_1 = customtkinter.CTkButton(master=self.frame_left, anchor="w",
                                                text="Изчисли", font=("Helvetica", 16),
                                                command=self.calculate)
        self.button_1.grid(row=2, column=0, padx=(20, 20), pady=(20, 0))

        self.power_for_the_next_16_days_label = customtkinter.CTkLabel(self.frame_left, text="",anchor="w")
        self.power_for_the_next_16_days_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))

        self.power_from_last_year_label = customtkinter.CTkLabel(self.frame_left, text="" , anchor="w")
        self.power_from_last_year_label.grid(row=4, column=0, padx=(20, 20), pady=(20, 0))

        self.power_from_year_1_label = customtkinter.CTkLabel(self.frame_left, text="" , anchor="w")
        self.power_from_year_1_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))

        self.power_from_year_2_label = customtkinter.CTkLabel(self.frame_left, text="" , anchor="w")
        self.power_from_year_2_label.grid(row=6, column=0, padx=(20, 20), pady=(20, 0))


        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Вид терен:", anchor="w" , font=("Helvetica", 16))
        self.map_label.grid(row=8, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                                       command=self.change_map)
        self.map_option_menu.grid(row=9, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Тема:", anchor="w" , font=("Helvetica", 16))
        self.appearance_mode_label.grid(row=10, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=11, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.lаt = 0
        self.lon = 0
        
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        script_directory = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(script_directory, "offline_tiles.db")
        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0, database_path=database_path)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="Въведете адрес")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Търси",
                                                font=("Helvetica", 16),
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.coord_label =  customtkinter.CTkLabel(self.frame_right, text="Координати: Няма избрани", font=("Helvetica", 16))
        self.coord_label.grid(row=0, column=2, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        self.map_widget.set_position(42.6977, 23.3219)
        self.map_option_menu.set("OpenStreetMap")
       # self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga")


      
        self.appearance_mode_optionemenu.set("Dark")
        self.map_widget.add_right_click_menu_command(label="Избери координати", command=self.update_coordinates, pass_coords=True)

    def update_coordinates(self, coords):
        """Актуализира координатите в основния прозорец."""
        lat, lon = coords
        self.coord_label.configure(text=f"Координати: {lat:.6f}, {lon:.6f}")
        self.lаt = lat
        self.lon = lon

    def search_event(self, event=None):
        address = self.entry.get()
        encoded_address = quote(address)  # Encode the address
        url = f"https://nominatim.openstreetmap.org/search?q={encoded_address}&format=jsonv2&addressdetails=1&limit=1"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = data[0]['lat']
                lon = data[0]['lon']
                self.map_widget.set_position(float(lat), float(lon))
            else:
                print("Address not found")
        else:
            print(f"Error: {response.status_code}")

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def calculate(self):
        """Пресмята нещо въз основа на въведените данни."""
        max_power = self.power_entry.get()
        dataframe = pd.DataFrame()
        dataframe = add_values_to_futher_dataframe(self.lаt, self.lon)
        dataframe.insert(0, 'Size', float(max_power))

        eval = get_elevation(self.lаt, self.lon)
        dataframe.insert(1, 'Elevation', eval)
        dataframe.drop(['date', 'time', 'Latitude', 'Longitude'], axis=1, inplace=True)
        model = tf.keras.models.load_model('the_best.h5')
        dataframe.fillna(0, inplace=True)
        
        # Debug print to check DataFrame values
        print("DataFrame before conversion to float32:")
        print(dataframe)

        self.power_for_the_next_16_days_label.configure(text="Изчисляване...", font=("Helvetica", 16))
        self.update_idletasks()  # Update the GUI to show the message
        dataframe_values = dataframe.values.astype('float32')
        
        real_powers = model.predict(np.squeeze(dataframe_values))
        sum_of_real_power = 0
        for i in range(0, len(real_powers)):
            sum_of_real_power += real_powers[i][0]

        self.power_for_the_next_16_days_label.configure(text=f"Сума на реалната мощност\nза следващите 16 дена:\n{sum_of_real_power/1000:.2f} kWh" , font=("Helvetica", 16))
        dataframe_from_the_last_year = pd.DataFrame()
        dataframe_from_the_last_year = add_values_to_climatic_data_frame_from_last_year(self.lаt, self.lon,0)
        dataframe_from_the_last_year.insert(0, 'Size', float(max_power))
        dataframe_from_the_last_year.insert(1, 'Elevation', eval)
        dataframe_from_the_last_year.drop(['date', 'time', 'Latitude', 'Longitude'], axis=1, inplace=True)
        dataframe_from_the_last_year.fillna(0, inplace=True, axis=1)
        real_powers = model.predict(dataframe_from_the_last_year.values.astype('float32'))
        sum_of_real_power = 0
        for i in range(0, len(real_powers)):
            sum_of_real_power += real_powers[i][0]

        self.power_from_last_year_label.configure(text=f"Сума на реалната мощност\nот 2024 до 2025 година:\n{sum_of_real_power/1000:.2f} kWh" , font=("Helvetica", 16))


        dataframe = pd.DataFrame()
        dataframe = add_values_to_climatic_data_frame_from_last_year(self.lаt, self.lon, 1)
        dataframe.insert(0, 'Size', float(max_power))
        dataframe.insert(1, 'Elevation', eval)
        dataframe.drop(['date', 'time', 'Latitude', 'Longitude'], axis=1, inplace=True)
        dataframe.fillna(0, inplace=True, axis=1)
        real_powers = model.predict(dataframe.values.astype('float32'))
        sum_of_real_power = 0
        for i in range(0, len(real_powers)):
            sum_of_real_power += real_powers[i][0]

        self.power_from_year_1_label.configure(text=f"Сума на реалната мощност\nот 2023 до 2024:\n{sum_of_real_power/1000:.2f} kWh" , font=("Helvetica", 16))

        dataframe = pd.DataFrame()
        dataframe = add_values_to_climatic_data_frame_from_last_year(self.lаt, self.lon, 2)
        dataframe.insert(0, 'Size', float(max_power))
        dataframe.insert(1, 'Elevation', eval)
        dataframe.drop(['date', 'time', 'Latitude', 'Longitude'], axis=1, inplace=True)
        dataframe.fillna(0, inplace=True, axis=1)
        real_powers = model.predict(dataframe.values.astype('float32'))
        sum_of_real_power = 0
        for i in range(0, len(real_powers)):
            sum_of_real_power += real_powers[i][0]

        self.power_from_year_2_label.configure(text=f"Сума на реалната мощност\nот 2022 до 2023:\n{sum_of_real_power/1000:.2f} kWh" , font=("Helvetica", 16))


    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
