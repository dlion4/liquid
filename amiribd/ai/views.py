from g4f.client import Client


client = Client()

paragraph = (
    "Write a blog of 300 words with the heading 'The rise of alexander the great'"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": paragraph},
    ],
)
print(response.choices[0].message.content)
