from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)

conn_str = "mysql://root:5676@localhost/cset160Final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def greeting():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            conn.execute(text('insert into user values (:userName, :firstName, :lastName, :email, :password, :type)'), request.form)
            conn.commit()
            return render_template('register.html', error=None, success="Data inserted successfully!")
        except:
            return render_template('register.html', error="Failed", success=None)
    return render_template('register.html')

@app.route('/accounts', methods=['GET', 'POST'])
def get_accounts():
    if request.method == 'POST':
        user_choice = request.form["type"]
        if user_choice == "All":
            accounts = conn.execute(text('select * from user')).all()
            return render_template("accounts.html", accounts=accounts)
        elif user_choice == "Teacher":
            accounts = conn.execute(text('select * from user where type = "Teacher"')).all()
            return render_template("accounts.html", accounts=accounts)
        elif user_choice == "Student":
            accounts = conn.execute(text('select * from user where type = "Student"')).all()
            return render_template("accounts.html", accounts=accounts)
    accounts = conn.execute(text('select * from user')).all()
    return render_template("accounts.html", accounts=accounts)

@app.route('/createTest', methods=['GET', 'POST'])
def createTest():
    if request.method == "POST":
        choice = request.form["id"]
        print(choice)

    accounts = conn.execute(text('select * from user where type = "Teacher"')).all()
    return render_template("create_test.html", accounts=accounts)

if __name__ == '__main__':
    app.run(debug=True)