from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# 👉 Railway даёт DATABASE_URL автоматически
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔥 ВАЖНО: защита от падения если БД не подключилась
def get_conn():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL is not set")
    return psycopg2.connect(DATABASE_URL)

# ---------------------------
# GET all items
# ---------------------------
@app.route("/api/data", methods=["GET"])
def get_data():
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT id, name FROM items;")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        # форматируем нормально в JSON
        result = [{"id": r[0], "name": r[1]} for r in rows]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# POST add item
# ---------------------------
@app.route("/api/data", methods=["POST"])
def add_data():
    try:
        data = request.json

        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO items (name) VALUES (%s)",
            (data["name"],)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "added"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# DELETE item
# ---------------------------
@app.route("/api/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("DELETE FROM items WHERE id=%s", (id,))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "deleted"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# IMPORTANT FOR RAILWAY
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 🔥 FIX FOR RAILWAY
    app.run(host="0.0.0.0", port=port)
