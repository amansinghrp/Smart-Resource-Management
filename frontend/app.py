from flask import Flask, request, jsonify, render_template
from system import System

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_deadlock():
    data = request.get_json()

    processes = data['processes']
    resources = data['resources']
    allocation = data['allocation']
    maximum = data['maximum']
    available = data['available']

    try:
        system = System(processes, resources, allocation, maximum, available)
        safe = system.is_safe()

        if safe:
            return jsonify({"message": "✅ System is in a safe state."})
        else:
            return jsonify({"message": "⚠️ Deadlock detected!"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)