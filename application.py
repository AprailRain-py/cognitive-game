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

    app_id = '6ff8d3c1'

    app_key = 'fdabfa4e797795d7f9294a40ee67d334'
    language = 'en'
    word_id = request.args.get('userInputCat')

    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + \
        language + '/' + word_id.lower() + '/synonyms;antonyms'
    # // url Normalized frequency
    # urlFR = 'https://od-api.oxforddictionaries.com:443/api/v1/stats/frequency/word/'  + language + '/?corpus=nmc&lemma=' + word_id.lower()

    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})

    # print("code {}\n".format(r.status_code))
    # print("text \n" + r.text)
    # print("json \n" + json.dumps(r.json()))

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

    # text = json.dumps(r.json())

    output = []
    print("*****")
    print(r)
    if r.status_code == 404:
        outputJquery = 0
    else:
        text = r.json()
        extractedWord = textChar(text)
        for i in extractedWord:
            if len(i.split(' ')) < 2:
                if i[0].lower() != 's':
                    output.append(i.lower())

        varRandom = random.randint(0, len(output))

        if len(output) == 1:
            outputJquery = output[0]
        else:
            outputJquery = output[varRandom]

    return jsonify(result=outputJquery)


if __name__ == '__main__':
    app.run(debug=True)
