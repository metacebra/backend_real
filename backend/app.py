from flask import Flask, request, jsonify
from qiskit import QuantumCircuit, Aer, execute

app = Flask(__name__)

seal_map = {
  "00": {"symbol": "Flor de la Vida", "color": "#FFD700"},
  "01": {"symbol": "Cubo de Metatrón", "color": "#0000FF"},
  "10": {"symbol": "Sri Yantra", "color": "#8A2BE2"},
  "11": {"symbol": "Espiral Infinita", "color": "#00FF00"},
}

@app.route("/quantum-seal", methods=["POST"])
def quantum_seal():
  data = request.get_json(force=True) or {}
  intention = data.get("intention", "default")

  qc = QuantumCircuit(2, 2)
  qc.h(0)
  qc.cx(0, 1)
  qc.measure([0, 1], [0, 1])

  simulator = Aer.get_backend("qasm_simulator")
  result = execute(qc, simulator, shots=1).result()
  counts = result.get_counts(qc)
  seal = list(counts.keys())[0]

  payload = {
    "intention": intention,
    "quantum_seal": seal,
    "symbol": seal_map[seal]["symbol"],
    "color": seal_map[seal]["color"],
  }
  return jsonify(payload)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
