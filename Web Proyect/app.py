from flask import Flask
from flask import render_template, request, redirect, session
from flask_login import LoginManager,login_user,logout_user,login_required
from flask_wtf.csrf import CSRFProtect
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os
from templates.entities.User import User
from templates.entities.ModelUser import ModelUser

csrf=CSRFProtect()
app=Flask(__name__)
mysql=MySQL()
app.secret_key="develoteca"
login_manager_app=LoginManager(app)

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='website'
mysql.init_app(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql,id)


@app.route('/')
def start():
    return render_template('site/index.html')

@app.route('/img/<image>')
def images(image):
    print(image)
    return send_from_directory(os.path.join('templates/site/img'),image)

@app.route('/css/<archivecss>')
def css_link(archivecss):
    return send_from_directory(os.path.join('templates/site/css'),archivecss)


@app.route('/books')
def books():

    connection=mysql.connect()
    cursor= connection.cursor()
    cursor.execute("SELECT * FROM `books`")
    books=cursor.fetchall()
    connection.commit()

    return render_template('site/books.html', books=books)

@app.route('/us')
def us():
    return render_template('site/us.html')

@app.route('/admin/')
@login_required
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    if request.method == 'POST':
        user = User(0,request.form['username'], request.form['password'])
        logged_user=ModelUser.login(mysql,user)
        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                return render_template('/admin/index.html')
            else:
                return render_template('/admin/login.html', message="ACCESS DENIED")
        else:
            return render_template('/admin/login.html', message="ACCESS DENIED")
    else:
        return render_template('/admin/login.html', message="ACCESS DENIED")
        

    

@app.route('/admin/close')
def admin_login_close():
    logout_user()
    return render_template('/admin/login.html')


@app.route('/admin/books')
@login_required
def admin_books():

    connection=mysql.connect()
    cursor= connection.cursor()
    cursor.execute("SELECT * FROM `books`")
    books=cursor.fetchall()
    connection.commit()
    print(books)

    return render_template('admin/books.html', books=books)

@app.route('/admin/books/save', methods=['POST'])
def admin_books_save():
     
    _name=request.form['txtName']
    _url=request.form['txtURL']
    _archive=request.files['txtImage']

    time=datetime.now()
    currentTime=time.strftime('%Y%H%M%S')

    if _archive.filename!="":
        newName=currentTime+"_"+_archive.filename
        _archive.save("templates/site/img/"+newName)

    sql="INSERT INTO `books` (`id`, `name`, `image`, `url`) VALUES (NULL, %s, %s, %s);"
    date=(_name,newName,_url)

    connection= mysql.connect()
    cursor=connection.cursor()
    cursor.execute(sql,date)
    connection.commit()


    print(_name)
    print(_url)
    print(_archive)

    return redirect('/admin/books')

@app.route('/admin/books/delete', methods=['POST'])
def admin_books_delete():

    _id=request.form['txtID']
    print(_id)

    connection=mysql.connect()
    cursor= connection.cursor()
    cursor.execute("SELECT image FROM `books` WHERE id=%s", (_id))
    book=cursor.fetchall()
    connection.commit()
    print(book)

    if os.path.exists("templates/site/img/"+str(book[0][0])):
        os.unlink("templates/site/img/"+str(book[0][0]))

    connection=mysql.connect()
    cursor= connection.cursor()
    cursor.execute("DELETE FROM `books` WHERE id=%s", (_id))
    connection.commit()

    return redirect('/admin/books')

def status_401(error):
    return redirect("/admin/login")

def status_404(error):
    return "<h1> Page Not Found <h1>", 404

if __name__ =='__main__':
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(debug=True)