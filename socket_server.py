import json
import logging
from flask import Flask, request, Response, make_response
app = Flask(__name__)

with open("level.txt", "r") as file:
    level = file.read()
if level == "INFO":
    logging.basicConfig(level=logging.INFO)
elif level == "WARNING":
    logging.basicConfig(level=logging.WARNING)
elif level == "ERROR":
    logging.basicConfig(level=logging.ERROR)
elif level == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)

dictionary = {}
@app.route('/', methods=['GET'])
def req_get():
    jameson = json.loads(request.data)
    key = jameson.get("key")
    if key is None:
        logging.error("Failed to find key in request body")
        return Response(status=400)
    else:
        dictionary_key = dictionary.get(key)
        if dictionary_key is None:
            logging.error("Failed to find messade for key '%s'", key)
            return Response(status=404)
        else:
            logging.debug("Successfully got message for key '%s'", key)
            return make_response({"message": dictionary_key}, 200)


@app.route('/', methods=['PUT'])
def req_put():
    jameson = json.loads(request.data)
    key = jameson.get("key")
    message = jameson.get("message")
    if key is None or message is None:
        logging.error("Failed to find key or message in request body")
        return Response(status=400)
    else:
        dictionary_key = dictionary.get(key)
        if dictionary_key is None:
            logging.error("Failed to find messade for key '%s' to update", key)
            return Response(status=404)
        else:
            logging.debug("Successfully put message for key '%s'", key)
            dictionary.update({key: message})
            return Response(status=200)


@app.route('/', methods=['POST'])
def req_post():
    jameson = json.loads(request.data)
    key = jameson.get("key")
    message = jameson.get("message")
    if key is None or message is None:
        logging.error("Failed to find key or message in request body")
        return Response(status=400)
    else:
        dictionary_key = dictionary.get(key)
        if dictionary_key is None:
            logging.debug("Successfully post message for key '%s'", key)
            dictionary.update({key: message})
            return make_response({"key": "value"}, 201)
        else:
            logging.error("Key '%s' has already been added", key)
            return Response(status=405)


@app.route('/', methods=['DELETE'])
def req_delete():
    jameson = json.loads(request.data)
    key = jameson.get("key")
    if key is None:
        logging.error("Failed to find key in request body")
        return Response(status=400)
    else:
        dictionary_key = dictionary.get(key)
        if dictionary_key is None:
            logging.error("Failed to find key '%s' in dictionary", key)
            return Response(status=204)
        else:
            logging.debug("Successfully delete message for key '%s'", key)
            dictionary.pop(key)
            return make_response({"message": dictionary_key}, 204)


if __name__ == '__main__':
    app.run()
