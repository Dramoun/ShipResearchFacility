import React, { useState, useEffect } from 'react';
import { Box, Button } from '@mui/material';

interface GridProps {
  rows: number;
  cols: number;
  cellSize: number;
  activeCells: Set<string>;
  onCellClick: (row: number, col: number) => void;
}

const Grid: React.FC<GridProps> = ({ rows, cols, cellSize, activeCells, onCellClick }) => {
  return (
    <Box
      display="flex"
      flexWrap="wrap"
      width="80vw"
      height="80vh"
      justifyContent="center"
      alignItems="center"
      style={{ position: 'relative' }}
    >
      {Array.from(activeCells).map((cellKey) => {
        const [row, col] = cellKey.split(',').map(Number);
        return (
          <Box
            key={cellKey}
            onClick={() => onCellClick(row, col)}
            sx={{
              position: 'absolute',
              top: `${row * cellSize}px`,
              left: `${col * cellSize}px`,
              width: `${cellSize}px`,
              height: `${cellSize}px`,
              backgroundColor: 'grey.300',
            }}
          />
        );
      })}
    </Box>
  );
};

const App: React.FC = () => {
  const containerWidth = 80; // in viewport width units (vw)
  const containerHeight = 80; // in viewport height units (vh)
  const cellSize = 20; // in pixels (adjustable)

  // Calculate the number of rows and columns based on available space
  const rows = Math.floor((containerHeight / 100) * window.innerHeight / cellSize);
  const cols = Math.floor((containerWidth / 100) * window.innerWidth / cellSize);

  const [activeCells, setActiveCells] = useState<Set<string>>(new Set());

  // Function to generate random active cells
  const generateRandomCells = () => {
    const newActiveCells = new Set<string>();
    const totalCells = rows * cols;
    const numberOfCellsToActivate = Math.floor(Math.random() * totalCells);
    
    // Randomly activate some cells
    for (let i = 0; i < numberOfCellsToActivate; i++) {
      const row = Math.floor(Math.random() * rows);
      const col = Math.floor(Math.random() * cols);
      newActiveCells.add(`${row},${col}`);
    }
    return newActiveCells;
  };

  // Handle cell click to toggle cell state (alive or dead)
  const handleCellClick = (row: number, col: number) => {
    const cellKey = `${row},${col}`;
    setActiveCells((prevActiveCells) => {
      const newActiveCells = new Set(prevActiveCells);
      if (newActiveCells.has(cellKey)) {
        newActiveCells.delete(cellKey);  // Remove if already active (dead)
      } else {
        newActiveCells.add(cellKey);  // Add if dead (alive)
      }
      return newActiveCells;
    });
  };

  // Initialize random cells when the component mounts
  useEffect(() => {
    setActiveCells(generateRandomCells());
  }, [rows, cols]);

  // Handle the random regeneration of cells on button click
  const handleRandomRegenerate = () => {
    setActiveCells(generateRandomCells());
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
      bgcolor="white"
    >
      <h1>Testing grid</h1>
      <Grid rows={rows} cols={cols} cellSize={cellSize} activeCells={activeCells} onCellClick={handleCellClick} />
      <Button
        variant="contained"
        color="primary"
        onClick={handleRandomRegenerate}
        sx={{ marginTop: 2 }}
      >
        Random Regenerate
      </Button>
    </Box>
  );
};

export default App;
