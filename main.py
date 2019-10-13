from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Secreto@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)



entryBlog = []

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        titl = request.form['title']
        body = request.form['body']
        entryBlog.append([titl,body])
        return render_template('base.html',title=titl, bodyBlog=body )


    return render_template('newpost.html',title="Add a Blog Entry")


@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
       return render_template('base.html',title="New Blog") 
    return render_template('blog.html',title="Build a Blog", blogItems=entryBlog)

app.run()