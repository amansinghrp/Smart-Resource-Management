let canvas = document.getElementById("graphCanvas");
let ctx = canvas.getContext("2d");

let nodes = [];
let edges = [];

let processCount = 0;
let resourceCount = 0;

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw edges
  edges.forEach(edge => {
    ctx.beginPath();
    ctx.moveTo(edge.from.x, edge.from.y);
    ctx.lineTo(edge.to.x, edge.to.y);
    ctx.strokeStyle = edge.type === "request" ? "blue" : "black";
    ctx.stroke();

    // Arrowhead
    let dx = edge.to.x - edge.from.x;
    let dy = edge.to.y - edge.from.y;
    let angle = Math.atan2(dy, dx);
    let arrowLength = 10;

    ctx.beginPath();
    ctx.moveTo(edge.to.x, edge.to.y);
    ctx.lineTo(edge.to.x - arrowLength * Math.cos(angle - 0.3), edge.to.y - arrowLength * Math.sin(angle - 0.3));
    ctx.lineTo(edge.to.x - arrowLength * Math.cos(angle + 0.3), edge.to.y - arrowLength * Math.sin(angle + 0.3));
    ctx.closePath();
    ctx.fillStyle = edge.type === "request" ? "blue" : "black";
    ctx.fill();
  });

  // Draw nodes
  nodes.forEach(node => {
    ctx.beginPath();
    ctx.fillStyle = node.type === "process" ? "#2ecc71" : "#e67e22";
    ctx.arc(node.x, node.y, 20, 0, 2 * Math.PI);
    ctx.fill();
    ctx.fillStyle = "white";
    ctx.textAlign = "center";
    ctx.fillText(node.label, node.x, node.y + 5);
  });
}

function addProcess() {
  processCount++;
  nodes.push({
    label: `P${processCount}`,
    type: "process",
    x: 100 + processCount * 80,
    y: 100
  });
  draw();
}

function addResource() {
  resourceCount++;
  nodes.push({
    label: `R${resourceCount}`,
    type: "resource",
    x: 100 + resourceCount * 80,
    y: 300
  });
  draw();
}

function addRequest() {
  let fromLabel = prompt("Process (e.g., P1):");
  let toLabel = prompt("Resource (e.g., R1):");

  let from = nodes.find(n => n.label === fromLabel);
  let to = nodes.find(n => n.label === toLabel);

  if (from && to) {
    edges.push({ from, to, type: "request" });
    draw();
  } else {
    alert("Invalid node labels!");
  }
}

function addAllocation() {
  let fromLabel = prompt("Resource (e.g., R1):");
  let toLabel = prompt("Process (e.g., P1):");

  let from = nodes.find(n => n.label === fromLabel);
  let to = nodes.find(n => n.label === toLabel);

  if (from && to) {
    edges.push({ from, to, type: "allocation" });
    draw();
  } else {
    alert("Invalid node labels!");
  }
}

function checkDeadlock() {
  // Build an adjacency list from the edges
  let adjacency = {};

  nodes.forEach(node => {
    adjacency[node.label] = [];
  });

  edges.forEach(edge => {
    adjacency[edge.from.label].push(edge.to.label);
  });

  // Cycle detection using DFS
  let visited = {};
  let recStack = {};

  function isCyclic(nodeLabel) {
    if (!visited[nodeLabel]) {
      visited[nodeLabel] = true;
      recStack[nodeLabel] = true;

      for (let neighbor of adjacency[nodeLabel]) {
        if (!visited[neighbor] && isCyclic(neighbor)) {
          return true;
        } else if (recStack[neighbor]) {
          return true;
        }
      }
    }

    recStack[nodeLabel] = false;
    return false;
  }

  for (let node of nodes) {
    if (isCyclic(node.label)) {
      alert("⚠️ Deadlock detected!");
      return;
    }
  }

  alert("✅ No deadlock detected.");
}
