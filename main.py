from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)

conn_str = "mysql://root:CSET155@localhost:3307/cset160Final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/')
def greeting():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            conn.execute(text('insert into user (firstName, lastName, email, password, type) values (:firstName, :lastName, :email, :password, :type)'), request.form)
            conn.commit()
            return render_template('register.html', error=None, success="Data inserted successfully!")
        except:
            return render_template('register.html', error="Failed", success=None)
    return render_template('register.html')

@app.route('/accounts', methods=['GET', 'POST'])
def get_accounts():
    user_choice = request.args.get("type")
    print(user_choice)
    accounts = conn.execute(text('select * from user')).all()
    return render_template("accounts.html", accounts=accounts)

if __name__ == '__main__':
    app.run(debug=True)