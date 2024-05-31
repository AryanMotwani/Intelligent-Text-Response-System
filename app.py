from flask import Flask, render_template, request, jsonify
from web_ml_reply import response


app = Flask(__name__)


@app.get("/")
def get_html():
    return render_template("index.html")


@app.post("/reply")
def reply():
    text = request.get_json().get("message")
    answer = response(text)
    return answer
        

if __name__ =="__main__":
    app.run(debug=True)