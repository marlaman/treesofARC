import React, { useCallback } from 'react';
import { Handle, Position } from 'reactflow';

function FinetuneNode({ data, isConnectable }) {
  const onScroll = useCallback((evt) => {
    evt.stopPropagation();
  }, []);

  return (
    <div className="nowheel" style={{
      width: '600px',
      border: '1px solid #ccc',
      borderRadius: '8px',
      background: "#FDC959",
      // overflow: 'hidden',
      display: 'flex',
      overflowY: 'auto',
      maxHeight: '500px',
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
      }}>
        Finetuned Output
      </div>
      <div
        style={{
          flex: 1,
          padding: '10px',
          overflowY: 'auto',
          background: "white",
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

export default FinetuneNode;