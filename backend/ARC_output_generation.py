from langchain_openai import ChatOpenAI
# from langchain.output_parsers import StrOutputParser
import json

# Initialize the OpenAI Chat model
import os
import time
import uuid
import matplotlib.pyplot as plt

os.environ["OPENAI_API_KEY"] = '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'
           
api_key = "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"

llm = ChatOpenAI(model='gpt-4o-mini',temperature = 0.0001)

LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="pr-plaintive-succotash-73"



import requests
import base64
import requests
import matplotlib
matplotlib.use('Agg')

global ins_conversation_history

# Initialize conversation history
conversation_history = []
output_generation_history = []

ins_conversation_history = []



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def understand_first_train(image_path,instruction_set,data):
    global output_generation_history
    # api_key = 'sk-proj-mtnt5y5G2U2DhczZUg6DT3BlbkFJNiSb59Zvu7ipGJ3R1anS'
    base64_image_train = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Add user message to conversation history
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "The image you are given is one example unit of the training set input and output in a visual pattern recognition problem. The image has been generated using an NxN dimensional number array which you will be given. You will also be given the step-by-step instructions to visually derive the output from the input. \n\nYour only task is to understand how the visual instructions relate to the numbers changing because after this(not now), you will be asked to generate the numerical output for a certain test input.\n\n The NxN dimensional array that generated the image given to you is: " + data + "\n\n The step-by-step instructions to derive the output are: " + instruction_set
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image_train}",
                    "detail": "high"
                }}
        ]
    }
    output_generation_history.append(user_message)

    payload = {
        "model": "gpt-4o-mini",
        "messages": output_generation_history
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    description = response.json().get('choices')[0]['message']['content']
    
    # Add GPT response to conversation history
    gpt_message = {
        "role": "assistant",
        "content": description
    }
    output_generation_history.append(gpt_message)
    
    return description


def generate_test_output(image_path,instruction_set,data):
    global output_generation_history
    # api_key = 'sk-proj-mtnt5y5G2U2DhczZUg6DT3BlbkFJNiSb59Zvu7ipGJ3R1anS'
    base64_image_train = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Add user message to conversation history
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Now you'll be given the test input, both the image and the number arrays, along with the instruction set. Your task is to return what the FULL and EXACT ANSWER in terms of the number arrays for the full output would be while following the instructions. ENSURE YOU HAVE MADE ALL CHANGES BEFORE REPLYING PLEASE I BEG YOU. \n\n The NxN dimensional array that generated the image given to you is: " + data + "\n\n The step-by-step instructions to derive the output are: " + instruction_set
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image_train}",
                    "detail": "high"
                }}
        ]
    }
    output_generation_history.append(user_message)

    payload = {
        "model": "gpt-4o-mini",
        "messages": output_generation_history
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    description = response.json().get('choices')[0]['message']['content']
    
    # Add GPT response to conversation history
    gpt_message = {
        "role": "assistant",
        "content": description
    }
    output_generation_history.append(gpt_message)
    
    return description



def generate_test_output_finetune(image_path,instruction_set,data):
    global output_generation_history
    # api_key = 'sk-proj-mtnt5y5G2U2DhczZUg6DT3BlbkFJNiSb59Zvu7ipGJ3R1anS'
    base64_image_train = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Add user message to conversation history
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Consider the previous message and now give ONLY AND ONLY the final and full TEST OUTPUT ONLY \n\n The NxN dimensional array for the test input is : " + data + "\n\n The step-by-step visual instructions to derive the output are: " + instruction_set
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image_train}",
                    "detail": "high"
                }}
        ]
    }
    output_generation_history.append(user_message)

    payload = {
        "model": "gpt-4o-mini",
        "messages": output_generation_history
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    description = response.json().get('choices')[0]['message']['content']
    
    # Add GPT response to conversation history
    gpt_message = {
        "role": "assistant",
        "content": description
    }
    output_generation_history.append(gpt_message)
    
    return description


def extract_arrays(data_str):
    # Convert the string to a dictionary using json
    data_dict = json.loads(data_str.replace("'", '"'))

    # Combine the train inputs and outputs
    train_1 = json.dumps({
        'input': data_dict['train'][0]['input'],
        'output': data_dict['train'][0]['output']
    })
    train_2 = json.dumps({
        'input': data_dict['train'][1]['input'],
        'output': data_dict['train'][1]['output']
    })
    train_3 = json.dumps({
        'input': data_dict['train'][2]['input'],
        'output': data_dict['train'][2]['output']
    })

    # Extract the test input
    test = json.dumps(data_dict['test'][0]['input'])

    return train_1, train_2, train_3, test





def answer_formatting(answer_text, output_format):
    # api_key = 'sk-proj-mtnt5y5G2U2DhczZUg6DT3BlbkFJNiSb59Zvu7ipGJ3R1anS'
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        
    }

    # Add user message to conversation history
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "You will be given the output to a question answering bot. You are tasked with returning only the main answer in the format(remember to replace the question marks with the actual answer numbers) : " + output_format + "\n\n" + "Make sure that you are printing just as many numbers as are specified in the output format. The output to process is : " + answer_text
             }
        ]
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [user_message]
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

def convert_to_2d_array(json_str):
    # Parse the JSON string into a Python dictionary
    data = json.loads(json_str)
    
    # Extract the 'test_output' array
    if 'test_output' in data:
        two_d_array = data['test_output']
        return two_d_array
    else:
        return None  # Return None if 'test_output' is not found
    
def save_predicted_output(pred_array, base_filename):
    """
    Save the predicted output image with no extra whitespace or text.

    Parameters:
        pred_array (numpy.ndarray): The predicted output image array.
        base_filename (str): The base filename for saving the image.
    """
    # Create a new figure and axis.
    fig, ax = plt.subplots()
    
    # Display the image using a colormap.
    ax.imshow(pred_array, cmap='nipy_spectral')
    
    # Remove the axis so no ticks or labels are shown.
    ax.axis('off')
    
    # Adjust the subplot to fill the entire figure area.
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    # Save the figure with no extra whitespace or padding.
    plt.savefig(f'{base_filename}_predicted.jpg', bbox_inches='tight', pad_inches=0)
    plt.close(fig)


def generate_output(image_path, socket, instruction_set, json_string, output_format, parent_node_id):
    # Create container node for output generation

    image_filename = "test_input.jpg_combined.jpg"
    image_url = f"http://localhost:5020/backend-image/{image_filename}"  # URL to serve image
    correct_output_filename = "test_input.jpg_test_output.jpg"
    correct_output_url = f"http://localhost:5020/backend-image/{correct_output_filename}"
    predicted_output_filename = "test_input.jpg_predicted.jpg"
    predicted_output_url = f"http://localhost:5020/backend-image/{predicted_output_filename}"
    output_container_id = f"node-{str(uuid.uuid4())}"

    socket.emit('update', {
        'id': output_container_id,
        'label': 'Output Generation Steps',
        'type': 'textUpdater',
        'parentId': parent_node_id
    })
    time.sleep(0.2)

    print("FINAL INSTRUCTION SET: \n\n")
    print(instruction_set)
    train_1, train_2, train_3, test = extract_arrays(json_string)

    # First training understanding node
    first_node_id = f"node-{str(uuid.uuid4())}"
    first_output = understand_first_train(image_path + "_train_1.jpg", instruction_set, train_1)
    socket.emit('update', {
        'id': first_node_id,
        'label': 'Understanding First Training Example',
        'parentId': output_container_id,
        'type': 'displayNode'
    })
    socket.emit('update', {
        'id': f"node-{str(uuid.uuid4())}",
        'label': first_output,
        'parentId': first_node_id,
        'type': 'displayNode'
    })
    time.sleep(0.2)

    # Test output generation node
    test_node_id = f"node-{str(uuid.uuid4())}"
    final_output = generate_test_output(image_path + "_test.jpg", instruction_set, test)
    socket.emit('update', {
        'id': test_node_id,
        'label': 'Initial Test Output Generation',
        'parentId': first_node_id,
        'type': 'displayNode'
    })
    socket.emit('update', {
        'id': f"node-{str(uuid.uuid4())}",
        'label': final_output,
        'parentId': test_node_id,
        'type': 'displayNode'
    })
    time.sleep(0.2)

    # Finetuned output node
    finetune_node_id = f"node-{str(uuid.uuid4())}"
    final_output_finetuned = generate_test_output_finetune(image_path + "_test.jpg", instruction_set, test)
    socket.emit('update', {
        'id': finetune_node_id,
        'label': 'Finetuned Test Output',
        'parentId': test_node_id,
        'type': 'textUpdater'
    })
    socket.emit('update', {
        'id': f"node-{str(uuid.uuid4())}",
        'label': final_output_finetuned,
        'parentId': finetune_node_id,
        'type': 'displayNode'
    })
    time.sleep(0.2)


    final_output_formatted = answer_formatting(final_output_finetuned, output_format)

    print(final_output_formatted)


    final_list = convert_to_2d_array(final_output_formatted.replace("```","").replace("json","").lower().replace("output:","").replace('"""',"").replace("'",""))

    save_predicted_output(final_list, image_path)
    socket.emit('puzzleupdate', {
        'mainPuzzle': image_url,          # URL for the main puzzle image
        'correctOutput': correct_output_url,
        "generatedOutput" : predicted_output_url   # URL for the correct output image
    })
    answer_node_id = f"node-{str(uuid.uuid4())}"
    
    socket.emit('update', {
    'id': answer_node_id,
    'label': "Final Answer",
    'imageUrl': predicted_output_url,
    'type' : "imageNode", # Send the image URL to the front-end,
    'parentId': finetune_node_id
    })

    return final_output_formatted, answer_node_id