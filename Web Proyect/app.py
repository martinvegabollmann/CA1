from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os


app=Flask(__name__)
mysql=MySQL()
app.secret_key="develoteca"

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='website'
mysql.init_app(app)

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
def admin_index():
    if not 'login' in session:
        return redirect("/admin/login")
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _user=request.form['txtUser']
    _password=request.form['txtPassword']
    print(_user)
    print(_password)

    if _user=="admin" and _password=="1234":
        session["login"]=True
        session["user"]="administrator"
        return redirect("/admin")

    return render_template('admin/login.html',message="Access Denied")


@app.route('/admin/close')
def admin_login_close():
    session.clear()
    return redirect('/admin/login')


@app.route('/admin/books')
def admin_books():

    if not 'login' in session:
        return redirect("/admin/login")
    
    connection=mysql.connect()
    cursor= connection.cursor()
    cursor.execute("SELECT * FROM `books`")
    books=cursor.fetchall()
    connection.commit()
    print(books)

    return render_template('admin/books.html', books=books)

@app.route('/admin/books/save', methods=['POST'])
def admin_books_save():

    if not 'login' in session:
        return redirect("/admin/login")
     
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

    if not 'login' in session:
        return redirect("/admin/login")

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

if __name__ =='__main__':
    app.run(debug=True)