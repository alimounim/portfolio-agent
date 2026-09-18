from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, render_template, session
import anthropic
import secrets

from about_ali import BIO

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
client = anthropic.Anthropic()

system_prompt = BIO + """

You are Ali Rajabi, speaking about your own background in a natural, first-person conversation — not a chatbot summarizing a database. Guidelines:
- Talk like a real person in a conversation, not a document. No headers, no "Here's a summary of..." framing.
- Keep answers short and conversational — a few sentences, like you'd actually say out loud. Only go longer if the person clearly wants detail.
- When listing multiple items (courses, certifications, projects, skills), use a markdown bullet list (lines starting with "- ") so it's easy to scan.
- Answer only what was asked. Don't volunteer your entire work history when someone asks one specific question.
- Speak in first person ("I worked at...", "I'm currently studying...") since you're representing Ali directly.
- If you don't know something, say so plainly and briefly — don't pad it with disclaimers or suggestion lists.
- Only use information from the background above. Never invent details.
"""

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/projects")
def projects():
	return render_template("projects.html")

@app.route("/certifications")
def certifications():
	return render_template("certifications.html")

@app.route("/research")
def research():
	return render_template("research.html")

conversations = {} # dict: {session_id: [messages...]} — each visitor gets their own history

@app.route("/chat", methods=["POST"])
def chat(): 
	if "session_id" not in session:
		session["session_id"] = secrets.token_hex(8)

	sid = session["session_id"]
	if sid not in conversations:
		conversations[sid] = []

	history = conversations[sid]

	data = request.get_json()
	user_message = data.get("message")

	history.append({"role": "user", "content": user_message})

	response = client.messages.create(
		model = "claude-sonnet-4-6",
		max_tokens = 300,
		system = system_prompt,
		messages =history
	)

	reply = response.content[0].text
	history.append({"role": "assistant", "content": reply})

	return jsonify({"reply":reply})

if __name__=="__main__":
	app.run(debug=True, port=5000)