from flask import Flask,render_template,request,redirect,session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key="abc123"


app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='MYSQL'
app.config['MYSQL_DB']='complaintdb'


mysql=MySQL(app)


@app.route('/')
def home():

    return render_template('login.html')



@app.route('/register',methods=['GET','POST'])

def register():

    if request.method=='POST':

        name=request.form['name']
        email=request.form['email']
        password=request.form['password']


        cur=mysql.connection.cursor()

        cur.execute(
        "insert into students(name,email,password) values(%s,%s,%s)",
        (name,email,password)
        )

        mysql.connection.commit()

        cur.close()

        return redirect('/')


    return render_template('register.html')



@app.route('/login',methods=['POST'])

def login():

    email=request.form['email']
    password=request.form['password']


    cur=mysql.connection.cursor()

    cur.execute(

    "select * from students where email=%s and password=%s",

    (email,password)

    )



    user=cur.fetchone()


    if user:

        session['id']=user[0]

        return redirect('/dashboard')


    return "Invalid Login"



@app.route('/dashboard',methods=['GET','POST'])

def dashboard():


    if request.method=='POST':


        title=request.form['title']

        desc=request.form['description']


        cur=mysql.connection.cursor()

        cur.execute(

        "insert into complaints(student_id,title,description,status) values(%s,%s,%s,%s)",


        (session['id'],title,desc,'Pending')

        )

        mysql.connection.commit()




    cur=mysql.connection.cursor()

    cur.execute(

    "select title,status from complaints where student_id=%s",

    (session['id'],)

    )


    complaints=cur.fetchall()



    return render_template('dashboard.html',
                           complaints=complaints)



if __name__=='__main__':

    app.run(debug=True)
