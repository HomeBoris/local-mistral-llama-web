# -*- coding: utf-8 -*-
import panel as pn
import codecs
import locale
import os
from ctransformers import AutoModelForCausalLM

pn.extension()

async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):

    if "mistral" not in llms:
        instance.placeholder_text = "Downloading model; please wait..."

        llms["mistral"] = AutoModelForCausalLM.from_pretrained(
            "TheBloke/Mistral-7B-Instruct-v0.1-GGUF",
            model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            gpu_layers=1,
        )

    llm = llms["mistral"]
    response = llm(contents, stream=True, max_new_tokens=1000)
    message = ""

    for token in response:
        message += token
        yield message

llms = {}

chat_interface = pn.chat.ChatInterface(callback=callback, callback_user="Mistral")

chat_interface.send(
    "Отправьте сообщение и получите ответ от нейросети!", user="System", respond=False
)

chat_interface.servable()