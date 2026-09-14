from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, render_template
import anthropic


app = Flask(__name__)
client = anthropic.Anthropic()

system_prompt = "You are an assistant representing Ali Rajabi, a data science graduate student at UT Arlington with a background in IT infrastructure and financial services. Courses I have taken so far are Foundations of Computing, Foundations of Data Science, Statistics and Probability, Machine Learning, Big Data Management, Data Visualizations. Answer questions about their background accurately and concisely."

@app.route("/")
def home():
	return render_template("index.html")

conversation_history = [] # lives outside the route function, persists between requests

@app.route("/chat", methods=["POST"])

def chat():
	data = request.get_json()
	user_message = data.get("message")

	conversation_history.append({"role": "user", "content": user_message})

	response = client.messages.create(
		model = "claude-sonnet-4-6",
		max_tokens = 300,
		system = system_prompt,
		messages =conversation_history
	)

	reply = response.content[0].text
	conversation_history.append({"role": "assistant", "content": reply})

	return jsonify({"reply":reply})

if __name__=="__main__":
	app.run(debug=True, port=5000)