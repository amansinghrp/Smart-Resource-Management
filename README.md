⚙️ Smart Resource Management & Deadlock Handling in OS

📝 Description
    This project is a simulation of Smart Resource Management in Operating Systems, focusing on:
    Efficient resource allocation
    Deadlock detection and prevention
    It implements algorithms like the Banker’s Algorithm, Resource Allocation Graph (RAG), and Wait-For Graph (WFG) to model and resolve process-resource interactions. The project also features a web-based visualizer for easy understanding and interaction.

💡 Features
    🧠 Simulates multiple processes and resource types
    🔐 Implements Banker’s Algorithm for safe resource allocation
    🕸 Generates Resource Allocation Graph (RAG)
    🔄 Converts RAG to Wait-for Graph (WFG) for deadlock detection
    ❌ Detects and prevents deadlocks
    🌐 Web-based frontend for interactive simulations
    🛠️ Deadlock Recovery Module:
        Suggests a process to terminate in case of a deadlock
        Recalculates the safe sequence after removal

🧰 Technologies Used
    Languages:
        Python
        JavaScript (for frontend)

    Tools & Libraries:
        Flask – Backend web framework
        Matplotlib / NetworkX – For graph visualization
        Jinja2 – HTML templating
        unittest / pytest – For unit testing

🛠 Installation Instructions

    1. Clone the Repository
        git clone https://github.com/amansinghrp/Smart-Resource-Management.git
        cd Smart-Resource-Management

    2. Create Virtual Environment (Optional but Recommended)
        python3 -m venv venv
        source venv/bin/activate

    3. Install Dependencies
        pip install -r requirements.txt

⚙ Usage
    ➤ Run the Visualizer
        cd frontend
        python3 app.py
    Opens a local web server at http://127.0.0.1:5000
    Users can define the number of processes/resources and request matrix
    Graphical output includes RAG and WFG
    Output also includes banker’s decision and deadlock status

🗃 Project Structure
    Smart-Resource-Management/
    ├── core/                  # Core logic modules
    │   ├── banker.py
    │   ├── process.py
    │   ├── resource.py
    │   ├── rag.py
    │   ├── wfg.py
    │   ├── system.py
    │
    ├── frontend/              # Web visualizer
    │   ├── app.py             # Flask entry point
    │   ├── static/            # Contains generated graph images
    │   ├── templates/
    │   │   └── index.html     # Frontend UI
    │
    ├── tests/                 # Unit tests for all modules
    │   ├── test_process.py
    │   ├── test_resource.py
    │   ├── test_system.py
    │   ├── test_bankers.py
    │   └── test_deadlock.py
    │
    ├── utils/
    │   └── helpers.py         # Utility functions
    │
    ├── requirements.txt
    ├── README.md
    └── .gitignore

📄 Example Scenario
    Input:
        5 Processes, 3 Resources
        Allocation & Request matrices defined on UI

    Output:
        graph.png: Resource Allocation Graph
        rag.png: Wait-for Graph
        Banker’s Decision: Safe/Unsafe
        Deadlock Detected: Yes/No

🧪 Tests
    Run all unit tests with:
        cd tests
        pytest
    Or  
    using Python directly:
        python3 -m unittest discover

🧠 Roadmap
    Banker’s Algorithm
    Deadlock Detection via WFG
    RAG to WFG Transformation
    Web UI with Graph Visuals
    Add support for dynamic resource allocation
    Real-time simulation and animation
    Add performance statistics and history tracking