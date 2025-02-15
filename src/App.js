import React, { useEffect, useReducer, useState, memo } from 'react';
import ReactFlow, { ReactFlowProvider, Controls, Background, applyNodeChanges, applyEdgeChanges, ConnectionLineType, useReactFlow } from 'reactflow';

import 'reactflow/dist/style.css';
import io from 'socket.io-client';
import dagre from 'dagre';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {Box} from '@mui/material';
import './index.css';
import DisplayNode from './components/DisplayNode.js';
import FinetuneNode from './components/FinetuneNode.js';
import ImageNode from './components/ImageNode.js';
import CodeAnswerNode from './components/CodeAnswerNode.js';

import { ArrowRight } from 'lucide-react'
import './components/text-updater-node.css';

const socket = io('http://localhost:5020');

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));
dagreGraph.setGraph({ rankdir: 'TB', ranksep: 40 });


function getNodeDimensions(node) {
  if (node.type === 'imageNode') {
    return { width: 700, height: 750 };
  } else if (node.type === 'textUpdater') {
    return { width: 700, height: 150 };
  } else if (node.type === 'displayNode') {
    return { width: 700, height: 450 };
  } else {
    return { width: 700, height: 200 }; // fallback for other types
  }
}

const nodeTypes = {
  displayNode: memo(DisplayNode),
  codeAnswer: memo(CodeAnswerNode),
  imageNode: memo(ImageNode),
  textUpdater: memo(FinetuneNode)
}
const layoutReducer = (state, action) => {
  switch (action.type) {
    case 'ADD_NODE_AND_EDGE': {
      const { newNode, newEdge } = action.payload;
      const nodesAfterAdd = [...state.nodes, newNode];

      let updatedEdges;
      if (newEdge) {
        updatedEdges = state.edges.filter(
          edge => !(edge.source === newEdge.source && edge.target === newEdge.target)
        );
        updatedEdges.push(newEdge);
      } else {
        updatedEdges = state.edges;
      }

      // Determine the correct dimensions for the new node.
      const { width, height } = getNodeDimensions(newNode);
      dagreGraph.setNode(newNode.id, { width, height });
      if (newEdge) {
        dagreGraph.setEdge(newEdge.source, newEdge.target);
      }

      // Re-run the layout for the entire graph.
      dagre.layout(dagreGraph);

      const layoutedNodes = nodesAfterAdd.map(node => {
        // Get the dimensions for each node.
        const { width: nodeW, height: nodeH } = getNodeDimensions(node);
        const nodeWithPosition = dagreGraph.node(node.id);

        return {
          ...node,
          // dagre returns a center position; subtract half dimensions for top-left coordinates.
          position: {
            x: nodeWithPosition.x - nodeW / 2,
            y: nodeWithPosition.y - nodeH / 2,
          },
          style: {
            color: "#333",
            border: "1px solid #222138",
            position: 'absolute',
            borderRadius: "8px",
            overflow: "auto",
            wordBreak: "break-word",
          },
        };
      });

      return { nodes: layoutedNodes, edges: updatedEdges };
    }

    case 'UPDATE_NODE_TESTS':
      const { nodeId, passedTests, totalTests } = action.payload;

      // Update the specific node's test data
      const nodesAfterTestUpdate = state.nodes.map(node => { // Renamed to 'nodesAfterTestUpdate'
        if (node.id === nodeId) {


          return {
            ...node,
            data: {
              ...node.data,
              passedTests,
              totalTests,
              hasTests: totalTests > 0
            }
          };
        }
        return node;
      });

      return { ...state, nodes: nodesAfterTestUpdate };

    case 'UPDATE_NODES':
      return { ...state, nodes: action.payload };

    case 'UPDATE_EDGES':
      return { ...state, edges: action.payload };

    default:
      return state;
  }
};

const theme = createTheme({
  palette: {
    primary: {
      main: '#FF69B4',
    },
    secondary: {
      main: '#1E90FF',
    },
    background: {
      default: '#FFFFFF',
      paper: '#F5F5F5',  // Changed to light grey
    },
    text: {
      primary: '#000000', // Changed to black text
      secondary: '#FF69B4',
    },
  },
  typography: {
    fontFamily: '"Fira Code", monospace, bold',
    h1: {
      fontSize: '6rem',
      fontWeight: 900,
      marginBottom: '40px',
    },
    body1: {
      fontSize: '1rem',
      color: '#FFFFFF',
    },
    body2: {
      fontSize: '0.875rem',
      color: '#FF69B4',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          fontFamily: '"Playfair Display", serif', // Classy and minimalistic font
          color: '#000000', // Black text on yellow button
          backgroundColor: '#FFEB3B', // Yellow button background
          '&:hover': {
            backgroundColor: '#FFD700', // Darker yellow on hover
          },
        },
      },
    },
  },

});

function App() {
  const [state, dispatch] = useReducer(layoutReducer, { nodes: [], edges: [] });
  const [isLoaded, setIsLoaded] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const { fitView } = useReactFlow();

  const reactFlowInstance = useReactFlow();
  const [matrixResult, setMatrixResult] = useState({ same: null, accuracy: null });

  const [images, setImages] = useState({
    mainPuzzle: '',
    correctOutput: '',
    generatedOutput: ''
  });







  const handleSubmit = async (e) => {
    setIsExpanded(true);
    e.preventDefault();
    fetch('http://localhost:5020/solve_arc', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(data => {
        console.log("Solve ARC result:", data);
      })
      .catch(error => {
        console.error('Error during solve_arc:', error);
      });
  };
  const onNodesChange = (changes) => {
    dispatch({
      type: 'UPDATE_NODES',
      payload: applyNodeChanges(changes, state.nodes)
    });
  };

  const onEdgesChange = (changes) => {
    dispatch({
      type: 'UPDATE_EDGES',
      payload: applyEdgeChanges(changes, state.edges)
    });
  };





  useEffect(() => {
    const handleUpdate = (data) => {
      console.log('Received update:', data);
      const newNode = {
        id: data.id,
        type: data.type,
        data: data.imageUrl ? { imageUrl: data.imageUrl } : { label: data.label, title: data.title },

      };

      const newEdge = data.parentId ? { id: `${data.parentId}-${data.id}`, source: data.parentId, target: data.id, animated: true } : null;

      dispatch({ type: 'ADD_NODE_AND_EDGE', payload: { newNode, newEdge } });

      reactFlowInstance.fitView();

    };

    socket.on('update', handleUpdate);

    setIsLoaded(true);


    return () => {
      socket.off('update', handleUpdate);
    };
  }, []);

  useEffect(() => {
    const handlePuzzleUpdate = (data) => {
      console.log('Received update:', data);

      reactFlowInstance.fitView();

      setImages({
        mainPuzzle: data.mainPuzzle,
        correctOutput: data.correctOutput,
        generatedOutput: data.generatedOutput
      });

    };

    socket.on('puzzleupdate', handlePuzzleUpdate);

    setIsLoaded(true);


    return () => {
      socket.off('puzzleupdate', handlePuzzleUpdate);
    };
  }, []);

  useEffect(() => {
    const handleMatrixUpdate = (data) => {
      console.log('Received matrix update:', data);
      // Update state with the new matrix comparison result.
      setMatrixResult({
        same: data.same,
        accuracy: data.accuracy
      });
    };

    // Listen for the 'matrixupdate' event.
    socket.on('matrixupdate', handleMatrixUpdate);

    // Cleanup listener on unmount.
    return () => {
      socket.off('matrixupdate', handleMatrixUpdate);
    };
  }, []);

  useEffect(() => {
    // Listen for the test updates from the backend
    socket.on('testUpdate', (data) => {
      const { nodeId, passedTests, totalTests } = data;

      // Update the specific node with the new test data
      dispatch({
        type: 'UPDATE_NODE_TESTS',
        payload: {
          nodeId,
          passedTests,
          totalTests
        }
      });
    });

    return () => {
      socket.off('testUpdate');
    };
  }, []);



  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'row', backgroundColor: '#f4f4f9' }}>
        {/* Left Section - 50% */}
        <div className="w-1/2 h-full border-r border-gray-100">
          {/* Main Container */}
          <div className="h-full flex flex-col">
            {/* Status Bar */}
            <div className="px-6 py-3 bg-gray-50 border-b border-gray-100 flex justify-between items-center">
              <div className="flex items-center space-x-4">
                <div className="flex items-stretch bg-gray-100 rounded-2xl py-1 px-3">
                  {/* Emoji Container */}
                  <div className="flex items-center justify-center w-12">
                    <span
                      role="img"
                      aria-label="bushy tree"
                      style={{ fontSize: '2.5rem' }}
                    >
                      🌳
                    </span>
                  </div>
                  {/* Text Block */}
                  <div className="ml-4">
                    <div className="atari-text text-xl">Trees Of</div>
                    <div className="atari-text text-xl" style={{ color: '#E53AA3' }}>ARC</div>
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-500">Accuracy:</span>
                  <span className="text-sm font-medium text-gray-700">{matrixResult.accuracy != null ? matrixResult.accuracy : '-'}</span>
                </div>
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${matrixResult.same === "Correct" ? "bg-green-50 text-green-600" : "bg-red-50 text-red-600"}`}>
                {matrixResult.same || '-'}
                </span>
              </div>
            </div>

            {/* Content Grid */}
            <div className="flex-1 p-6 grid grid-cols-2 gap-6">
              {/* Left Side - Main Puzzle */}
              <div className="space-y-3">
                <p className="text-sm text-gray-500">Main Puzzle</p>
                <div className="bg-gray-50 rounded-lg p-4">
                  <img
                    src={
                      images.mainPuzzle && images.mainPuzzle.trim().length > 0
                        ? images.mainPuzzle
                        : "https://dummyimage.com/400x300/eeeeee/eeeeee.png"
                    }
                    alt="Main Puzzle"
                    className="w-full rounded-md"
                  />
                </div>
              </div>

              {/* Right Side - Outputs */}
              <div className="space-y-4">
                {/* Correct Output */}
                <div>
                  <p className="text-sm text-gray-500 mb-2">Correct Output</p>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <img
                      src={
                        images.correctOutput && images.correctOutput.trim().length > 0
                          ? images.correctOutput
                          : "https://dummyimage.com/400x300/eeeeee/eeeeee.png"
                      }
                      alt="Correct Output"
                      className="w-full rounded-md"
                    />
                  </div>
                </div>

                {/* Generated Output */}
                <div>
                  <p className="text-sm text-gray-500 mb-2">Generated Output</p>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <img
                      src={
                        images.generatedOutput && images.generatedOutput.trim().length > 0
                          ? images.generatedOutput
                          : "https://dummyimage.com/400x300/eeeeee/eeeeee.png"
                      }
                      alt="Generated Output"
                      className="w-full rounded-md"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Footer with Button */}
            <div className="p-6 border-t border-gray-100 flex justify-center">
              <button
                onClick={handleSubmit}
                className="flex items-center space-x-2 bg-purple-50 text-purple-600 px-6 py-3 rounded-lg 
                     transition-colors duration-300 hover:bg-purple-100 focus:outline-none focus:ring-2 
                     focus:ring-purple-200 focus:ring-offset-2"
              >
                <span className="text-sm font-medium">Random Puzzle</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Right Section - 50% */}
        <Box sx={{ width: '50%', height: '100%', p: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#f9fafc' }}>
          <ReactFlowProvider>
            <ReactFlow
              nodes={state.nodes}
              edges={state.edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              nodeTypes={nodeTypes}
              connectionLineType={ConnectionLineType.SmoothStep}
              fitView
              minZoom={0.1}
            >
              <Background variant="dots" color="#000000" gap={20} />
              <Controls />
            </ReactFlow>
          </ReactFlowProvider>
        </Box>
      </Box>
    </ThemeProvider>

  );
}

function ARCFlowWithProvider(props) {
  return (
    <ReactFlowProvider>
      <App {...props} />
    </ReactFlowProvider>
  );
}

export default ARCFlowWithProvider;
