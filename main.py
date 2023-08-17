from pymongo import MongoClient
from flask import Flask, request, abort, send_file, jsonify
from PIL import Image

import os
import io
import requests
import qrcode
import random
import json
import base64

mdb_user = os.getenv('MONGODB_USERNAME')
mdb_pass = os.getenv('MONGODB_PASSWORD')
mdb_host = os.getenv('MONGODB_HOST')
mdb_dbs = os.getenv('MONGODB_DATABASE')

sd_host = os.getenv('SD_HOST')

app = Flask(__name__)

options_character = ["a female doll", "a male doll", "a female warrior", "a prince", 'a male doctor', "a female doctor", 'a cyberpunk samurai', 'a steampunk samurai', 'Margot Robbie', 'Anne Hathaway',
                "a princess", "a male mermaid", "a cyborg", "magician", 'steampunk doctor', 'an angel', 'a human with two horns','a vampire', 'a Frankenstein', 'Amber Heard', 'Thor', 'Loki',
                "a robot  with a human face", "a fairy", "a male fairy", "a male astronaut", "a female astronaut", "a female steampunk inventor", "an elegant vampire", 'a evil vampire', 'Captain America',
                "a male steampunk inventor", "a crazy scientist", "a mafia man", "a space sailor", "an male engineer", "an female engineer", 'a rich man', 'a rich woman', 'Ryan Gosling', 'Avatar',
                "a male space farmer", "a female space farmer", "a time traveler", "a wizard", "a witch", "a male explorer", "a female explorer", 'a businessman', 'a businesswoman', 'Audrey Hepburn',
                    "a cyborg bride", "a cyborg groom", "a barbie doll", "a Ken doll", 'A tree spirit with a human face', 'an alchemist', 'a super model', 'an emperor', 'a king', 'Godfather', 'Aquaman'
                "an ice mage", 'an artist','A monk', 'a human dragon rider ','a pirate','an assassin', 'a blacksmith', 'a human with Rabbit ears', 'a mayor', 'a queen', 'Willy Wonka', 'Johnny Depp',
                'a guardian','an earth guardian', 'a sky pirate', 'a drag queen','a sailor', 'a professor', 'a dictator', 'a soldier','a superhero', 'a president', 'a snow white', 'Angelina Jolie',
                'a medieval knight', 'a football player', 'a basketball player', 'a volleyball player', 'a singer', 'a gothic prince','a gothic princess', 'a character from the South Park', 'Hermione Granger',
                'a working class labor', 'Anya Taylor Joy']

options_location = ['in the forest', 'in front of a neon building', 'in the steampunk factory', 'in the heaven', 'in the hell', 'in the space ship', 'in the space', 'in the colorful barbie world',
                    'in the magnificent palace','in front of a luxurious palace', 'in the dynamic ocean world', 'in the underground world', 'in the colorful aquarium', 'in a garden surrounded by alien plants', 
                    'in a space farm','in a snowy world', 'in fire world', 'in a ruin', 'in forest fire', "in front of a cyberpunk portal", 'on a music planet', 'in black hole', 'in a circus', 'in Liberty square',
                    'in a magic cave', 'in colorful galaxy', 'in front of a supernova', 'in northpole', 'in an ice palace', 'in a cybepunk city', 'in a steampunk city', 'in an exotic market place', 'in front of Taipei 101',
                    'a smoky dragon island', 'in Hogwarts', 'in front of an exploding nuclear bomb', "in a riot", 'in a battlefield', 'in pure chaos', 'in a desert', 'in an underground labyrinth', 'in a violent congress'
                    'in a stardust night', 'in the rain', 'in front a waterfall', 'a floating flower world', 'in a colorful crystal cave', 'in a volcano', 'in a sky city', 'in a bustling intersection', 'in Rome Senate',
                    'in a space train station', 'on a floating island', 'in  front of a tower that pierces the sky', 'in a shifting maze of corridors', 'in a grand library filled with endless shelves of magical tomes',
                    'in a mystical mirror chamber',  'A bridge perched at the edge of the world', 'in a plateau covered in colorful crystalline formation', 'in a traveling carnival', ' in a magical cathedral',
                    'in a desert oasis', 'an alien glade', 'in a digital democratic world', 'in a totalitarian world', 'in a Utopia', 'in an equal world', 'in a capitalist world', 'in a protest', 'in an democratic world',
                    'in the middle of a riot', 'in a peace sit-in protest', 'in the crowded road', 'in an authoritarian state', 'on the volleyball court', 'in Chocolate factory', 'in a world made of candy', 'in a Post-apocalyptic world',
                    'in a gothic vampire castle', 'in a Cthulhu world', 'in Atlantis underwater world', 'in an arabian bazaar', 'in ancient Chinese palace', 'in Forbidden city', 'in front of Krusty Krab', 'in Japanese classroom',
                    'in Asgard', 'in Orbit City', 'in Emerald City', 'in Hogsmeade Village', 'in Rivendell', 'in Shangri-La', 'in Tomorrowland', 'in Cloud City', 'in Gotham city', 'in Willy Wonka’s Factory', 'in front of The Gatsby Mansion',
                    'in the South park', 'in Lilliput','in Jurassic park','in Quahog', 'in Kowloon Walled city', 'a burning house', 'a digital democratic world', 'a communist world'
                ]

def submit_post(url: str, data: dict):
    """
    Submit a POST request to the given URL with the given data.
    """
    return requests.post(url, data=json.dumps(data))

@app.route("/", methods=['GET'])
def home():

    # QR Code
    qr_img = qrcode.make('http://')
    # qr_img.save('qr_code.png', 'PNG')

    buffered = io.BytesIO()
    qr_img.save(buffered, format="JPEG")  # You can change format to PNG or other file types
    qr_img_base64 = base64.b64encode(buffered.getvalue())






    # choose a random 
    option1 = random.choice(options_character)
    option2 = random.choice(options_location)

    # replace string
    prompt = "in location, a person, alone, facing the camera, solo, skin detail, face detail, Taiwanese, raw photo ,8K HDR, hyper-realistic, half body shot, hyper detailed, cinematic lighting"
    prompt = prompt.replace("a person", option1).replace("in location", option2)
    neg_prompt = "nsfw, nude, censored, ((duplication)), more than one person, text, watermark, blurry background, naked, half naked, topless, wearing underwear, showing thighs, showing chest, deformed iris, deformed pupils, out of frame, cropped, not wearing pants,semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation, worst quality, normal quality, low quality, low res, blurry, text, watermark, logo, banner, extra digits, cropped, jpeg artifacts, signature, username, error, sketch ,duplicate, ugly, monochrome, horror, geometry, mutation, disgusting, bad anatomy, bad hands, three hands, three legs, bad arms, missing legs, missing arms, poorly drawn face, bad face, fused face, cloned face, worst face, three crus, extra crus, fused crus, worst feet, three feet, fused feet, fused thigh, three thigh, fused thigh, extra thigh, worst thigh, missing fingers, extra fingers, ugly fingers, long fingers, horn, extra eyes, huge eyes, 2girl, amputation, disconnected limbs, cartoon, cg, 3d, unreal, animate"


    data = {'prompt': prompt,
            "negative_prompt": neg_prompt,
            "sampler_name": "DPM++ 2M Karras",
            'width': 32,
            'height': 32}

    response = submit_post(sd_host, data)
    image_base64 = response.json()['images'][0]

    with open('gen_image.png', "wb") as image_file:
        image_file.write(base64.b64decode(image_base64))






    return_dict = dict()
    return_dict['image'] = image_base64
    return_dict['qr'] = qr_img_base64  
    # print(return_dict)

    # return_json = jsonify(return_dict)
    # print(return_json)


    return return_dict
    # return send_file('gen_image.png', mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)