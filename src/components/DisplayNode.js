import React, { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function DisplayNode({ data, isConnectable }) {
  const onScroll = useCallback((evt) => {
    evt.stopPropagation();
  }, []);

  return (
    <div

      className="nowheel"

      style={{
        width: '600px',
        height: '400px',
        border: '1px solid #ccc',
        borderRadius: '8px',
        background: "#FAF9F6",
        display: 'flex',
        flexDirection: 'column',
      }}>
      <Handle
        type="target"
        position={Position.Top}
        isConnectable={isConnectable}
      />
      <div style={{
        padding: '10px',
        borderBottom: '1px solid #ccc',
        fontWeight: 'bold',
        flexShrink: 0  // Prevent header from shrinking
      }}>
        Answer:
      </div>
      <div
        style={{
          padding: '10px',
          background: "white",
          flexGrow: 1,     // Take remaining space
          overflow: 'auto', // Enable scrolling
          height: 0,       // Force container to scroll
        }}
        onScroll={onScroll}
      >
        <div style={{
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-word',
        }}>
          {data.label}
        </div>
      </div>
      <Handle
        type="source"
        position={Position.Bottom}
        id="b"
        isConnectable={isConnectable}
      />
    </div>
  );
}

export default DisplayNode;