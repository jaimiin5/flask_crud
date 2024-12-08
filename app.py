from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("get_data"))


@app.route("/api/create", methods=["POST"])
def create_Account():

    if request.method == "POST":
        ac_no = request.form.get("acc_number")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        city = request.form.get("city")
        amount = request.form.get("amount")

        if not ac_no or not first_name or not last_name or not city:
            return jsonify({"error": "All fields are required!"}), 400

        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="jaimin",
                password="root",
                host="localhost",
                port="5432",
            )

            cur = conn.cursor()
            post_query = "INSERT INTO accounts (ac_no, first_name, last_name, city, amount) VALUES (%s, %s, %s, %s, %s)"
            value = (ac_no, first_name, last_name, city, amount)
            cur.execute(post_query, value)

            conn.commit()

            return jsonify({"message": "Account added successfully!"}), 201

        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500

        finally:
            cur.close()
            conn.close()


@app.route("/api/read", methods=["GET"])
def get_data():

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="jaimin",
            password="root",
            host="localhost",
            port="5432",
        )

        cur = conn.cursor()
        get_query = "SELECT * FROM accounts"
        cur.execute(get_query)
        data = cur.fetchall()

        conn.commit()

        return render_template("index.html", data=data)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

    finally:
        cur.close()
        conn.close()


@app.route("/api/delete/<int:ac_id>", methods=["DELETE"])
def delete_data(ac_id):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="jaimin",
            password="root",
            host="localhost",
            port="5432",
        )
        cur = conn.cursor()
        print("heheheh???", ac_id)
        delete_query = "DELETE FROM accounts WHERE id = %s"
        cur.execute(delete_query, (ac_id,))

        conn.commit()

        return jsonify({"message": "data deleted Successfully"}), 201

    except Exception as e:
        return f"error {e}"

    finally:
        conn.close()
        cur.close()


@app.route("/api/single/<int:ac_id>", methods=["GET"])
def single_data(ac_id):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="jaimin",
            password="root",
            host="localhost",
            port="5432",
        )
        cur = conn.cursor()
        single_query = "SELECT * FROM accounts WHERE id = %s"
        cur.execute(single_query, (ac_id,))
        data = cur.fetchall()

        conn.commit()

        return jsonify({"data": data}), 200

    except Exception as e:
        return f"error {e}"

    finally:
        conn.close()
        cur.close()


@app.route("/api/update/<int:ac_id>", methods=["PUT"])
def update_data(ac_id):
    ac_no = request.form.get("acc_number")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    city = request.form.get("city")
    amount = request.form.get("amount")
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="jaimin",
            password="root",
            host="localhost",
            port="5432",
        )
        cur = conn.cursor()
        update_query = """UPDATE accounts SET 
        ac_no = %s,
        first_name = %s,
        last_name = %s,
        city = %s  ,
        amount = %s,
        WHERE id = %s
        """
        value = (ac_no, first_name, last_name, city, amount, ac_id)
        cur.execute(update_query, value)
        data = cur.fetchall()

        conn.commit()

        return jsonify({"data": data}), 200

    except Exception as e:
        return f"error {e}"

    finally:
        conn.close()
        cur.close()


if __name__ == "__main__":
    app.run(debug=True)
