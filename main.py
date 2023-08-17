from pymongo import MongoClient
from flask import Flask, request, abort

import os
import requests
import qrcode


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

@app.route("/", methods=['GET'])
def home():

    return 'Hello World'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)