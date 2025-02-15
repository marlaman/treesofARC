from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
# from langchain.output_parsers import StrOutputParser
import pandas as pd
import numpy as np
import uuid
import textwrap
import json
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
# Initialize the OpenAI Chat model
import os
import time

os.environ["OPENAI_API_KEY"] = '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'
           
api_key = "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"

llm = ChatOpenAI(model='gpt-4o-mini',temperature = 0.0001)

LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="pr-plaintive-succotash-73"



import requests
import base64
from PIL import Image
import numpy as np
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
global conversation_history

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

def find_common_patterns(first, second, third, commonalities = ""):
    # global conversation_history
    # api_key = 'sk-proj-mtnt5y5G2U2DhczZUg6DT3BlbkFJNiSb59Zvu7ipGJ3R1anS'
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    conversation_history = []

    # Add user message to conversation history
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"""You will be given descriptions + further questions of 3 training input-output instances - of visual patterns described by text. These are all part of the same puzzle which involves transforming an input image into an output image using some rules.

                        I want you to combine them and give me very very briefly what do you think is common among them.
                        
                        You can present them as two outputs -
                        
                        1) high confidence pattern aspects
                        
                        2) an intruction set which intructs a human on how to convert the test input of a new puzzle into an output. If you are given a hint with this already is present, you need to clarify it and add more details/make it easier to follow. 


                        HINT ABOUT THE VISUAL PATTERN (IGNORE IF EMPTY) : {commonalities}

                         If provided a hint, please make sure that you are adding more trustable information about the precise pattern. Your output must not be just a copy of the hint. You will be severly penalised if you are lazy and just return the hint in different words. 
                
                YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE HINTS TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.

                        
                        
                        The descriptions are:
                        
                        First Puzzle Description:
                        
                        {first}
                        
                        Second:
                        
                        {second}
                        
                        Third:
                        
                        {third}




                        YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE HINTS TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.
                        YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE HINTS TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.
                        YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE HINTS TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.
                        YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE HINTS TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.
                        YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE HINTS TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.
                        YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE HINTS TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.
                        YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE HINTS TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE HINTS TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.
                        """ 
            }
        ]
    }
    conversation_history.append(user_message)

    payload = {
        "model": "gpt-4o-mini",
        "messages": conversation_history,
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response)
    description = response.json().get('choices')[0]['message']['content']
    
    # Add GPT response to conversation history
    gpt_message = {
        "role": "assistant",
        "content": description
    }
    conversation_history.append(gpt_message)
    
    return description


def describe_image_via_gpt(image_path,train_input="", train_output="", commonalities = "", questions = ""):
    # global conversation_history
    # api_key = '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'
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    conversation_history = []
    
    # Add user message to conversation history
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"""You will be given a train set image of a visual pattern recognition problem (which is just a 2-D array visualized)


                
                The image consists of an input pattern and its output pattern, which is a definitely different from the input. 
                
                
                Your task is only to analyze it (using the hint if its given) and talk about what the EXACT pattern is. Make sure to be AS SPECIFIC AS POSSIBLE.  You will be penalized heavily for ambiguity.

                
                
                
                HINTs ABOUT THE VISUAL PATTERN (Ignore if empty) - {commonalities}

                Further Questions about the patter to the answered (Ignore if empty) - {questions}

                You will be penalized very heavily if you don't find an answer for the questions asked here above

                
                
                
                
                USE THE HINT ABOVE (IF GIVEN) as a starting point, to then come up with MUCH more detailed description about how exactly the input might be being transformed to the output - thinking about things like 

                        1) Are there objects in the pictures? Are they appearing or disappearing? Do they interact with each other? Do they interact with the background?

                        2) Do the objects have intentions like agents? Are they animate or inaminate? What is the nature of their change in the output?

                        3) Is there any counting necesssary? Would it be a good way to predict a pattern? Are there basic mathematical operations like addition, subtraction and comparison involved?

                        4) Are there any shapes like rectangles, triangles, and circles? Are they being mirrored, rotated, translated, deformed, combined, repeated, etc? Are their distances predictive of the output?

                
                If provided a hint, please make sure that you are adding more trustable information about the precise pattern. Your output must not be just a copy of the hint. You will be severly penalised if you are lazy and just return the hint in different words. 
                
                YOU NEED TO BE VERY VERY SPECIFIC ABOUTT THE PATTERN SUCH THAT A HUMAN ON THE OTHER HAND CAN USE THESE descriptions TO TRANSLATE THE TEST INPUT TO THE TEST OUTPUT.
                
            

                YOUR OUTPUT MUST BE AS BRIEF AS POSSIBLE, BUT BE VERY PRECISE AND AVOID AMBIGUITY
                """
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_path}",
                    "detail": "high"
                }},
        ]
    }
    conversation_history = []
    conversation_history.append(user_message)

    payload = {
        "model": "gpt-4o-mini",
        "messages": conversation_history
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    description = response.json().get('choices')[0]['message']['content']
    
    # Add GPT response to conversation history
    gpt_message = {
        "role": "assistant",
        "content": description
    }
    conversation_history.append(gpt_message)
    
    return description


def instruction_set_questions(image_path,instruction_set, numbered = False):
    # global ins_conversation_history

    if numbered:
        base64_image_train = encode_image(image_path + "_numbered__train_1.jpg")
    else:
        base64_image_train = encode_image(image_path + "_train_1.jpg")

    # print(len(ins_conversation_history))
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    ins_conversation_history = []

    # Add user message to conversation history
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"""You will be given 
                
                1) a input and an output for a pattern recognition train set as an image (its a problem in an ML dataset),
                
                
                
                Your only task is to see if the instruction set correctly and accurately explains the transformations. 
                Ideally, this instruction set should be able to be used by a human to transform the input to the output correctly, without any ambiguity

                Then, if you feel like the instruction set is not correct or not comprehensive enough. Return the crucial questions that help reason about the problem in more detail.
                
                Focus on details.
                
                                
                
                Your reply must have only 1 section:

                1) Further questions/clarifications if any. Never ask any questions of visual cues, You will only ever get text inputs. 
                
                Your only questions must be about clarifications about the logic or specifics about how to transform the input


                Example output:


                1) Some crucial questions are:
                            - How do i detect this shape?...
                            - Exactly how many steps should I move this objects...
                            - ...
                            - ...


                The instruction set is:

                {instruction_set}
                
                """
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image_train}",
                    "detail": "high"
                }},

        ]
    }

    ins_conversation_history.append(user_message)
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": ins_conversation_history
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # print(response.json())
    description = response.json().get('choices')[0]['message']['content']

    # Add GPT response to conversation history
    gpt_message = {
        "role": "assistant",
        "content": description
    }
    # ins_conversation_history.append(gpt_message)
    return description


def describe_each_train_set(image_path, socket, commonalities="", questions="", numbered=False, parent_node_id=None):
    global conversation_history
    answers = []
    nodes = []
    last_node_id = parent_node_id

    # Create iteration node to group this set of examples
    iteration_node_id = f"node-{str(uuid.uuid4())}"
    socket.emit('update', {
        'id': iteration_node_id,
        'label': 'Analysis Iteration',
        'parentId': parent_node_id,
        'type': 'textUpdater'
    })
    time.sleep(0.2)

    for n in range(1,4):
        image_node_id = f"node-{str(uuid.uuid4())}"
        if numbered:
            base64_image_train = encode_image(image_path + f"_numbered__train_{n}.jpg")
            image_url = f"http://localhost:5020/backend-image/{image_path}_numbered__train_{n}.jpg"
        else:
            base64_image_train = encode_image(image_path + f"_train_{n}.jpg")
            image_url = f"http://localhost:5020/backend-image/{image_path}_train_{n}.jpg"
        
        # Connect image nodes to iteration node
        socket.emit('update', {
            'id': image_node_id,
            'label': f'Training Example {n}',
            'imageUrl': image_url,
            'parentId': iteration_node_id,
            'type': 'imageNode'
        })
        time.sleep(0.2)
            
        description = describe_image_via_gpt(base64_image_train, commonalities=commonalities, questions=questions)

        desc_node_id = f"node-{str(uuid.uuid4())}"
        socket.emit('update', {
            'id': desc_node_id,
            'label': description,
            'parentId': image_node_id,
            'type': 'displayNode'
        })
        time.sleep(0.2)
        
        print(f"\nTraining set {n} Description: \n")
        print(description)
        answers.append(description)
        nodes.append(desc_node_id)

    common_pattern = find_common_patterns(answers[0], answers[1], answers[2])

    pattern_node_id = f"node-{str(uuid.uuid4())}"
    # Connect the pattern node to each description node
    # for desc_node_id in nodes:
    #     socket.emit('update', {
    #         'id': f"{pattern_node_id}-{desc_node_id}",  # Create unique edge ID
    #         'source': desc_node_id,
    #         'target': pattern_node_id,
    #         'type': 'smoothstep'
    #     })
    #     time.sleep(0.2)
    
    # Create the pattern node itself
    for desc_node_id in nodes:
        socket.emit('update', {
            'id': pattern_node_id,
            'label': common_pattern,
            'parentId': desc_node_id,
            'type': 'displayNode'
        })
        time.sleep(0.2)

    print("\nCommon Pattern : \n")
    print(common_pattern)

    return common_pattern, pattern_node_id

def find_all_commonalities(image_path, socket, commonalities='', questions='', n=3, numbered=False, parent_node_id=None):
    description = commonalities
    questions = questions
    last_node_id = parent_node_id
    
    # Create a container node for all iterations
    analysis_container_id = f"node-{str(uuid.uuid4())}"
    socket.emit('update', {
        'id': analysis_container_id,
        'label': 'Pattern Analysis Steps',
        'parentId': parent_node_id,
        'type': 'textUpdater'
    })
    time.sleep(0.2)

    for i in range(0,n):
        # Create iteration container
        iteration_container_id = f"node-{str(uuid.uuid4())}"
        socket.emit('update', {
            'id': iteration_container_id,
            'label': f'Analysis Step {i+1}',
            'parentId': last_node_id if i > 0 else analysis_container_id,  # Connect to previous iteration or container
            'type': 'textUpdater'
        })
        time.sleep(0.2)

        if numbered:
            description, pattern_node_id = describe_each_train_set(
                image_path, 
                socket, 
                commonalities=description, 
                questions=questions, 
                numbered=True,
                parent_node_id=iteration_container_id
            )
            questions = instruction_set_questions(image_path, description, numbered=True)
            last_node_id = pattern_node_id
        else:
            description, pattern_node_id = describe_each_train_set(
                image_path, 
                socket, 
                commonalities=description, 
                questions=questions,
                parent_node_id=iteration_container_id
            )
            questions = instruction_set_questions(image_path, description)

            # Create questions node connected to pattern node
            questions_node_id = f"node-{str(uuid.uuid4())}"
            socket.emit('update', {
                'id': questions_node_id,
                'label': questions,
                'parentId': pattern_node_id,
                'type': 'displayNode'
            })
            time.sleep(0.2)
            
            print("\nQUESTIONS:", questions)
            last_node_id = questions_node_id

    return description, questions, last_node_id




        
        
        

    
    