from flask import Flask
from flask import render_template

app=Flask(__name__)

@app.route('/')
def start():
    return render_template('site/index.html')

@app.route('/books')
def books():
    return render_template('site/books.html')

@app.route('/us')
def us():
    return render_template('site/us.html')

@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

if __name__ =='__main__':
    app.run(debug=True)