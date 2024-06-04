import time
import logging
import sys
from openai import OpenAI
from ddtrace.llmobs import LLMObs
from ddtrace.llmobs.decorators import llm, workflow

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI()

def simple_llm_call():
  try:
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful customer assistant for a travel agency."},
        {"role": "user", "content": "What are the top tourist attractions in Tokyo?"},
      ]
    )

  except Exception as e:
    logging.error('Error occurred: ' + str(e))

  return completion

@llm(model_name="gpt-3.5-turbo", name="evaluated_llm", model_provider="open_ai")
def evaluated_llm_call():
  try:
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": "What are the ethical implications of AI in healthcare?"},
      ]
    )

    LLMObs.annotate(
        span=None,
        input_data=[{"role": "user", "content": "AI implications in healthcare?"}],
        output_data=[{"role": "assistant", "content": "Privacy and security..."}],
        metrics={"input_tokens": 4, "output_tokens": 6, "total_tokens": 10},
        tags={"host": "test_host_name"},
    )

    span_context = LLMObs.export_span(span=None)
    LLMObs.submit_evaluation(
        span_context,
        label="sentiment",
        metric_type="score",
        value=3,
    )

  except Exception as e:
    logging.error('Error occurred: ' + str(e))

  return completion

@workflow(name="process_conversation")
def workflow_llm_call():
  # Initial question and context
  conversation = [
    {"role": "system", "content": "You are a helpful customer assistant for a furniture store."},
    {"role": "user", "content": "What are the latest trends in home office furniture?"},
  ]
  try:
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages = conversation
    )

  except Exception as e:
    logging.error('Error occurred: ' + str(e))

  try:
    # Append previous answer to conversation
    conversation.append(
      { "role": "assistant", 
        "content": completion.choices[0].message.content
      }
    )
    # Append follow up question to conversation
    conversation.append(
      { "role": "user", 
        "content": "That's interesting. Can you recommend any specific brands or designs?"
      }
    )

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages = conversation
    )

  except Exception as e:
    logging.error('Error occurred: ' + str(e))

  try:
    # Append previous answer to conversation
    conversation.append(
      { "role": "assistant", 
        "content": completion.choices[0].message.content
      }
    )
    # Append follow up question to conversation
    conversation.append(
      { "role": "user", 
        "content": "Thank you for the information!"
      }
    )
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages = conversation
    )

  except Exception as e:
    logging.error('Error occurred: ' + str(e))

  return completion

while True:
  simple_completion = simple_llm_call()
  print(simple_completion.choices[0].message)
  logging.info('Simple Completion created successfully')
  time.sleep(10)

  evaluated_completion = evaluated_llm_call()
  print(evaluated_completion.choices[0].message)
  logging.info('Evaluated Completion created successfully')
  time.sleep(10)

  workflow_completion = workflow_llm_call()
  print(workflow_completion.choices[0].message)
  logging.info('Conversation Completion created successfully')
  time.sleep(10)
  
  time.sleep(60)
