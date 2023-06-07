from flask import Flask,request, render_template,session
from flask_mysqldb import MySQL,MySQLdb



app = Flask(__name__)

app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_DB']= "flask"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= "Kumar321@"
app.config['MYSQL_CURSORCLASS']="DictCursor"
app.secret_key="myapp"
conn = MySQL(app)
@app.route('/')
def welcome():
     return render_template('welcomepage.html')


@app.route('/login', methods = ['POST', 'GET'])
def signin():
    if request.method  == 'POST':
        username = request.form['username']
        password = request.form['password']
        con=conn.connection.cursor()
        sql = "select username, password from signup WHERE username= %s and  password=%s"
        result=con.execute(sql,(username,password))
        con.connection.commit()
        con.close()
        
        if result:
            return render_template('booking.html')
        else:
            return render_template('login.html')
            
        
    return render_template('login.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method  == 'POST':
        username = request.form['username']
        password = request.form['password']
        email=request.form['email']
        con=conn.connection.cursor()
        try:
            sql = "insert into signup(email,username,password) values  (%s,%s,%s)"
            con.execute(sql,(email,username,password))
            con.connection.commit()
            con.close()
            msg1='<p style="color:green;">Signup successful</p>'
            return  render_template('login.html', msg=msg1)
        except MySQLdb.IntegrityError:
            return render_template('signup.html', msg='<p style="color:red;">Username already exists.Please choose another username</p>')
            
    return render_template('signup.html')

@app.route('/booking', methods = ['GET','POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        start = request.form['start']
        end = request.form['end']
        date = request.form['date']
        time = request.form['time']
        seats = request.form['seats']
        con = conn.connection.cursor()
        sql = "insert into booking (name,email,phone,start,end,date,time,seats) values (%s,%s,%s,%s,%s,%s,%s,%s)"
        con.execute(sql,(name,email,phone,start,end,date,time,seats))
        con.connection.commit()
        con.close()
        con=conn.connection.cursor()
        sql="select * from  booking WHERE name = %s"
        con.execute(sql,(name,))
        result= con.fetchall()
        con.connection.commit()   
        session['name']=name 
        if result:
            return render_template('viewdata.html', mes='<p style="color:darkblue;">Booking successful</p>',data=result)
        else:
            return render_template('booking.html',mes='<p>Please enter the correct details</p>')
    return render_template('booking.html')

@app.route('/viewdata', methods = ['GET'])
def viewdata():
    name = session.get('name')
    con=conn.connection.cursor()
    sql="select * from  booking WHERE name = %s"
    con.execute(sql,(name,))
    result= con.fetchall()
    con.connection.commit()    
   
    if result:
        return render_template('viewdata.html', mes='<p>Booking successful</p>',data=result)
    else:
        return render_template('booking.html',mes='<p>Please enter the correct details</p>')
@app.route('/forget')
def forget():
    return render_template('forgotpassword.html')
        
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')
 
if __name__ =='__main__':
    app.run(debug=True)