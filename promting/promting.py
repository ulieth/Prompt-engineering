# %pip install -U -q "google-generativeai>=0.8.3"
import google.generativeai as genai
from IPython.display import HTML, Markdown, display

# GOOGLE_API_KEY is an API key from AI Studio
# You can easily generate it
# The key is available through Kaggle secrets by choosing Secrets from the Add-ons menu

from kaggle_secrets import UserSecretsClient

GOOGLE_API_KEY = UserSecretsClient().get_secret("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# In this step, you will test that your API key is set up correctly by making a request.
# The gemini-1.5-flash model has been selected here
flash = genai.GenerativeModel('gemini-1.5-flash')
response = flash.generate_content("Explain AI to me like I'm a kid.")
print(response.text)
# Start a chat
chat = flash.start_chat(history=[])
response = chat.send_message('Hello! My name is Zlork.')
print(response.text) # Hello Zlork! It's nice to meet you. 😊 What can I do for you today?
response = chat.send_message('Can you tell something interesting about dinosaurs?')
print(response.text)
# While you have the `chat` object around, the conversation state
# persists. Confirm that by asking if it knows my name.
response = chat.send_message('Do you remember what my name is?')
print(response.text)
# The Gemini API provides access to a number of models from the Gemini model family.
for model in genai.list_models():
  print(model.name)
# To stop the model from generating tokens past a limit, you can specify the `max_output_tokens`
short_model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=genai.GenerationConfig(max_output_tokens=200))

response = short_model.generate_content('Write a 1000 word essay on the importance of olives in modern society.')
print(response.text)
# Temperature
from google.api_core import retry

high_temp_model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=genai.GenerationConfig(temperature=2.0))


# When running lots of queries, it's a good practice to use a retry policy so your code
# automatically retries when hitting Resource Exhausted (quota limit) errors.
retry_policy = {
    "retry": retry.Retry(predicate=retry.if_transient_error, initial=10, multiplier=1.5, timeout=300)
}

for _ in range(5):
  response = high_temp_model.generate_content('Pick a random colour... (respond in a single word)',
                                              request_options=retry_policy)
  if response.parts:
    print(response.text, '-' * 25)

# The same prompt with temperature set to zero
# The output is not completely deterministic, as other parameters affect token selection,
# but the results will tend to be more stable.
low_temp_model = genai.GenerativeModel(
    'gemini-1.5-flash',
    generation_config=genai.GenerationConfig(temperature=0.0))

for _ in range(5):
  response = low_temp_model.generate_content('Pick a random colour... (respond in a single word)',
                                             request_options=retry_policy)
  if response.parts:
    print(response.text, '-' * 25)

# Top-K and Top-P
model = genai.GenerativeModel(
    'gemini-1.5-flash-001',
    generation_config=genai.GenerationConfig(
        # These are the default values for gemini-1.5-flash-001.
        temperature=1.0,
        top_k=64,
        top_p=0.95,
    ))

story_prompt = "You are a creative writer. Write a short story about a cat who goes on an adventure."
response = model.generate_content(story_prompt, request_options=retry_policy)
print(response.text)
# Zero-shot prompts are prompts that describe the request for the model directly.
model = genai.GenerativeModel(
    'gemini-1.5-flash-001',
    generation_config=genai.GenerationConfig(
        temperature=0.1,
        top_p=1,
        max_output_tokens=5,
    ))

zero_shot_prompt = """Classify movie reviews as POSITIVE, NEUTRAL or NEGATIVE.
Review: "Her" is a disturbing study revealing the direction
humanity is headed if AI is allowed to keep evolving,
unchecked. I wish there were more movies like this masterpiece.
Sentiment: """

response = model.generate_content(zero_shot_prompt, request_options=retry_policy)
print(response.text) # Sentiment: **POSITIVE**
# The Gemini API has an Enum mode feature that allows you to constrain the output to a fixed set of values
import enum

class Sentiment(enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


model = genai.GenerativeModel(
    'gemini-1.5-flash-001',
    generation_config=genai.GenerationConfig(
        response_mime_type="text/x.enum",
        response_schema=Sentiment
    ))

response = model.generate_content(zero_shot_prompt, request_options=retry_policy)
print(response.text)
