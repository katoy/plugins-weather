import json
import requests
import urllib.parse

import quart
import quart_cors
from quart import request


def get_weather(lat, lon):
    # See 
    # https://open-meteo.com/en/docs
    url = f"https://api.open-meteo.com/v1/jma?current_weather=true&latitude={lat}&longitude={lon}"
    # &hourly=temperature_2m,relativehumidity_2m"
    response = requests.get(url)
    data = response.json()
    return data


# Note: Setting CORS to allow chat.openapi.com is only required when running a localhost plugin
app = quart_cors.cors(quart.Quart(__name__),
                      allow_origin="https://chat.openai.com")


@app.route('/weather', methods=['GET'])
async def weather():
    lat = request.args.get("latitude")
    lon = request.args.get("longitude")
    result = get_weather(lat, lon)
    return result


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open(".well-known/ai-plugin.json") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the manifest
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        # This is a trick we do to populate the PLUGIN_HOSTNAME constant in the OpenAPI spec
        text = text.replace("PLUGIN_HOSTNAME", f"https://{host}")
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()
