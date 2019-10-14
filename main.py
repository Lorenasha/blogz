from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Secreto@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120))
    body=db.Column(db.String(1000))

    def __init__(self, title, body):
        self.title=title
        self.body=body



@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        titl = request.form['title']
        body = request.form['body']
        errtitl=""
        errbody=""
        
        if titl=="":
            errtitl="Please fill in the title"
        if body=="":
            errbody="Please fill in the body"
        
        if errtitl or errbody:
            return render_template('newpost.html',title="Add a Blog Entry", errtitl=errtitl, errbody=errbody)
        else:
            new_blog=Blog(titl,body)
            db.session.add(new_blog)
            db.session.commit()
            entryBlog = Blog.query.filter_by(id=new_blog.id).first_or_404(description="There is no data with the {} ID".format(new_blog.id))
            #return render_template('entry.html',  title=entryBlog.title, blogItems=entryBlog)
            return redirect(url_for('entry', numid=entryBlog.id))
            


    return render_template('newpost.html',title="Add a Blog Entry")


    

@app.route('/blog')
def blog():
    
    entryBlog=Blog.query.all()
    return render_template('blog.html',title="Build a Blog", blogItems=entryBlog)



@app.route('/blog?id=<numid>')
def entry(numid):
    idnum=numid
    entryBlog = Blog.query.filter_by(id=idnum).first_or_404(description="There is no data with the {} ID".format(idnum))
    return render_template('entry.html', title=entryBlog.title, blogItems=entryBlog)




if __name__=="__main__":
    app.run()