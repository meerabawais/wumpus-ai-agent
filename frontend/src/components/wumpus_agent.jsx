import React, { useState } from "react";

export default function WumpusAgent() {
  const [size, setSize] = useState(4);
  const [grid, setGrid] = useState([]);
  const [logs, setLogs] = useState([]);

  // 🚀 INIT WORLD
  async function startGame() {
    await fetch("http://localhost:5000/init", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ size }),
    });

    setGrid(
     Array(size * size).fill({
  status: "UNKNOWN",
  text: "",
})
    );

    setLogs([]);
  }

  // 🎯 MOVE AGENT
  async function handleClick(index) {
  const res = await fetch("http://localhost:5000/move", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ index }),
  });

  const data = await res.json();

  let newGrid = [...grid];

  // 🎯 GAME RESULT
  if (data.status === "LOSE") {
    alert("💀 " + data.reason);
  } else if (data.status === "WIN") {
    alert("🏆 " + data.reason);
  }

  // 🧠 UPDATE CELL
  newGrid[index] = {
    status: data.safe ? "SAFE" : "DANGER",
    text:
      data.status === "WIN"
        ? "🏆"
        : data.status === "LOSE"
        ? "💀"
        : data.breeze
        ? "💨"
        : data.stench
        ? "👃"
        : "✔",
  };

  setGrid(newGrid);

  setLogs((prev) => [
    ...prev,
    `Cell ${index} → Breeze: ${data.breeze}, Stench: ${data.stench}`,
  ]);
}
    return (
  <div className="min-h-screen bg-gradient-to-br from-indigo-100 to-blue-200 flex flex-col items-center p-6">

    {/* TITLE */}
    <h1 className="text-3xl font-bold text-gray-800 mb-4">
      🧠 Wumpus AI Agent
    </h1>

    {/* CONTROL PANEL */}
    <div className="bg-white shadow-lg rounded-xl p-4 mb-6 flex items-center gap-3">
      <input
        type="number"
        value={size}
        onChange={(e) => setSize(Number(e.target.value))}
        className="border px-3 py-2 rounded-lg w-20 text-center"
      />

      <button
        onClick={startGame}
        className="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-lg shadow"
      >
        🚀 Start Game
      </button>
    </div>

    {/* MAIN CARD */}
    <div className="bg-white shadow-xl rounded-2xl p-6 flex gap-8">

      {/* GRID */}
      <div>
        <h2 className="text-lg font-semibold mb-3 text-gray-700">
          🗺️ Grid
        </h2>

        <div
          className="grid gap-3"
          style={{ gridTemplateColumns: `repeat(${size}, 60px)` }}
        >
          {grid.map((cell, i) => (
            <div
              key={i}
              onClick={() => handleClick(i)}
              className={`w-14 h-14 flex items-center justify-center rounded-lg border cursor-pointer transition transform hover:scale-105
                ${
                  cell.status === "SAFE"
                    ? "bg-green-300"
                    : cell.status === "DANGER"
                    ? "bg-red-400"
                    : "bg-gray-200"
                }`}
            >
              <span className="text-lg">{cell.text}</span>
            </div>
          ))}
        </div>
      </div>

      {/* LOG PANEL */}
      <div className="w-72">
        <h2 className="text-lg font-semibold mb-3 text-gray-700">
          📊 Inference Logs
        </h2>

        <div className="bg-gray-100 rounded-lg p-3 h-72 overflow-y-auto text-sm">
          {logs.length === 0 ? (
            <p className="text-gray-500">No logs yet...</p>
          ) : (
            logs.map((l, i) => (
              <div key={i} className="mb-2 border-b pb-1">
                {l}
              </div>
            ))
          )}
        </div>
      </div>

    </div>

    {/* FOOTER */}

  </div>
);
}