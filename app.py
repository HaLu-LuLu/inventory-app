import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        name = request.form.get("name")
        category = request.form.get("category")
        stock = request.form.get("stock")
        price = request.form.get("price")

        conn = sqlite3.connect("items.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO items (name, category, stock, price) VALUES (?, ?, ?, ?)",
            (name, category, stock, price)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, category, stock, price FROM items")
    items = cursor.fetchall()

    conn.close()

    search = request.args.get("search", "")
    category = request.args.get("category", "")

    if search:
        filtered_items = []

        for item in items:
            if search in item[1]:
                filtered_items.append(item)

        items = filtered_items

    if category:
        filtered_items = []

        for item in items:
            if item[2] == category:
                filtered_items.append(item)

        items = filtered_items

    return render_template("index.html", items=items, search=search, category=category)

@app.route("/delete/<int:index>")
def delete(index):

    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM items WHERE id = ?",
        (index,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):

    if request.method == "POST":

        name = request.form.get("name")
        category = request.form.get("category")
        stock = request.form.get("stock")
        price = request.form.get("price")

        conn = sqlite3.connect("items.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE items
            SET name = ?, category = ?, stock = ?, price = ?
            WHERE id = ?
            """,
            (name, category, stock, price, index) 
        )
        
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, category, stock, price FROM items WHERE id =?",
        (index,)
    )
    item = cursor.fetchone()

    conn.close()

    return render_template("edit.html", item=item, index=index)

        

if __name__ == "__main__":
    app.run(debug=True)