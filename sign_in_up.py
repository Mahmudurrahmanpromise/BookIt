from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)

conn = MySQLdb.connect(host="localhost", user= "root", password= "promise12", db = "bookit_db")

@app.route("/")
def index():
    return render_template("index.html", title="SignUP")


@app.route("/signUp", methods=["POST"])
def signUp():
    username = str(request.form["user"])
    password = str(request.form["password"])
    email = str(request.form["email"])
    nid = str(request.form["nid"])
    location = str(request.form["location"])

    cursor = conn.cursor()

    cursor.execute("INSERT INTO user (username,password,email,nid_number,location)VALUES(%s,%s,%s,%s,%s)",
                   (username, password, email,nid,location))
    conn.commit()
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home_login.html")


@app.route("/checkuser", methods=["POST"])
def checkuser():
    user_email = str(request.form["email"])
    password = str(request.form["password"])

    cursor = conn.cursor()
    cursor.execute("SELECT password FROM user WHERE email LIKE %s", (user_email,))
    user_password = cursor.fetchone()
    x = user_password[0]

    if (password == x) :

         return redirect(url_for("posts"))
    else :

        return redirect(url_for("loginerror"))
    

@app.route("/post-entry/",methods=["POST"])
def post_entry():
    if request.method=='POST':
        data = request.form.to_dict()
        print(data['bookname'])
        print(data['author'])
        print(data['location'])

        cursor = conn.cursor()

        cursor.execute("INSERT INTO post (name,author,location)VALUES(%s,%s,%s)",
                       (data['bookname'],data['author'],data['location']))
        conn.commit()
        return redirect("/")


@app.route("/posts/")
def posts():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM post")
    books = cursor.fetchall()

    return render_template("posts.html",**locals())

@app.route("/loginerror")
def loginerror():
        return render_template("loginerror.html")

@app.route("/userprofile")
def userprofile():
        return render_template("posts.html")




if __name__ == "__main__":
    app.run(debug=True)
