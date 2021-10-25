# -*- coding: utf-8 -*-
import random, math
from somali.data.scp import get_random_number
from somali import config

aliases=['rmap']
description = f'Vai mandar um lugar aleatorio do mapa, devido a "problemas" pode ser que caia no meio do mar então é so ir para a costa mais proxima que é a localização real.'
usage = 'digite o comando, "rmapa".'


async def command(ctx,) -> None:
    count = 0
    # lagitude = random.uniform(-90, 90)
    # longitude = random.uniform(-180, 180)
    # # r = f'https://www.google.com.br/maps/@{lagitude},{longitude},15z'
    with open('/home/pi/Botos/Oboto/somali/data/cidades.csv') as fr: 
        lines = fr.readlines() 
        random_line = random.choice(lines) if lines else None 

    circle_x, circle_y = random_line.split(",", 1)
    circle_x = float(circle_x.replace('"',""))
    circle_y = float(circle_y.replace('"',""))
    print(circle_x, circle_y) 


    if -160 < circle_x and circle_y  < 160:
        # radius of the circle
        circle_r = 20

        # random angle
        alpha = 2 * math.pi * random.random()
        # random radius
        r = circle_r * math.sqrt(random.random())
        # calculating coordinates
        x = r * math.cos(alpha) + circle_x
        y = r * math.sin(alpha) + circle_y
        ctx.response = f'FBBlock https://www.google.com.br/maps/@{x},{y},15z'

    elif -170 < circle_x and circle_y < 170:
        # radius of the circle
        circle_r = 9

        # random angle
        alpha = 2 * math.pi * random.random()
        # random radius
        r = circle_r * math.sqrt(random.random())
        # calculating coordinates
        x = r * math.cos(alpha) + circle_x
        y = r * math.sin(alpha) + circle_y
        ctx.response = f'FBBlock https://www.google.com.br/maps/@{x},{y},15z'


    elif -179 < circle_x and circle_y < 179:
        # radius of the circle
        circle_r = 0.4

        # random angle
        alpha = 2 * math.pi * random.random()
        # random radius
        r = circle_r * math.sqrt(random.random())
        # calculating coordinates
        x = r * math.cos(alpha) + circle_x
        y = r * math.sin(alpha) + circle_y
        ctx.response = f'FBBlock https://www.google.com.br/maps/@{x},{y},15z'


    elif -180 < circle_x and circle_y < 180:
        # radius of the circle
        circle_r = 0.4

        # random angle
        alpha = 2 * math.pi * random.random()
        # random radius
        r = circle_r * math.sqrt(random.random())
        # calculating coordinates
        x = r * math.cos(alpha) + circle_x
        y = r * math.sin(alpha) + circle_y
        ctx.response = f'FBBlock https://www.google.com.br/maps/@{x},{y},15z'


    else:
        # radius of the circle
        circle_r = 0.4

        # random angle
        alpha = 2 * math.pi * random.random()
        # random radius
        r = circle_r * math.sqrt(random.random())
        # calculating coordinates
        x = r * math.cos(alpha) + circle_x
        y = r * math.sin(alpha) + circle_y
        ctx.response = f'FBBlock https://www.google.com.br/maps/@{x},{y},15z'

    count += 1


