from g4f.client import Client

def generate(query):
    query = query.replace('google','')
    query = query + "summary in 30-50 words"
    # text generator
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
        )
    generated_text = response.choices[0].message.content
    #print(generated_text)
    return generated_text