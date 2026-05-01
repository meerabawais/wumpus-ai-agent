from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
# 🌍 GLOBAL STATE
SIZE = 4
KB = []
PITS = []
WUMPUS = None
GOLD = None        # 🟡 ADD THIS
GAME_OVER = False  # 🟡 ADD THIS

# 🔴 GENERATE WORLD
def generate_world(size):
    global PITS, WUMPUS, GOLD, GAME_OVER

    GAME_OVER = False
    total = size * size

    WUMPUS = random.randint(0, total - 1)

    PITS = []
    while len(PITS) < 3:
        p = random.randint(0, total - 1)
        if p != WUMPUS:
            PITS.append(p)

    # 🟡 GOLD
    while True:
        GOLD = random.randint(0, total - 1)
        if GOLD not in PITS and GOLD != WUMPUS:
            break
# 🔁 ADJACENCY
def is_adjacent(a, b):
    ax, ay = divmod(a, SIZE)
    bx, by = divmod(b, SIZE)
    return (abs(ax - bx) == 1 and ay == by) or (abs(ay - by) == 1 and ax == bx)

# 🌬️ PERCEPTS
def get_percepts(index):
    breeze = any(is_adjacent(index, p) for p in PITS)
    stench = is_adjacent(index, WUMPUS)
    return breeze, stench

# ➖ NEGATION
def negate(l):
    return l[1:] if l.startswith("¬") else "¬" + l

# 🔥 RESOLUTION
def resolution(query):
    clauses = KB + [[negate(query)]]
    new = []

    while True:
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                for lit in clauses[i]:
                    if negate(lit) in clauses[j]:
                        resolvent = list(set(
                            [x for x in clauses[i] if x != lit] +
                            [x for x in clauses[j] if x != negate(lit)]
                        ))

                        if len(resolvent) == 0:
                            return True

                        if resolvent not in clauses:
                            new.append(resolvent)

        if not new:
            return False

        clauses.extend(new)

# 🧠 UPDATE KB (CNF STYLE RULES)
def update_kb(x, y, breeze, stench):
    # percept facts
    if not breeze:
        KB.append([f"¬P_{x}_{y}"])
    else:
        KB.append([f"B_{x}_{y}"])

    if not stench:
        KB.append([f"¬W_{x}_{y}"])
    else:
        KB.append([f"S_{x}_{y}"])

# 📡 API: INIT WORLD
@app.route("/init", methods=["POST"])
def init():
    global SIZE, KB
    data = request.json
    SIZE = data["size"]
    KB = []

    generate_world(SIZE)

    return jsonify({"message": "World initialized"})

# 📡 API: MOVE AGENT
@app.route("/move", methods=["POST"])
def move():
    global GAME_OVER, GOLD, WUMPUS, PITS

    data = request.json or {}
    index = data.get("index", 0)

    # 👇 ADD PRINT HERE
    print("MOVE CALLED:", index, GOLD, WUMPUS, PITS)

    x, y = divmod(index, SIZE)

    breeze, stench = get_percepts(index)

    update_kb(x, y, breeze, stench)

    # 💀 CHECK LOSS
    if index in PITS:
        GAME_OVER = True
        return jsonify({"status": "LOSE", "reason": "Fell into PIT"})

    if index == WUMPUS:
        GAME_OVER = True
        return jsonify({"status": "LOSE", "reason": "Eaten by WUMPUS"})

    # 🟡 CHECK WIN
    if index == GOLD:
        GAME_OVER = True
        return jsonify({"status": "WIN", "reason": "Found GOLD"})

    # 🔍 inference
    pit = resolution(f"P_{x}_{y}")
    wumpus = resolution(f"W_{x}_{y}")

    safe = not pit and not wumpus

    return jsonify({
        "status": "PLAY",
        "safe": safe,
        "breeze": breeze,
        "stench": stench
    })
if __name__ == "__main__":
    app.run(debug=True)
