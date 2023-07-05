from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

app=Flask(__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='website'
mysql.init_app(app)

@app.route('/')
def start():
    return render_template('site/index.html')

@app.route('/books')
def books():
    return render_template('site/books.html')

@app.route('/us')
def us():
    return render_template('site/us.html')

@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/books')
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

    sql="INSERT INTO `books` (`id`, `name`, `image`, `url`) VALUES (NULL, %s, %s, %s);"
    date=(_name,_archive.filename,_url)

    connection= mysql.connect()
    cursor=connection.cursor()
    cursor.execute(sql,date)
    connection.commit()


    print(_name)
    print(_url)
    print(_archive)

    return redirect('/admin/books')


if __name__ =='__main__':
    app.run(debug=True)