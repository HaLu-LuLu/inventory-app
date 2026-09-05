from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        name = request.form.get("name")
        category = request.form.get("category")
        stock = request.form.get("stock")
        price = request.form.get("price")


        with open("items.txt", "a", encoding="utf-8") as f:
            f.write(f"{name},{category},{stock},{price}\n")

        return redirect(url_for("index"))

    with open("items.txt", "r", encoding="utf-8") as f:
        items = f.readlines()

    search = request.args.get("search", "")
    category = request.args.get("category", "")

    if search:
        filtered_items = []

        for item in items:
            if search in item:
                filtered_items.append(item)

        items = filtered_items

    if category:
        filtered_items = []

        for item in items:
            data = item.split(",")

            if data[1] == category:
                filtered_items.append(item)

        items = filtered_items

    new_items = []

    for item in items:
        data = item.split(",")
        new_items.append(data)


    return render_template("index.html", items=new_items, search=search, category=category)

@app.route("/delete/<int:index>")
def delete(index):

    with open("items.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    del lines[index]

    with open("items.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

    return redirect(url_for("index"))


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):

    if request.method == "POST":

        name = request.form.get("name")
        category = request.form.get("category")
        stock = request.form.get("stock")
        price = request.form.get("price")

        with open("items.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        lines[index] = f"{name},{category},{stock},{price}\n"

        with open("items.txt", "w", encoding="utf-8") as f:
            f.writelines(lines)

        return redirect(url_for("index"))

    with open("items.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    item = lines[index].strip().split(",")

    return render_template("edit.html", item=item, index=index)

        

if __name__ == "__main__":
    app.run(debug=True)