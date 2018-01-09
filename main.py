from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:pass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return redirect('/blog')

       
@app.route('/newpost', methods=['POST','GET'])
def new_blog():

    if request.method == 'POST':
        error_found = False
        blog_title = request.form['title']
        blog_body = request.form['body']
        if not blog_title:
            error_found = True
            flash('You must enter a blog title', 'error1')
            # return render_template('newpost.html',title="New Blog")
        if not blog_body:
            error_found = True
            flash('You must enter a blog body', 'error2')
            # return render_template('newpost.html',title="New Blog")
        if error_found:
            return render_template('newpost.html',title="New Blog")
        else:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()

            blog2 = Blog.query.filter_by(title = blog_title).first()
            print("literal", blog2.title)
            print("bog2", blog2.id)
            bid = str(blog2.id)
            return redirect('/blogdetail?id='+ bid)

    return render_template('newpost.html',title="New Blog")
    

@app.route('/blog', methods=['GET'])
def old_blogs():

    blogs = Blog.query.all()
    return render_template('blog.html',title="Past Blogs",
    blogs=blogs)
             
@app.route('/blogdetail', methods=['GET'])
def blog_detail():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id = id).first()
    return render_template('blogdetail.html',
    blog=blog)
             
# @app.route('/delete-task', methods=['POST'])
# def delete_task():

#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     task.completed = True
#     db.session.add(task)
#     db.session.commit()




if __name__ == '__main__':
    app.run()