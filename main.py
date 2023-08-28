from pymongo import MongoClient
from flask import Flask, request, abort, send_file, jsonify, send_from_directory, make_response
from PIL import Image
from flask_cors import CORS


import os
import io
import requests
import qrcode
import random
import json
import base64
import time

import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from io import BytesIO
import numpy as np



mdb_user = os.getenv('MONGODB_USERNAME')
mdb_pass = os.getenv('MONGODB_PASSWORD')
mdb_host = os.getenv('MONGODB_HOST')
mdb_dbs = os.getenv('MONGODB_DATABASE')

sd_host = 'http://192.168.0.106:3000'
sr_host = 'http://140.119.112.78:8828'

app = Flask(__name__, static_folder="/")
CORS(app)  # This will enable CORS for all routes

options_character = ["a female doll", "a male doll", "a female warrior", "a prince", 'a male doctor', "a female doctor", 'a cyberpunk samurai', 'a steampunk samurai', 'Margot Robbie', 'Anne Hathaway',
                'a princess", "a male mermaid', "a cyborg", "magician", 'steampunk doctor', 'an angel', 'a human with two horns','a vampire', 'a Frankenstein', 'Amber Heard', 'Thor', 'Loki',
                'a robot  with a human face"', "a fairy", "a male fairy", "a male astronaut", "a female astronaut", "a female steampunk inventor", "an elegant vampire", 'a evil vampire', 'Captain America',
                'a male steampunk inventor', "a crazy scientist", "a mafia man", "a space sailor", "an male engineer", "an female engineer", 'a rich man', 'a rich woman', 'Ryan Gosling', 'Avatar',
                'a male space farmer', "a female space farmer", "a time traveler", "a wizard", "a witch", "a male explorer", "a female explorer", 'a businessman', 'a businesswoman', 'Audrey Hepburn',
                'a cyborg bride', "a cyborg groom", "a barbie doll", "a Ken doll", 'A tree spirit with a human face', 'an alchemist', 'a super model', 'an emperor', 'a king', 'Godfather', 'Aquaman'
                'an ice mage', 'an artist','A monk', 'a human dragon rider ','a pirate','an assassin', 'a blacksmith', 'a human with Rabbit ears', 'a mayor', 'a queen', 'Willy Wonka', 'Johnny Depp',
                'a guardian','an earth guardian', 'a sky pirate', 'a drag queen','a sailor', 'a professor', 'a dictator', 'a soldier','a superhero', 'a president', 'a snow white', 'Angelina Jolie',
                'a medieval knight', 'a football player', 'a basketball player', 'a volleyball player', 'a singer', 'a gothic prince','a gothic princess', 'a character from the South Park', 'Hermione Granger',
                'a working class labor', 'Anya Taylor Joy', 'Andrew Scott', 'Andy Lau', 'a beautiful girl', 'a beautiful boy', 'a beautiful woman', 'a beautiful man', 'a cute boy', 'a cute girl', 'a Korean star',
                'a Kpop singer', 'a jpop singer', 'a cosplayer', 'an anime girl', 'a Japanese girl', 'a Korean man', 'a Korean girl', 'a stylish man', 'Freddie Mercury', 'Elton John', 'Mulan','Rapunzel',
                'Ron Weasley', 'Draco Malfoy','Dracula', 'Elon Musk','Mark Zuckerberg','Donald Trump','Hilary Clinton', 'Joe Biden', 'Alexander Hamilton', 'William Shakespeare', 'Prince Hamlet', 'kim Jong Un',
                'a dwarf', 'Wednesday Addams', 'a demon', 'Sherlock Holmes', 'James Moriarty', 'John Watson', 'Robert Oppenheimer', 'albert einstein', 'Confucius', 'James Bond','Sheldon Cooper', 'Elizabeth Bennet', 
                'Fitzwilliam Darcy', 'Jay Gatsby', 'Edmond Dantès', 'Scarlett OHara', 'Frank Sinatra', 'Severus Snape', 'the Hatter', 'Red Queen', 'Michael Scott', 'Dwight Schrute', 'Bruce Wayne', "Luke Skywalker",
                "Frodo Baggins", "Hermione Granger", "Darth Vader", "Katniss Everdeen", "Tony Stark (Iron Man)", "Princess Leia", "Winnie the Pooh", "Indiana Jones","Jack Sparrow", "Mickey Mouse", "Wonder Woman", 
                "Batman", "Superman", "Gandalf", "Spider-Man", "Black Widow", "Elsa", "Captain Jack Harkness", "Dobby the House Elf", "Mulan", "Hannibal Lecter", "Shrek", "Edward Scissorhands","Katniss Everdeen", 
                "Marty McFly", "John Wick", "Voldemort", "Forrest Gump", "James T. Kirk","Walter White", "Aragorn", "Gollum", "Dumbledore", 'Pete Mitchell', 'Ursula', "Maleficent", 'the Joker', "The Wicked Witch of the West",
                'Ip Man'
                    ]

options_location = ['in the forest', 'in front of a neon building', 'in the steampunk factory', 'in the heaven', 'in the hell', 'in the space ship', 'in the space', 'in the colorful barbie world', 'in food court', 'in a Mafia gun fight',
                    'in the magnificent palace','in front of a luxurious palace', 'in the dynamic ocean world', 'in the underground world', 'in the colorful aquarium', 'in a garden surrounded by alien plants', 'in Taroko canyon',
                    'in a space farm','in a snowy world', 'in fire world', 'in a ruin', 'in forest fire', "in front of a cyberpunk portal", 'on a music planet', 'in black hole', 'in a circus', 'in Liberty square', 'in huanted house',
                    'in a magic cave', 'in colorful galaxy', 'in front of a supernova', 'in northpole', 'in an ice palace', 'in a cybepunk city', 'in a steampunk city', 'in an exotic market place', 'in front of Taipei 101', 'in BLM protest', 
                    'a smoky dragon island', 'in Hogwarts', 'in front of an exploding nuclear bomb', "in a riot", 'in a battlefield', 'in pure chaos', 'in a desert', 'in an underground labyrinth', 'in a violent congress', 'in Hog Kong protest',
                    'in a stardust night', 'in the rain', 'in front a waterfall', 'a floating flower world', 'in a colorful crystal cave', 'in a volcano', 'in a sky city', 'in a bustling intersection', 'in Rome Senate', 'in Tiananmen Protest', 
                    'in a space train station', 'on a floating island', 'in  front of a tower that pierces the sky', 'in a shifting maze of corridors', 'in a grand library filled with endless shelves of magical tomes', 'in a laundry store',
                    'in a mystical mirror chamber',  'A bridge perched at the edge of the world', 'in a plateau covered in colorful crystalline formation', 'in a traveling carnival', ' in a magical cathedral', 'in Mcdonald', 'in a strike',
                    'in a desert oasis', 'an alien glade', 'in a digital democratic world', 'in a totalitarian world', 'in a Utopia', 'in an equal world', 'in a capitalist world', 'in a protest', 'in an democratic world', 'in Pride parade',
                    'in the middle of a riot', 'in a peace sit-in protest', 'in the crowded road', 'in an authoritarian state', 'on the volleyball court', 'in Chocolate factory', 'in a world made of candy', 'in a Post-apocalyptic world', 'in a nightmarket',
                    'in a gothic vampire castle', 'in a Cthulhu world', 'in Atlantis underwater world', 'in an arabian bazaar', 'in ancient Chinese palace', 'in Forbidden city', 'in front of Krusty Krab', 'in Japanese classroom', 'on a beach full of trash',
                    'in Asgard', 'in Orbit City', 'in Emerald City', 'in Hogsmeade Village', 'in Rivendell', 'in Shangri-La', 'in Tomorrowland', 'in Cloud City', 'in Gotham city', 'in Willy Wonka’s Factory', 'in front of The Gatsby Mansion',
                    'in the South park', 'in Lilliput','in Jurassic park','in Quahog', 'in Kowloon Walled city', 'a burning house', 'a digital democratic world', 'a communist world', 'in a theater', 'in Scotland', 'in Taiwan', 'in UFO', 'in Buckingham Palace',
                    'in NYSE', 'in a lab', 'in front of Doofenshimirtz Evil Co.', 'in Malibu beach', 'in Hollywood', 'in a kitchen', 'in a mining field', 'in a concert', 'in Times Sqaure', 'in Central Park', 'on The Millennium Falcon', "in Hawl's moving castle",
                    'at Niagara Falls', 'at Machu Picchu', 'at Venice Canals', 'at Pyramids of Giza', 'at The Burj Khalifa', 'at Taj Mahal', 'at Sydney Opera House', 'in front of Mount Fuji', "at St. Basil's Cathedral", 'at Neuschwanstein Castle',
                    'at Matterhorn', 'in a jungle village', 'in 1820 France ', 'at an Oceanic Abyss', 'in ancient Rome', 'in 1970s New York', 'in 1920s Chicago', 'in 1960s San Francisco', 'in a jazz club'
                    ]

def submit_post(url: str, data: dict):
    """
    Submit a POST request to the given URL with the given data.
    """
    return requests.post(url, data=json.dumps(data))

def image_to_base64(img: Image.Image, format: str = "PNG") -> str:
    buffered = io.BytesIO()
    img.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

@app.route("/get_qr", methods=['POST'])
def gen_qr():

    # print(request)
    jsonobj = request.get_json(silent=True)
    filename = json.dumps(jsonobj['filename']).replace("\"", "")

    # qnap_url = '{}/share.cgi/{}?ssid=2ae29aaac2164743a4fa9945859f3fa7&fid=2ae29aaac2164743a4fa9945859f3fa7&path=%2F&filename={}&openfolder=normal&ep='.format(sr_host, filename, filename)
    # qnap_url = '{}/share.cgi/{}?ssid=2ae29aaac2164743a4fa9945859f3fa7&fid=2ae29aaac2164743a4fa9945859f3fa7&path=%2Foutput&filename={}&openfolder=normal&ep='.format(sr_host, filename, filename)
    qnap_url = '{}/share.cgi/{}?ssid=5efda713c3554a7f80fbaec6b6c266fc&fid=5efda713c3554a7f80fbaec6b6c266fc&path=%2F&filename={}&openfolder=normal&ep='.format(sr_host, filename, filename)
    print(qnap_url)

    qr_img = qrcode.make(qnap_url)
    qr_img_base64 = image_to_base64(qr_img)

    # return send_file('qr_code.png', mimetype='image/png')

    res = dict()
    res['image'] = qr_img_base64
    res = make_response(jsonify(res), 200)

    return res

@app.route("/get_ai", methods=['POST'])
def gen_image():

    # print(request)
    jsonobj = request.get_json(silent=True)
    filename = json.dumps(jsonobj['filename']).replace("\"", "")


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
            'width': 512,
            'height': 512}

    sd_api_host = sd_host+'/sdapi/v1/txt2img'

    response = submit_post(sd_api_host, data)
    image_base64 = response.json()['images'][0]

    path = '../sd_image/'
    with open(path+filename, "wb") as image_file:
        image_file.write(base64.b64decode(image_base64))
    
    # return send_file('gen_image.png', mimetype='image/png')
    res = dict()
    res['image'] = image_base64
    res = make_response(jsonify(res), 200)

    return res

def gen_ai(filename):


    print('gen ai image')
    # choose a random 
    option1 = random.choice(options_character)
    option2 = random.choice(options_location)

    # replace string
    prompt = "raw photo, a person, half body portrait, in location, (medium shot, 10mm: 1.3), detailed background, facial detail, best quality"
    prompt = prompt.replace("a person", option1).replace("in location", option2)
    neg_prompt = "nude, (nsfw, deformed, distorted, disfigured:1.3), poorly drawn face, bad anatomy, wrong anatomy, extra limb, missing limb, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation. tattoo, watermark, text, anime, illustration, sketch, 3d, vector art, cartoon, painting, large breasts, blurry, depth of field, "

    # data = {"prompt": prompt,
    #         "negative_prompt": neg_prompt,
    #         "sampler_name": "DPM++ 2M Karras",
    #         "steps":60,
    #         "cfg_scale":8,
    #         "enable_hr":True,
    #         "denoising_strength": 0.7,
    #         "firstphase_width": 768,
    #         "firstphase_height": 512, 
    #         "hr_resize_x":1152,
    #         "hr_resize_y": 768,
    #         "hr_scale": 2,
    #         "hr_second_pass_steps": 30,
    #         "hr_upscaler":"SwinIR 4x",
    #         "seed": -1,
    #         "restore_faces": True,
    #         "width": 768,
    #         "height": 512}
    data_dict = dict()
    data_dict["prompt"]=prompt
    data_dict["negative_prompt"]=neg_prompt
    data_dict["sampler_name"]="DPM++ 2M Karras"
    data_dict["steps"]=60
    data_dict['cfg_scale']=8
    data_dict['enable_hr']=True
    data_dict['denoising_strength']= 0.7
    data_dict['firstphase_width']= 768
    data_dict['firstphase_height']= 512
    data_dict['hr_resize_x']=1152
    data_dict['hr_resize_y']= 768
    data_dict["hr_scale"]= 2
    data_dict["hr_second_pass_steps"]= 30
    # data_dict['hr_upscaler']='SwinIR 4x'
    data_dict['seed']= -1
    data_dict['restore_faces']= True
    data_dict['width']= 768
    data_dict['height']= 512
    data = data_dict

    sd_api_host = sd_host+'/sdapi/v1/txt2img'

    while True:

        try: 
            # print(sd_api_host)
            # print(data)

            response = submit_post(sd_api_host, data)

            print(response)
            image_base64 = response.json()['images'][0]

            app = FaceAnalysis(name='buffalo_l', root='./')
            app.prepare(ctx_id=0, det_size=(640, 640))
            faces = app.get(base64_string_2_np(image_base64))


            if len(faces) == 1:
                print('# of face equal to 1, ', end =" ")
                break

            elif (len(faces) == 1) and ('$error' not in json.loads(response.text)):
                print('no error occured in http request')
                break

            else:
                print('face not equal to 1 or error occured')
                time.sleep(5)

        except requests.ConnectionError:
            print("Received ConnectionError. Retrying...", end =" ")
            time.sleep(5)
            continue


    path = '../sd_image/'
    with open(path+filename, "wb") as image_file:
        image_file.write(base64.b64decode(image_base64))
    
    return image_base64

def gen_ai_v2(filename):
    print('gen ai image')
    # choose a random 
    option1 = random.choice(options_character)
    option2 = random.choice(options_location)

    # replace string
    prompt = "raw photo, a person, half body portrait, in location, (medium shot, 10mm: 1.3), detailed background, facial detail, best quality"
    prompt = prompt.replace("a person", option1).replace("in location", option2)
    neg_prompt = "nude, (nsfw, deformed, distorted, disfigured:1.3), poorly drawn face, bad anatomy, wrong anatomy, extra limb, missing limb, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation. tattoo, watermark, text, anime, illustration, sketch, 3d, vector art, cartoon, painting, large breasts, blurry, depth of field, "

    data_dict = dict()
    data_dict["prompt"]=prompt
    data_dict["negative_prompt"]=neg_prompt
    data_dict["sampler_name"]="DPM++ 2M Karras"
    data_dict["steps"]=60
    data_dict['cfg_scale']=8
    data_dict['enable_hr']=True
    data_dict['denoising_strength']= 0.7
    data_dict['firstphase_width']= 768
    data_dict['firstphase_height']= 512
    data_dict['hr_resize_x']=1152
    data_dict['hr_resize_y']= 768
    data_dict["hr_scale"]= 2
    data_dict["hr_second_pass_steps"]= 30
    # data_dict['hr_upscaler']='SwinIR 4x'
    data_dict['seed']= -1
    data_dict['restore_faces']= True
    data_dict['width']= 768
    data_dict['height']= 512
    data = data_dict

    sd_api_host = sd_host+'/sdapi/v1/txt2img'
    response = submit_post(sd_api_host, data)
    image_base64 = response.json()['images'][0]

    return image_base64

def gen_qr(filename):
    print('gen qr code')
    qnap_url = '{}/share.cgi/{}?ssid=2ae29aaac2164743a4fa9945859f3fa7&fid=2ae29aaac2164743a4fa9945859f3fa7&path=%2F&filename={}&openfolder=normal&ep='.format(sr_host, filename, filename)
    # print(qnap_url)

    qr_img = qrcode.make(qnap_url)
    qr_img_base64 = image_to_base64(qr_img)

    return qr_img_base64

def base64_string_2_np (base64_string):
    # Decode the base64 string
    image_bytes = base64.b64decode(base64_string)

    # Create a PIL Image object from the decoded string
    webcam_image = Image.open(BytesIO(image_bytes))

    webcam_np = np.array(webcam_image)
    webcam_np = webcam_np[:, :, :3]
    return webcam_np

def gen_wc (filename, webcam_image_string):
    wc_image_base64_string = webcam_image_string.replace("data:image/png;base64,", "")

    # print(webcam_image)
    # print(filename)

    path = '../sd_image/photo/'
    with open(path+filename, "wb") as image_file:
        image_file.write(base64.b64decode(wc_image_base64_string))

    return wc_image_base64_string

def face_swap (source_base64, target_base64):

    # source: webcam
    # target: ai image

    data = dict()
    data["source_image"] = source_base64
    data["target_image"] = target_base64
    data["face_index"] = [0]
    data["scale"] = 1
    data["upscale_visibility"] = 1
    data["face_restorer"] = "None"
    data["restorer_visibility"] = 1
    data["model"] = "inswapper_128.onnx"

    sd_api_host = sd_host+'/roop/image'
    response = submit_post(sd_api_host, data)
    output_base64 = response.json()['image']

    return output_base64


@app.route("/v2/submit", methods=['POST'])
def submit():
    # print(request)
    jsonobj = request.get_json(silent=True)
    filename = json.dumps(jsonobj['filename']).replace("\"", "")
    webcam_image_string = json.dumps(jsonobj['webcam_image']).replace("\"", "")

    # print(webcam_image)

    ai_image_base64_string = gen_ai(filename)
    wc_image_base64_string = gen_wc(filename, webcam_image_string)

    output_base64 = face_swap (wc_image_base64_string, wc_image_base64_string)

    # ai_image_np = base64_string_2_np(ai_image_base64_string)
    # wc_image_np = base64_string_2_np(wc_image_base64_string)

    res = dict()
    res['image'] = output_base64
    res = make_response(jsonify(res), 200)

    return res

    

@app.route("/submit", methods=['POST'])
def submit():

    # print(request)
    jsonobj = request.get_json(silent=True)
    filename = json.dumps(jsonobj['filename']).replace("\"", "")
    webcam_image_string = json.dumps(jsonobj['webcam_image']).replace("\"", "")

    # print(webcam_image)

    ai_image_base64_string = gen_ai(filename)
    wc_image_base64_string = gen_wc(filename, webcam_image_string)

    ai_image_np = base64_string_2_np(ai_image_base64_string)
    wc_image_np = base64_string_2_np(wc_image_base64_string)


    




    app = FaceAnalysis(name='buffalo_l', root='./')
    app.prepare(ctx_id=0, det_size=(640, 640))

    face_on_ai = app.get(ai_image_np)[0]
    face_on_wc = app.get(wc_image_np)[0]

    swapper = insightface.model_zoo.get_model('inswapper_128.onnx',
                                                download=False,
                                                download_zip=False)




    output = swapper.get(ai_image_np, face_on_ai, face_on_wc, paste_back=True)     
    # Convert ndarray to an Image object
    image = Image.fromarray(output)

    # Save the image
    image.save('../sd_image/output/'+filename)
    output_base64 = image_to_base64(image)



    res = dict()
    res['image'] = output_base64
    res = make_response(jsonify(res), 200)


    return res





@app.route('/')
def root():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=8000)
    app.run()