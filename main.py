from flask import Flask, render_template, request, redirect
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
    success = ""
    error = ""
    if request.method == 'POST':
        try:
            conn.execute(text('insert into test values (:testId, :q1, :q2, :q3, :userName)'), request.form)
            conn.commit()
            success="Data inserted successfully!"
            error=None
        except:
            success=None
            error="Failed"
    accounts = conn.execute(text('select * from user where type = "Teacher"')).all()
    return render_template("create_test.html", accounts=accounts, success=success, error=error)

@app.route('/viewTest', methods=['GET', 'POST'])
def viewTest():
    tests = conn.execute(text('select * from test')).all()
    return render_template("viewTest.html", tests=tests)

@app.route('/editTest/<testId>', methods=['GET', 'POST'])
def editTest(testId):
    success = ""
    error = ""
    if request.method == 'POST':
        try:
            conn.execute(
                text(f'update test set q1 = :q1, q2 = :q2, q3 = :q3, userName = :userName where testId = "{testId}"'), 
                request.form)
            conn.commit()
            success="Data inserted successfully!"
            error=None
        except:
            success=None
            error="Failed"
    editTest = conn.execute(text(f'select * from test where testId = "{testId}"')).one()
    accounts = conn.execute(text('select * from user where type = "Teacher"')).all()
    return render_template("editTest.html", editTest=editTest, accounts=accounts, success=success, error=error)

@app.route('/deleteTest/<testId>')
def deleteTest(testId):
    conn.execute(text(f'delete from test where testId = "{testId}"'))
    conn.commit()
    return redirect("/viewTest")

@app.route('/takeTest/<testId>', methods=['GET', 'POST'])
def takeTest(testId):
    success = ""
    error = ""
    if request.method == 'POST':
        try:
            conn.execute(
                text(f'insert into answer (q1, q2, q3, userName, testId) values (:q1, :q2, :q3, :userName, "{testId}")'), 
                request.form)
            conn.commit()
            success="Data inserted successfully!"
            error=None
        except:
            success=None
            error="The student has already completed the test."
    takeTest = conn.execute(text(f'select * from test where testId = "{testId}"')).one()
    accounts = conn.execute(text('select * from user where type = "Student"')).all()
    return render_template("takeTest.html", takeTest=takeTest, accounts=accounts, success=success, error=error)

@app.route('/viewAnswer', methods=['GET', 'POST'])
def viewAnswer():
    if request.method == 'POST':
        user_choice = request.form["testId"]
        answers =  conn.execute(text(f'select * from answer where testId ="{user_choice}"')).all() 
        testIds = conn.execute(text(f'select distinct testId from answer')).all()
        return render_template("viewResponse.html", answers=answers, testIds=testIds)
    testIds = conn.execute(text(f'select distinct testId from answer')).all()
    return render_template("viewResponse.html", testIds=testIds)

if __name__ == '__main__':
    app.run(debug=True)