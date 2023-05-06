import urllib

BASE_URL = "https://latex.codecogs.com/svg.image"


def get_image_url(equation):
    return f"{BASE_URL}?{encode_equation(equation)}"


def encode_equation(equation):
    return urllib.parse.quote(rf"{equation}")
