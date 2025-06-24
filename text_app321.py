import openai
import gradio as gr
import os
from dotenv import load_dotenv

# Load your OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Text generation function
def generate_text(prompt, temperature, max_tokens):
    if not prompt.strip():
        return "Please enter something!"
    if len(prompt) > 200:
        return "Too long. Please limit it to 200 characters."

    # Prompt engineering: instruct the model to only complete
    formatted_prompt = f"Complete this phrase naturally and stay on topic:\n{prompt}"

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that completes unfinished phrases naturally."},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Gradio interface
iface = gr.Interface(
    fn=generate_text,
    inputs=[
        gr.Textbox(lines=2, label="Enter your prompt"),
        gr.Slider(0.0, 1.0, value=0.7, label="Temperature"),
        gr.Slider(10, 500, value=100, step=10, label="Max Tokens")
    ],
    outputs="text",
    title="The Greatest 'Finish My Phrase' Text Generator"
)

iface.launch()