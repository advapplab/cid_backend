# cid_backend


ONNX Model: https://drive.google.com/file/d/1krOLgjW2tAPaqV-Bw4YALz0xT5zlb5HF/view

Realistic Vision v5.1: https://huggingface.co/stablediffusionapi/realistic-vision-v51

docker run -p 8829:8080 -v /home/owen/workspace_ext/cid/:/webapps/ -v /home/owen/workspace_ext/sd_image/:/sd_image/ -d --rm --name cid -it cfleu198/cid_api 
