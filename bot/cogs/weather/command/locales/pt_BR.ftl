# Translation for Weather
Weather-city_not_passed = Nenhuma cidade salva ou enviada, use { $prefix }savecity (cidade) (hide:true para esconder a cidade) para salvar uma cidade.
Weather-no_weather_found = Não foi encontrado o tempo para "{ $name }".
Weather-user_has_no_city = Usuário { $name } não tem cidade salva.
Weather-city_not_found = cidade "{ $city }" não encontrada.
Weather-hidden = (Localização escondida)

Weather-weather_wind_direction =
    .n = N, norte
    .ne = NE, nordeste
    .l = L, leste
    .se = SE, sudeste
    .s = S, sul
    .so = SO, sudoeste
    .o = O, oeste
    .no = NO, noroeste

Weather-weather_display = { $city }. { $desc } { $emoji }, temperatura de { $temp } { $u_temp }, máxima de { $max } { $u_temp } e aparente de { $app } { $u_temp }, { $press } { $u_press }, { $hum }{ $u_hum }, { $wind_spd }{ $u_wind_spd } { $wind_dir }{ $precip }

Weather-weather_strings =
    .precip = , e precipitação de { $val } { $u_precip }

Weather-deco_helper = Digite o comando e uma cidade para obter a previsão do tempo.
Weather-deco_usage = Para usar: { $prefix }weather (localização)
Weather-deco_description = Digite o comando e uma cidade para obter a previsão do tempo.

# Commands
Weather-cmd_ex1_args = wt fortaleza
Weather-cmd_ex1_res = Fortaleza, Ceará, Brazil. Nublado ☁️ , temperatura de 26.5 °C, máxima de 32.7 °C e aparente de 30.4 °C, 1011.4 hPa, 79%, 7.6km/h leste
Weather-cmd_ex2_args = wt georgia, georgia
Weather-cmd_ex2_res = Georgia, Georgia. Nublado ☁️ , temperatura de -3.8 °C, máxima de -2.4 °C e aparente de -6.7 °C, 1023.4 hPa, 93%, 2.1km/h noroeste
Weather-cmd_ex3_args = wt 61700-000
Weather-cmd_ex3_res = 61700-000, Aquiraz, Ceará, Brazil. Nublado ☁️ , temperatura de 25.6 °C, máxima de 32.6 °C e aparente de 30.2 °C, 1011.5 hPa, 83%, 4.6km/h nordeste
Weather-cmd_ex4_args = wt Vicolo di Cecilio Giocondo, 2, 80045 Pompei NA, Itália
Weather-cmd_ex4_res = Vicolo di Cecilio Giocondo, Pompei, Campania, Italy. Parcialmente nublado ⛅ , temperatura de 13.9 °C, máxima de 15.3 °C e aparente de 12.3 °C, 1020.1 hPa, 58%, 6.6km/h nordeste
Weather-cmd_ex5_prefix = As localizações podem ser ocultadas.
Weather-cmd_ex5_args = wt
Weather-cmd_ex5_res = (Localização oculta) Limpo 🌙 , temperatura de 1.5 °C, máxima de 6.9 °C e aparente de -3.0 °C, 1017.1 hPa, 45%, 8.4km/h noroeste

# Admonitions
Weather-adm_title1 = Definir cidade
Weather-adm_msg1 = Você pode usar /whisper gorenmu +set city (nome da cidade) para salvar uma cidade sem precisar enviar uma mensagem no chat.
Weather-adm_title2 = Ocultar localização
Weather-adm_msg2 = Por padrão, a cidade será salva como oculta ao usar { $prefix }set city (nome da cidade). Adicione "hidden:false" para exibir no chat.
