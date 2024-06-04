import time
import logging
import sys
from openai import OpenAI
from ddtrace.llmobs import LLMObs
from ddtrace.llmobs.decorators import llm

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI()

def simple_llm_call():
  try:
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful customer assistant for a furniture store."},
        {"role": "user", "content": "What are the latest trends in home office furniture?"},
      ]
    )

    logging.info('Simple completion created successfully')

  except Exception as e:
    logging.error('Error occurred: ' + str(e))

  return completion

@llm(model_name="gpt-3.5-turbo", name="evaluated_llm", model_provider="open_ai")
def evaluated_llm_call():
  try:
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful customer assistant for a furniture store."},
        {"role": "user", "content": "I'd like to buy a chair for my living room."},
        {"role": "assistant", "content": "Would you like recommendations for specific chairs, or do you have a particular style or brand in mind?"},
        {"role": "user", "content": "I'm interested in a purple velvet chair with a dog logo."},
        {"role": "assistant", "content": "That sounds like a unique choice! Let me check our inventory to see if we have any purple velvet chairs with a dog logo. I'll be right back with some options for you."},
        {"role": "user", "content": "So, what are the options???"},
      ]
    )

    logging.info('Evaluated completion created successfully')

    span_context = LLMObs.export_span(span=None)
    LLMObs.submit_evaluation(
        span_context,
        label="sentiment",
        metric_type="score",
        value=10,
    )

  except Exception as e:
    logging.error('Error occurred: ' + str(e))

  return completion

while True:
  simple_completion = simple_llm_call()
  print(simple_completion.choices[0].message)
  logging.info('Simple Completion created successfully')

  evaluated_completion = evaluated_llm_call()
  print(evaluated_completion.choices[0].message)
  logging.info('Evaluated Completion created successfully')
  
  time.sleep(60)
