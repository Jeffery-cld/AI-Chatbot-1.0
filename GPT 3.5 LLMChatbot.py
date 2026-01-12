from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=key)

#Send the API key (from the environment) into the OpenAI class which builds a tool (client) that can access OpenAI’s models.
# System prompt tells model to be short
messages = [
    {"role": "system", "content": "You are a helpful assistant. Keep answers under 50 words unless asked for detail."}
]

while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # cheaper model
        max_tokens=120,  # ~90 words cap
        messages=messages
    )

    reply = response.choices[0].message.content.strip()
    print("AI:", reply)
    messages.append({"role": "assistant", "content": reply})

    #Cost and token tracking
    total_tokens = response.usage.total_tokens
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    # GPT-3.5-turbo token prices tracking $0.50 per 1M input, $1.50 per 1M output
    input_cost = (input_tokens / 1_000_000) * 0.50
    output_cost = (output_tokens / 1_000_000) * 1.50
    total_cost = input_cost + output_cost

    print(f"[Usage] Input: {input_tokens} | Output: {output_tokens} | Total: {total_tokens}")
    print(f"[Cost] ~${total_cost:.6f} for this answer (≈${(total_cost*1000):.4f} per 1000 messages at this length)")

