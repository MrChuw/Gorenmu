# Translation for Weather
Weather-city_not_passed = No city saved or sent, use { $prefix }savecity (city) (hide:true to hide the city) to save a city.
Weather-no_weather_found = Weather not found for "{ $name }".
Weather-user_has_no_city = User { $name } has no saved city.
Weather-city_not_found = city "{ $city }" not found.
Weather-hidden = (Hidden location)

Weather-weather_wind_direction =
    .n = N, north
    .ne = NE, north-east
    .l = E, east
    .se = SE, south-east
    .s = S, south
    .so = SW, south-west
    .o = W, west
    .no = NW, north-west

Weather-weather_display = { $city }. { $desc } { $emoji }, temperature of { $temp } { $u_temp }, maximum of { $max } { $u_temp } and apparent temperature of { $app } { $u_temp }, { $press } { $u_press }, { $hum }{ $u_hum }, { $wind_spd }{ $u_wind_spd } { $wind_dir }{ $precip }

Weather-weather_strings =
    .precip = , and precipitation of { $val } { $u_precip }

Weather-deco_helper = Enter the command and a city to get the weather forecast.
Weather-deco_usage = To use: { $prefix }weather (location)
Weather-deco_description = Enter the command and a city to get the weather forecast.

# Commands
Weather-cmd_ex1_args = wt fortaleza
Weather-cmd_ex1_res = Fortaleza, Ceará, Brazil. Cloudy ☁️ , temperature of 26.5 °C, maximum of 32.7 °C and apparent temperature of 30.4 °C, 1011.4 hPa, 79%, 7.6km/h east
Weather-cmd_ex2_args = wt georgia, georgia
Weather-cmd_ex2_res = Georgia, Georgia. Cloudy ☁️ , temperature of -3.8 °C, maximum of -2.4 °C and apparent temperature of -6.7 °C, 1023.4 hPa, 93%, 2.1km/h north-west
Weather-cmd_ex3_args = wt 61700-000
Weather-cmd_ex3_res = 61700-000, Aquiraz, Ceará, Brazil. Cloudy ☁️ , temperature of 25.6 °C, maximum of 32.6 °C and apparent temperature of 30.2 °C, 1011.5 hPa, 83%, 4.6km/h north-east
Weather-cmd_ex4_args = wt Vicolo di Cecilio Giocondo, 2, 80045 Pompei NA, Italy
Weather-cmd_ex4_res = Vicolo di Cecilio Giocondo, Pompei, Campania, Italy. Partly cloudy ⛅ , temperature of 13.9 °C, maximum of 15.3 °C and apparent temperature of 12.3 °C, 1020.1 hPa, 58%, 6.6km/h north-east
Weather-cmd_ex5_prefix = Locations can be hidden.
Weather-cmd_ex5_args = wt
Weather-cmd_ex5_res = (Hidden location) Clear 🌙 , temperature of 1.5 °C, maximum of 6.9 °C and apparent temperature of -3.0 °C, 1017.1 hPa, 45%, 8.4km/h north-west

# Admonitions
Weather-adm_title1 = Set city
Weather-adm_msg1 = You can use /whisper gorenmu +set city (city name) to save a city without needing to send a message in the chat.
Weather-adm_title2 = Hide location.
Weather-adm_msg2 = By default, the city will be saved as hidden when using { $prefix }set city (city name). Add "hidden:false" to show in the chat.
