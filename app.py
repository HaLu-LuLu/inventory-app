import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    error = ""
    name = ""
    stock = ""
    price = ""
    form_category = ""

    if request.method == "POST":

        name = request.form.get("name")
        form_category = request.form.get("category")
        stock = request.form.get("stock")
        price = request.form.get("price")

        if not name:
            error = "商品名を入力してください"
        
        elif not stock:
            error = "在庫を入力してください"

        elif int(stock) < 0:
            error = "在庫数は0以上で入力してください"
        
        elif not price:
            error = "価格を入力してください"


        elif int(price) < 0:
            error = "価格は0以上で入力してください"

        if not error:
            conn = sqlite3.connect("items.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO items (name, category, stock, price) VALUES (?, ?, ?, ?)",
                (name, form_category, stock, price)
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

    return render_template("index.html", items=items, search=search, category=category, error=error, name=name, stock=stock, price=price, form_category=form_category)

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

    error = ""

    if request.method == "POST":

        name = request.form.get("name")
        category = request.form.get("category")
        stock = request.form.get("stock")
        price = request.form.get("price")

        if not name:
            error = "商品名を入力してください"
        
        elif not stock:
            error = "在庫を入力してください"

        elif int(stock) < 0:
            error = "在庫数は0以上で入力してください"
        
        elif not price:
            error = "価格を入力してください"


        elif int(price) < 0:
            error = "価格は0以上で入力してください"

        if not error:
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
        
        item = (name, category, stock, price)

    else:
        conn = sqlite3.connect("items.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name, category, stock, price FROM items WHERE id =?",
            (index,)
        )
        item = cursor.fetchone()

        conn.close()

    return render_template("edit.html", item=item, index=index, error=error)

        

if __name__ == "__main__":
    app.run(debug=True)