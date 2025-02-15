from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import numpy as np


import os

os.environ["OPENAI_API_KEY"] = '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'
           
api_key = "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"

llm = ChatOpenAI(model='gpt-4o-mini',temperature = 0.0001)



import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
global ins_conversation_history

# Initialize conversation history
conversation_history = []
output_generation_history = []

ins_conversation_history = []



def save_image(data, base_filename):
    # Fixed colors for integers 0-9:
    fixed_colors = [
        '#AAFF22',  # 0 -> White
        '#FF0000',  # 1 -> Red
        '#0000FF',  # 2 -> Blue
        '#808000',  # 3 -> Green
        '#FFFF00',  # 4 -> Yellow
        '#FF00FF',  # 5 -> Magenta
        '#00FFFF',  # 6 -> Cyan
        '#000000',  # 7 -> Black
        '#FFA500',  # 8 -> Orange
        '#800080'   # 9 -> Purple
    ]
    
    # Create a ListedColormap with a fixed mapping from integer to color.
    cmap = mcolors.ListedColormap(fixed_colors)
    # BoundaryNorm makes sure that each integer falls into its own bin.
    norm = mcolors.BoundaryNorm(np.arange(-0.5, 10.5, 1), cmap.N)
    
    # Helper function to get grid size string (e.g., "4x5").
    def get_grid_size_str(grid):
        grid_arr = np.array(grid)
        return f"{grid_arr.shape[0]}x{grid_arr.shape[1]}"
    
    # Helper function to display a grid using the fixed colormap.
    # It now appends the grid size to the title.
    def plot_grid(ax, grid, base_title):
        size_str = get_grid_size_str(grid)
        full_title = f"{base_title} ({size_str})"
        ax.imshow(np.array(grid), cmap=cmap, norm=norm)
        ax.set_title(full_title, fontsize=12, color='red')
        ax.axis('off')
    
    # Save train images.
    for i in range(3):
        if i < len(data['train']):
            fig, axs = plt.subplots(1, 2, figsize=(8, 4))
            fig.suptitle(f'Visualization of Train Set {i+1}', fontsize=14, color='red')
            
            input_grid = data['train'][i]['input']
            output_grid = data['train'][i]['output']
            
            plot_grid(axs[0], input_grid, f'Train Input {i+1}')
            plot_grid(axs[1], output_grid, f'Train Output {i+1}')
            
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig(f'{base_filename}_train_{i+1}.jpg', format='jpg')
            plt.close(fig)
    
    # Save test image (with a question mark for the output).
    if 'test' in data and data['test']:
        fig, axs = plt.subplots(1, 2, figsize=(8, 4))
        fig.suptitle('Visualization of Test Set', fontsize=14, color='red')
        
        test_input = data['test'][0]['input']
        plot_grid(axs[0], test_input, 'Test Input')
        
        axs[1].text(0.5, 0.5, '?', fontsize=60, ha='center', va='center', color='red')
        axs[1].set_title('Test Output', fontsize=12, color='red')
        axs[1].axis('off')
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(f'{base_filename}_test.jpg', format='jpg')
        plt.close(fig)
    
    # Create a combined image with train sets and test set.
    fig, axs = plt.subplots(4, 2, figsize=(12, 16))
    for i in range(3):
        if i < len(data['train']):
            plot_grid(axs[i, 0], data['train'][i]['input'], f'Train Input {i+1}')
            plot_grid(axs[i, 1], data['train'][i]['output'], f'Train Output {i+1}')
    
    if 'test' in data and data['test']:
        plot_grid(axs[3, 0], data['test'][0]['input'], 'Test Input')
        axs[3, 1].text(0.5, 0.5, '?', fontsize=60, ha='center', va='center', color='red')
        axs[3, 1].set_title('Test Output', fontsize=12, color='red')
        axs[3, 1].axis('off')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f'{base_filename}_combined.jpg', format='jpg')
    plt.close(fig)
    
    # Save the test output (if available) as a separate image.
    if 'test' in data and data['test']:
        fig, ax = plt.subplots()
        test_output = data['test'][0]['output']
        size_str = get_grid_size_str(test_output)
        ax.imshow(np.array(test_output), cmap=cmap, norm=norm)
        ax.set_title(f"Test Output ({size_str})", fontsize=12, color='red')
        ax.axis('off')
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        plt.savefig(f'{base_filename}_test_output.jpg', bbox_inches='tight', pad_inches=0, format='jpg')
        plt.close(fig)

def save_image_with_numbers(data, base_filename):
    # Fixed colors for integers 0-9:
    fixed_colors = [
        '#AAFF22',  # 0 -> White
        '#FF0000',  # 1 -> Red
        '#0000FF',  # 2 -> Blue
        '#808000',  # 3 -> Green
        '#FFFF00',  # 4 -> Yellow
        '#FF00FF',  # 5 -> Magenta
        '#00FFFF',  # 6 -> Cyan
        '#000000',  # 7 -> Black
        '#FFA500',  # 8 -> Orange
        '#800080'   # 9 -> Purple
    ]
    
    # Create a ListedColormap and norm that forces each integer to a fixed color.
    cmap = mcolors.ListedColormap(fixed_colors)
    norm = mcolors.BoundaryNorm(np.arange(-0.5, 10.5, 1), cmap.N)
    
    # Function to overlay numbers on the grid.
    def display_numbers(ax, grid):
        grid = np.array(grid)  # Convert to a NumPy array if it isn't already
        fontsize = 12 * min(10 / max(grid.shape), 1)  # Adjust font size based on grid dimensions
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                ax.text(j, i, str(grid[i, j]),
                        ha='center', va='center',
                        color='white', fontsize=fontsize,
                        weight='bold')
    
    # Save train images.
    for i in range(3):
        if i < len(data['train']):
            fig, axs = plt.subplots(1, 2, figsize=(8, 4), dpi=150)
            fig.suptitle(f'Visualization of Train Set {i+1}', fontsize=14)
    
            # Convert the grid lists to NumPy arrays
            input_grid = np.array(data['train'][i]['input'])
            output_grid = np.array(data['train'][i]['output'])
    
            # Get shapes for titles
            input_shape_str = f"{input_grid.shape[0]}x{input_grid.shape[1]}"
            output_shape_str = f"{output_grid.shape[0]}x{output_grid.shape[1]}"
    
            axs[0].imshow(input_grid, cmap=cmap, norm=norm)
            axs[0].set_title(f'Train Input {i+1} ({input_shape_str})', fontsize=12)
            axs[0].axis('off')
            display_numbers(axs[0], input_grid)
    
            axs[1].imshow(output_grid, cmap=cmap, norm=norm)
            axs[1].set_title(f'Train Output {i+1} ({output_shape_str})', fontsize=12)
            axs[1].axis('off')
            display_numbers(axs[1], output_grid)
    
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.savefig(f'{base_filename}_train_{i+1}.jpg', format='jpg', dpi=150)
            plt.close(fig)
    
    # Save test image.
    if 'test' in data and data['test']:
        fig, ax = plt.subplots(1, 1, figsize=(8, 4), dpi=150)
        fig.suptitle('Visualization of Test Set', fontsize=14)
    
        test_input = np.array(data['test'][0]['input'])
        test_shape_str = f"{test_input.shape[0]}x{test_input.shape[1]}"
    
        ax.imshow(test_input, cmap=cmap, norm=norm)
        ax.set_title(f'Test Input ({test_shape_str})', fontsize=12)
        ax.axis('off')
        display_numbers(ax, test_input)
    
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(f'{base_filename}_test.jpg', format='jpg', dpi=150)
        plt.close(fig)


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