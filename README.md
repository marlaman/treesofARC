# Tree of ARC

Trees of ARC is a modular-reasoning framework aimed at boosting model performance on the ARC AGI 1 dataset. The project aims to break down decision making using complex reasoning frameworks which consist of reasoning modules that abstract a reasoning task like - Input Analysis, Idea Generation, Output Parsing, etc

</br>



Each module can consist of complex reasoning frameworks that can use:

1) Multiple LLM APIs
2) Image Processing APIs
3) A Python Interpreter
4) Programatic paradigms like loops, if-else, recursion, etc

 </br>


Module are can then be combine using the same features to create a framework.

</br>
</br>


Currently, in the demo_framework - you can see two modules (i) Instruction Set Generation and (ii) Output Generation



## Features

- Interactive visualization of ARC puzzle-solving process
- Real-time updates and step-by-step solution generation
- Visual representation of puzzle matrices and transformations
- LLM-powered reasoning and solution generation
- Dynamic node-based visualization of the solution process

## Tech Stack

### Frontend
- React.js
- React Flow for interactive node visualization
- Material-UI (MUI) for UI components
- Socket.IO client for real-time updates
- Tailwind CSS for styling

### Backend
- Flask (Python)
- Flask-SocketIO for WebSocket support
- Large Language Model integration
- Custom ARC puzzle processing modules

## Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- npm or yarn package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ARCAssist.git
cd ARCAssist
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Start the backend server:
```bash
cd backend
python app.py
```
The backend server will start on port 5020.

2. Start the frontend development server:
```bash
# From the root directory
npm start
```
The frontend will be available at http://localhost:3040

## Project Structure

```
ARCAssist/
├── backend/
│   ├── app.py                 # Flask server
│   ├── llm_stuff.py          # LLM integration
│   ├── demo_framework.py      # Demo functionality
│   ├── ARC_output_generation.py
│   ├── visualisation.py
│   └── ARC_instruction_set_generation_module.py
├── src/
│   ├── App.js                # Main React component
│   ├── components/           # React components
│   ├── index.css             # Global styles
│   └── ...
├── public/                    # Static assets
├── package.json              # Frontend dependencies
└── README.md                 # This file
```

## Features in Detail

- **Interactive Node Graph**: Visualize the puzzle-solving process through an interactive node-based interface
- **Real-time Updates**: See the solution process unfold in real-time with WebSocket communication
- **Matrix Visualization**: Clear visual representation of ARC puzzles and their transformations
- **LLM Integration**: Leverage large language models for puzzle analysis and solution generation
- **Step-by-step Solution**: Break down complex puzzle solutions into understandable steps

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Abstraction and Reasoning Corpus (ARC) challenge
- OpenAI for LLM capabilities
- React Flow for visualization components
