from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Secreto@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key="-DJ-S0oIfJWqWJ38bHsSzQ"

class Blog(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(120))
    body=db.Column(db.String(1000))
    owner_id=db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, owner):
        self.title=title
        self.body=body
        self.owner=owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes=['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect('/login')



@app.route('/login', methods=["POST", "GET"] )
def login():
    if request.method=="POST":
        username=request.form["username"]
        erruser=""
        password=request.form["pass"]
        errpass=""
        

        existing_user = User.query.filter_by(username=username).first() 
        if not existing_user:
            erruser="Invalid Username"
        elif not existing_user.password==password:
            errpass= "Invalid Password"
        
        if not erruser and not errpass:
            session["username"]=username
            return redirect("/newpost")
        else:
            return render_template('login.html' , title="Login", username=username, erruser=erruser, errpass=errpass)

           
   
    return render_template('login.html' , title="Login")
   
        


@app.route('/signup',  methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']
        verify = request.form['vpass']

        erruser=""
        errpass=""
        errpass2=""


        if username=="":
            erruser="Username is required"
        elif 3>len(username):
            erruser="Username lenght min 3 characteres"
        elif 20<len(username):
            erruser="Username lenght max 20 characteres"
        elif " " in username:
            erruser="User not valid (spaces nor permit)"


        if password=="":
            errpass="Password is required"
        elif 3>len(password):
            errpass="Password lenght min 3 characteres"
        elif 20<len(password):
            errpass="Password lenght max 20 characteres"
        elif " " in password:
            errpass="Password not valid (spaces nor permit)"
    

        if verify=="":
            errpass2="Password Validation is required"
        elif not password==verify:
            errpass2="Password validation need to match"


        existing_user = User.query.filter_by(username=username).first() 
        if existing_user:
            erruser ="A user with that username already exists"

        if not erruser and not errpass and not errpass2:
            new_user = User(username, password)
            session["username"]=username
            db.session.add(new_user)
            db.session.commit()
            session["username"]=username
            return redirect('/newpost')
        else:
            return render_template('signup.html',username=username, erruser=erruser, errpass=errpass, errpass2=errpass2 )
    
    return render_template('signup.html', title="Sign Up")



@app.route('/logout')
def logout():
    del session["username"]
    return redirect('/blog')


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
            owner=User.query.filter_by(username=session['username']).first()
            new_blog=Blog(titl,body,owner)
            db.session.add(new_blog)
            db.session.commit()
            entryBlog = Blog.query.filter_by(id=new_blog.id).first_or_404(description="There is no data with the {} ID".format(new_blog.id))
            return redirect('/blog?id='+str(entryBlog.id))
           

    return render_template('newpost.html',title="Add a Blog Entry")



@app.route('/blog')
def blog():
    id=""
    id=request.args.get("id")
    if id:
        entryBlog = Blog.query.filter_by(id=id).first_or_404(description="There is no data with the {} ID".format(id))
        return render_template("entry.html", title=entryBlog.title, blogItems=entryBlog)
    else:        
        entryBlog=Blog.query.all()
        return render_template('blog.html',title="Build a Blog", blogItems=entryBlog)



if __name__=="__main__":
    app.run()