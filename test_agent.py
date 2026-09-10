import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
	model = "claude-sonnet-4-6",
	max_tokens = 300,
	system = "You are an assistant representing Ali Rajabi, a data science graduate student at UT Arlington with a background in IT infrastructure and financial services. Courses I have taken so far are Foundations of Computing, Foundations of Data Science, Statistics and Probability, Machine Learning, Big Data Management, Data Visualizations. Answer questions about their background accurately and concisely.",
	messages = [
		{"role": "user", "content": "What is this person's data science background?"}
		]
	)
print(response.content[0].text)