# llm-observability-script
Script to generate LLM Observability data in Datadog

## Overview

This example provides the code to quickly spin up a script that will generate LLM Observability data in Datadog.

It spins up 2 containers, a python llm script instance, and a Datadog Agent.

The script will post data every 60 seconds but you can change this value in the python script.

## Requirements

- [Docker](https://www.docker.com/).

## Getting Started

### Requirements:
You will need the following to run this example:
  - A Datadog API key. You can get one [here](https://docs.datadoghq.com/account_management/api-app-keys/#api-keys)
  - An OpenAI API key. You can get one [here](https://platform.openai.com/signup/).
  - Some credits in your OpenAI account. You can add some [here](https://platform.openai.com/account/billing).

### Environment file:

You will need to create a `.env` file at the root of this repository with the following variables:
```bash
OPENAI_API_KEY=<OPEN_AI_API_KEY>
DD_API_KEY=<DATADOG_API_KEY>
DD_SITE=<datadoghq.com|datadoghq.eu>
```
For the `DD_SITE` variable, please keep the value relevant to your Datadog account region. 

## Usage

1. Build `make build`
2. Run `make run`
3. Stop `make stop`

See the [Makefile](Makefile) for more commands.
