#!/usr/bin/python
#coding:utf-8
# import base64
import base64
import json
from requests import Request, Session
import numpy as np
from private import KEY
 
 
def recognize_captcha(str_image_path):
    # bin_captcha = open(str_image_path, 'rb').read()
    # print(bin_captcha)
    # str_encode_file = base64.b64encode(bin_captcha)
    # print(str_encode_file)

    with open(str_image_path, 'rb') as open_file:
        byte_content = open_file.read()
    base64_bytes = base64.b64encode(byte_content)
    str_encode_file = base64_bytes.decode('utf-8')

    str_url = "https://vision.googleapis.com/v1/images:annotate?key="

    str_api_key = KEY

    str_headers = {'Content-Type': 'application/json'}

    str_json_data = {
        'requests': [
            {
                'image': {
                    'content': str_encode_file
                },
                'features': [
                    {
                        'type': "TEXT_DETECTION",
                        'maxResults': 10
                    }
                ]
            }
        ]
    }

    # print("begin request")
    obj_session = Session()
    obj_request = Request("POST",
                          str_url + str_api_key,
                          data=json.dumps(str_json_data),
                          headers=str_headers
                          )
    obj_prepped = obj_session.prepare_request(obj_request)
    obj_response = obj_session.send(obj_prepped,
                                    verify=True,
                                    timeout=60
                                    )
    # print("end request")

    if obj_response.status_code == 200:
        # print(obj_response.text)
        with open('data.json', 'w') as outfile:
            json.dump(obj_response.text, outfile)
        return obj_response.text
    else:
        return "error"


def formatJson(strings):
    weather_dict = json.loads(strings)
    weather_format_json = json.dumps(weather_dict, indent=4, separators=(',', ': '))
    return weather_format_json


def searchStrings(strings, imageFile, flagDebug=False):
    recognize_captcha(imageFile)
    # result = formatJson(strings)
    # print(result)

    result = []

    a = open('data.json', 'r')
    b = json.load(a)
    raw = json.loads(b)
    # print("raw.keys : ", raw.keys())
    responses = raw['responses'][0]
    # print("len(responses) : ", len(responses))
    # print("responses.keys : ", responses.keys())

    fullTextAnnotation = responses['fullTextAnnotation']
    # print("fullTextAnnotation.keys : ", fullTextAnnotation.keys())
    pages = fullTextAnnotation['pages']
    text = fullTextAnnotation['text']

    textAnnotations = responses['textAnnotations']
    # print("len(textAnnotation) : ", len(textAnnotations))
    # print("textAnnotations[0].keys : ", textAnnotations[0].keys())
    for i in range(1, len(textAnnotations)):
        # print("textAnnotations[" + str(i) + "] : ", textAnnotations[i])
        # print("textAnnotations[" + str(i) + "].keys : ", textAnnotations[i].keys())
        description = textAnnotations[i]['description']
        if flagDebug:
            print("description : ", i, description)

        boundingPoly = textAnnotations[i]['boundingPoly']
        # print("boundingPoly.keys : ", i, boundingPoly.keys())
        vertices = boundingPoly['vertices']
        # print("vertices : ", i, vertices)
        upperRight = vertices[0]
        lowerRight = vertices[1]
        upperLeft = vertices[2]
        lowerLeft = vertices[3]
        # print(upperRight, lowerRight, upperLeft, lowerLeft)

        if strings in description:
            # result.append(vertices)
            up = vertices[0]['y']
            down = vertices[2]['y']
            left = vertices[0]['x']
            right = vertices[2]['x']
            result.append([[left, up], [right, down]])
            break
    result = np.asarray(result)
    return result

 
if __name__ == '__main__':
    strings = u"しゅうかく"
    imageFile = "screenshot.png"
    result = searchStrings(strings, imageFile, flagDebug=True)
    # print(result)
