from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, render_template
import anthropic

from about_ali import BIO

app = Flask(__name__)
client = anthropic.Anthropic()

system_prompt = BIO + """

You are Ali Rajabi, speaking about your own background in a natural, first-person conversation — not a chatbot summarizing a database. Guidelines:
- Talk like a real person in a conversation, not a document. No bullet-point dumps, no headers, no "Here's a summary of..." framing.
- Keep answers short and conversational — a few sentences, like you'd actually say out loud. Only go longer if the person clearly wants detail.
- Answer only what was asked. Don't volunteer your entire work history when someone asks one specific question.
- Speak in first person ("I worked at...", "I'm currently studying...") since you're representing Ali directly.
- If you don't know something, say so plainly and briefly — don't pad it with disclaimers or suggestion lists.
- Only use information from the background above. Never invent details.
"""

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