import requests
import json

token = 'qnVfXxPZmzZYahgI'
server_url = 'http://34.71.138.79:9090'

def model_stealing_submission(path_to_onnx_file: str):
    SERVER_URL = server_url
    ENDPOINT = "/modelstealing/submit"
    URL = SERVER_URL + ENDPOINT

    TEAM_TOKEN = token

    with open(path_to_onnx_file, "rb") as onnx_file:
        response = requests.post(
            URL, files={"file": onnx_file}, headers={"token": TEAM_TOKEN}
        )

        if response.status_code == 200:
            return response.content["score"]
        else:
            raise Exception(f"Request failed. Status code: {response.status_code}, content: {response.content}")
        
def model_stealing(path_to_png_file: str):
    SERVER_URL = server_url
    ENDPOINT = "/modelstealing"
    URL = SERVER_URL + ENDPOINT

    TEAM_TOKEN = token

    with open(path_to_png_file, "rb") as img_file:
        response = requests.get(
            URL, files={"file": img_file}, headers={"token": TEAM_TOKEN}
        )
        if response.status_code == 200:
            decoded_string = response.content.decode('utf-8')
            data = json.loads(decoded_string)
            return data['representation']
        else:
            raise Exception(f"Request failed. Status code: {response.status_code}, content: {response.content}")

# def model_stealing_reset():
#     SERVER_URL = server_url
#     ENDPOINT = "/modelstealing/reset"
#     URL = SERVER_URL + ENDPOINT

#     TEAM_TOKEN = "[paste your team token here]"

#     response = requests.post(
#         URL, headers={"token": TEAM_TOKEN}
#     )

#     if response.status_code == 200:
#         print("Endpoint rested successfully")
#     else:
#         raise Exception(f"Request failed. Status code: {response.status_code}, content: {response.content}")
        