from flask import Flask,render_template
app=Flask(__name__,template_folder='view/templates',static_folder='view/static')

@app.route("/")
def welcome():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/applicant')
def applicant_home():
    return render_template('applicant.html')  


@app.route('/recruiter')
def recruiter_home():
    return render_template('recruiter.html')  

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

if __name__ == '_main_':
    app.run(debug=True)

from controller import* 