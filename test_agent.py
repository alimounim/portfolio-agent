from dotenv import load_dotenv
load_dotenv()

import anthropic

client = anthropic.Anthropic()

system_prompt = "You are an assistant representing Ali Rajabi, a data science graduate student at UT Arlington with a background in IT infrastructure and financial services. Courses I have taken so far are Foundations of Computing, Foundations of Data Science, Statistics and Probability, Machine Learning, Big Data Management, Data Visualizations. Answer questions about their background accurately and concisely."

messages = [] # this will hold the conversation history. 

while True:
	user_input = input("You: ")

	if user_input == "quit":
		break

	messages.append({"role": "user", "content": user_input})

	response = client.messages.create(
		model = "claude-sonnet-4-6",
		max_tokens = 300,
		system = system_prompt,
		messages = messages
	)
	
	reply = response.content[0].text
	print(f"Claude: {reply}")

	messages.append({"role": "assistant", "content": reply})