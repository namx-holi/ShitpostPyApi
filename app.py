#!venv/bin/python

from flask import Flask, jsonify, request
from generator import SentenceGenerator


app = Flask(__name__)
s = SentenceGenerator("Words")

@app.route("/")
def index():
	return "Hello, World"


@app.route("/shitpost", methods=["GET"])
def get_shitpost():
	count_str = request.args.get("count", "1")

	try:
		count = int(count_str)
	except ValueError:
		return jsonify({"error": "Invalid count. Must be int."})

	sentences = s.generate_sentences(count)
	return jsonify(sentences)


@app.route("/shitpost?n=<int:count>", methods=["GET"])
def get_shitposts(count):
	sentences = s.generate_sentences(count)
	return jsonify({"sentences": sentences})


if __name__ == "__main__":
	app.run(debug=True)
