from ARC_instruction_set_generation_module import *
from visualisation import *
from ARC_output_generation import generate_output
import uuid
import time


def generate_output_string(test_output, placeholder="?"):
    # Create the base string structure
    output_str = '"""Output: \n```json\n{\n    "test_output": [\n'

    # Iterate over each row in the 2D array
    for row in test_output:
        # Replace numbers with the placeholder character
        modified_row = [placeholder if isinstance(item, (int, float)) else item for item in row]
        # Convert the row list to a string and format it correctly
        output_str += f'        {modified_row},\n'

    # Remove the trailing comma from the last row and add the closing braces
    output_str = output_str.rstrip(',\n') + '\n    ]\n}\n```\n"""'

    return output_str


def remove_test_output(data):
    # Initialize a variable to hold the test output
    test_output = None
    
    # Check if 'test' section exists
    if 'test' in data:
        for test_case in data['test']:
            # Extract the 'output' if it exists
            if 'output' in test_case:
                test_output = test_case['output']
                test_input = test_case['input']
                # Remove the 'output' field
                del test_case['output']
    
    # Return the modified data and the extracted test output
    return str(data), test_output, test_input, generate_output_string(test_output)


def compare_2d_arrays(arr1, arr2):
    """
    Compares two 2-D arrays (lists of lists) by converting them to NumPy arrays.
    Returns a tuple (same, accuracy), where:
      - same (bool): True if the arrays have the same shape and every element matches.
      - accuracy (float): The percentage of matching elements (100 if exactly the same).
    
    Note: This function assumes that the input lists represent rectangular arrays.
    """
    # Convert the lists of lists to NumPy arrays
    np_arr1 = np.array(arr1)
    np_arr2 = np.array(arr2)
    
    # Check if the shapes are the same
    if np_arr1.shape != np_arr2.shape:
        return False, 0.0
    
    # Create a boolean array of elementwise comparisons
    comparison = (np_arr1 == np_arr2)
    
    # Calculate the accuracy percentage
    total_elements = np_arr1.size
    matching_elements = np.sum(comparison)
    accuracy = (matching_elements / total_elements) * 100
    
    # Determine if arrays are exactly the same
    same = (accuracy == 100)
    
    return same, accuracy


def demo_framework(json_file_path,socketio):
    # Create root container node for the entire process
    root_node_id = f"node-{str(uuid.uuid4())}"
    socketio.emit('update', {
        'id': root_node_id,
        'label': 'ARC Pattern Analysis',
        'type': 'textUpdater'
    })
    time.sleep(0.2)

    
    
    image_filename = "test_input.jpg_combined.jpg"
    image_url = f"http://localhost:5020/backend-image/{image_filename}"  # URL to serve image
    correct_output_filename = "test_input.jpg_test_output.jpg"
    correct_output_url = f"http://localhost:5020/backend-image/{correct_output_filename}"
    predicted_output_filename = "test_input.jpg_predicted.jpg"
    predicted_output_url = f"http://localhost:5020/backend-image/{predicted_output_filename}"

    
    
    with open(json_file_path) as f:
        data = json.load(f)

    # Create data preparation node
    prep_node_id = f"node-{str(uuid.uuid4())}"
    socketio.emit('update', {
        'id': prep_node_id,
        'label': 'Data Preparation',
        'parentId': root_node_id,
        'type': 'textUpdater'
    })
    time.sleep(0.2)

    image_path = 'test_input.jpg'
    save_image(data, image_path)
    save_image_with_numbers(data, image_path + "_numbered_")
    data_new, test_o, test_i, output_format = remove_test_output(data)

    socketio.emit('puzzleupdate', {
            'mainPuzzle': image_url,          # URL for the main puzzle image
            'correctOutput': correct_output_url,   # URL for the correct output image
        })

    # Create image node to show the input
    input_image_node_id = f"node-{str(uuid.uuid4())}"
    socketio.emit('update', {
        'id': input_image_node_id,
        'label': 'Input Image',
        'imageUrl': image_url,
        'parentId': prep_node_id,
        'type': 'imageNode'
    })
    time.sleep(0.2)

    # Pattern analysis node
    pattern_analysis_node_id = f"node-{str(uuid.uuid4())}"
    socketio.emit('update', {
        'id': pattern_analysis_node_id,
        'label': 'Visual Pattern Analysis',
        'parentId': input_image_node_id,
        'type': 'textUpdater'
    })
    time.sleep(0.2)

    # Find visual patterns
    visual_patterns, questions, last_node_id = find_all_commonalities(
        "test_input.jpg", 
        socketio, 
        parent_node_id=pattern_analysis_node_id
    )

    # Create numbered pattern analysis node
    numbered_analysis_node_id = f"node-{str(uuid.uuid4())}"
    socketio.emit('update', {
        'id': numbered_analysis_node_id,
        'label': 'Numbered Pattern Analysis',
        'parentId': last_node_id,
        'type': 'textUpdater'
    })
    time.sleep(0.2)

    # Find numbered patterns
    numbered_patterns, questions, last_node_id = find_all_commonalities(
        image_path, 
        socketio, 
        commonalities=visual_patterns, 
        questions=questions, 
        numbered=True, 
        parent_node_id=numbered_analysis_node_id
    )

    print(visual_patterns)
    print(numbered_patterns)

    # Create output generation node
    output_node_id = f"node-{str(uuid.uuid4())}"
    socketio.emit('update', {
        'id': output_node_id,
        'label': 'Output Generation',
        'parentId': last_node_id,
        'type': 'DisplayNode'
    })
    time.sleep(0.2)

    # Generate output using the patterns
    final_output, answer_node_id = generate_output(
        image_path,
        socketio,
        numbered_patterns,  # Using the numbered patterns as instruction set
        json.dumps(data),
        output_format,
        output_node_id
    )

    # Create result comparison node
    result_node_id = f"node-{str(uuid.uuid4())}"
    socketio.emit('update', {
        'id': result_node_id,
        'label': 'Result Comparison',
        'parentId': answer_node_id,
        'type': 'textUpdater'
    })
    time.sleep(0.2)

    are_same, acc = compare_2d_arrays(final_output, test_o)

    # Create final result node
    final_result_node_id = f"node-{str(uuid.uuid4())}"
    socketio.emit('update', {
        'id': final_result_node_id,
        'label': f"Result: {'Correct' if are_same else 'Wrong'} (Accuracy: {acc}%)",
        'parentId': result_node_id,
        'type': 'displayNode'
    })
    time.sleep(0.2)


    socketio.emit('puzzleupdate', {
            'mainPuzzle': image_url,          # URL for the main puzzle image
            'correctOutput': correct_output_url,
            "generatedOutput" : predicted_output_url   # URL for the correct output image
        })

    socketio.emit('matrixupdate', {
        'same': "Correct" if are_same else "Wrong",
        'accuracy': acc
    })

    print("Final Generated Output:", final_output)
    return final_output

