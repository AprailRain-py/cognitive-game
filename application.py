import requests
import json
import random

from flask import Flask, render_template, request, jsonify

application = app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=["GET"])
def extractUserInput():
    text = request.form["userInput"]
    return render_template("index.html", text=text)


@app.route('/result')
def compResult():

    word_id = request.args.get('userInputCat')

    # new URL
    url = 'https://relatedwords.org/api/related?term=' + word_id.lower()

    r = requests.get(url, headers={})

    # Old Fn for converting text into data
    def textChar(dc):
        allWord = []
        for z in range(0, len(dc['results'][0]["lexicalEntries"])):
            t2 = dc["results"][0]["lexicalEntries"][z]["entries"][0]["senses"]
            for i in t2:
                if isinstance(i, dict):
                    for k, v in i.items():
                        if isinstance(v, list):
                            for s in v:
                                if isinstance(s, dict):
                                    for vk, vv in s.items():
                                        if isinstance(vv, list):
                                            for g in vv:
                                                if isinstance(g, dict):
                                                    for p, a in g.items():
                                                        if p == "text":
                                                            allWord.append(
                                                                g[p])
                                                else:
                                                    allWord.append(g)
                                        else:
                                            if vk == "text":
                                                allWord.append(vv)
        return allWord

    output = []

    if r.status_code == 404:
        outputJquery = 0
    else:
        text = r.json()
        for i in text[0:10]:
            if i['word'][0].lower() != 's':
                output.append(i['word'].lower())

        varRandom = random.randint(0, len(output))

        if len(output) == 1:
            outputJquery = output[0]
        else:
            outputJquery = output[varRandom]

    return jsonify(result=outputJquery)


if __name__ == '__main__':
    app.run(debug=True)
