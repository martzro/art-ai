from diffusers import StableDiffusionPipeline
import torch
import flask
import os
import uuid
import requests

app = flask.Flask(__name__)


@app.route('/textToImage', methods=["POST"])
def return_id_generate_image():
    """
    Generate image from text
    :return: image is as a string for the user to look up and retrieve
    """
    prompt = flask.request.form.get("text")
    _id = str(uuid.uuid1())
    url, data = ["http://172.16.20.139:5000/makeImage", {"prompt": str(prompt), "id": _id}]
    requests.post(url, data)

    return _id


@app.route('/makeImage', methods=["POST"])
def makeImage():
    """
    Make image from text and save using id
    :return:
    """
    prompt = flask.request.form.get("prompt")
    file_name = flask.request.form.get("id") + ".jpg"
    pipeline = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5",
                                                       torch_dtype=torch.float16,
                                                       safety_checker=None)
    pipeline.to("cuda")
    image = pipeline(prompt).images[0]
    image.save(file_name)
    return


@app.route('/getImage', methods=["POST"])
def check_if_ready():
    """
    Function for user to check if image is done. If done then the image is returned as bytes
    :return: image as bytes
    """
    _id = flask.request.form.get("id")
    if os.path.isfile(f"{_id}.jpg"):
        image = open(f"{_id}.jpg", "rb").read()
        return image
    else:
        return str(400)


if __name__ == '__main__':
    app.run(host='172.16.20.139', port=5000, debug=True, threaded=True)
