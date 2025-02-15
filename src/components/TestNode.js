import React from 'react';
import { Handle, Position } from 'reactflow';
import { TestTube2 } from 'lucide-react';

const TestNode = ({ data }) => {
  return (
    <div className="bg-accent text-accent-foreground rounded-lg shadow-md p-4 border border-accent w-48">
      <Handle type="target" position={Position.Top} className="w-3 h-3" />
      <div className="flex items-center mb-2">
        <TestTube2 className="w-5 h-5 mr-2" />
        <h3 className="text-lg font-semibold">Tests</h3>
      </div>
      <p className="text-sm font-medium text-center">
        {data.description}
      </p>
      <Handle type="source" position={Position.Bottom} className="w-3 h-3" />
    </div>
  );
};

export default TestNode; 