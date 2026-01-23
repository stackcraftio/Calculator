from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/calc")
def api_calc():
    data = request.get_json(force=True)
    expr = (data.get("expr") or "").strip()
    expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")

    # VERY simple safety: allow only digits, spaces, dot, and basic operators incl % and parentheses
    allowed = set("0123456789.+-*/()% ")
    if not expr or any(ch not in allowed for ch in expr):
        return jsonify(result="Error")

    try:
        # Convert percent: 50% -> (50/100)
        # This is simple and works inside expressions.
        expr = convert_percent(expr)

        # Evaluate in restricted environment (no builtins)
        result = eval(expr, {"__builtins__": {}}, {})
        return jsonify(result=result)
    except ZeroDivisionError:
        return jsonify(result="Cannot divide by 0")
    except Exception:
        return jsonify(result="Error")


def convert_percent(expr: str) -> str:
    """
    Converts percent patterns like:
      50%   -> (50/100)
      12.5% -> (12.5/100)
    Works anywhere inside expression.
    """
    out = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]
        if ch.isdigit() or ch == ".":
            # read full number
            j = i
            dot_count = 0
            while j < n and (expr[j].isdigit() or expr[j] == "."):
                if expr[j] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        break
                j += 1

            number = expr[i:j]

            # if immediately followed by % -> wrap
            if j < n and expr[j] == "%":
                out.append(f"({number}/100)")
                i = j + 1
            else:
                out.append(number)
                i = j
        else:
            out.append(ch)
            i += 1

    return "".join(out)


if __name__ == "__main__":
    app.run(debug=True)
