from flask import Flask,render_template,url_for,redirect,request,session
from db import connect

app=Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/contact',methods=['POST','GET'])
def contact():
	if request.method=='POST':
		e,f=connect()
		firstname=request.form.get("firstname",False)
		lastname=request.form.get("lastname",False)
		username=request.form.get("yourusername",False)
		querysubject=request.form.get("querysubject",False)
		query=request.form.get("query",False)
		#instead of 'queries' you can give your own table name
		f.execute("insert into queries(Firstname, Lastname, Username, Subject, Query) values(%s,%s, %s, %s, %s)",(firstname,lastname,username,querysubject,query))
		e.commit()
		e.close()
		f.close()
		return redirect(url_for('index'))  
	return render_template('contact.html')

@app.route('/logout')
def logout():
	session['logged_in']=False
	session.pop('username',None)
	session.clear()
	return redirect(url_for('index'))

@app.route('/contactlist',methods=['POST','GET'])
def contactlist():
		e,f=connect()
		user_list=f.execute("select FirstName,LastName,Username from users")
		names=f.fetchall()
		e.commit()
		e.close()
		f.close()
		return render_template('contactlist.html',names=names)

@app.route('/view',methods=['POST','GET'])
def view():
	if request.method=='GET':
		e,f=connect()
		if session['logged_in']==True:
			loggedin_username=session['username']
		#instead of 'messages' you can give your own table name
		get_reciever_username=f.execute("select Username,Message from messages where Reciever_Username='%s'"%(loggedin_username))
		#get_sender_username=f.execute("select Username from messages where Reciever_Username='%s'"%(loggedin_username))
		if get_reciever_username!=0:
			get_reciever_username_messages=f.fetchall()
		elif get_reciever_username==0:
			get_reciever_username_messages=" "
		e.commit()
		e.close()
		f.close()
		#return redirect(url_for('view1',get_reciever_username_messages=get_reciever_username_messages))
		return render_template('viewmessage1.html',get_reciever_username_messages=get_reciever_username_messages)
	return render_template('viewmessage.html')

@app.route('/send',methods=['POST','GET'])
def send():
	if request.method=='POST':
		e,f=connect()
		entered_rusername=request.form.get("rusername",False)
		entered_subject=request.form.get("subject",False)
		entered_message=request.form.get("message",False)
		if session['logged_in']==True:
			login_username=session['username']
		#instead of 'messages' you can give your own table name
		f.execute("insert into messages(Username, Reciever_Username, Subject, Message) values(%s, %s, %s, %s)",(login_username,entered_rusername,entered_subject,entered_message))
		e.commit()
		e.close()
		f.close()
		return redirect(url_for('userhomepage'))
	return render_template('sendmessage.html')

@app.route('/dashboard')
def dashboard():
	return render_template('userhomepage.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/userhomepage')
def userhomepage():
	return render_template('userhomepage.html')

@app.route('/login',methods=['POST','GET'])
def login():
	if request.method=="POST":
		e,f=connect()
		usname=request.form.get("uname",False)
		paswd=request.form.get("pass",False)
		get_username=f.execute("select * from users where Username='%s'"%(usname))
		if get_username==0:
			return redirect(url_for('login'))
		get_password=f.fetchone()[5]
		#instead of 'messages' you can give your own table name
		#get_reciever_username=f.execute("select * from messages where Reciever_Username='%s'"%(get_username))
		#get_messages=f.fetchone()[3]
		if get_password!=paswd or get_username==0:
			return redirect(url_for('login'))
		else:
			session['logged_in']=True
			session['username']=usname
			return redirect(url_for('userhomepage'))
		e.commit()
		e.close()
		f.close()
	return render_template('login.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
	if request.method=="POST":	
		e,f=connect()
		firstname=request.form.get("fname",False)
		lastname=request.form.get("lname",False)
		usernames=request.form.get("username",False)
		contacts=request.form.get("contact",False)
		password=request.form.get("pswd",False)
		check_username=f.execute("select Username from users where Username='%s'"%(usernames))
		if usernames=='admin' or check_username!=0:
			return redirect(url_for('signup'))
		#instead of 'users' you can give your own table name
		f.execute("insert into users(FirstName, LastName, Username, Contact, Password) values(%s, %s, %s, %s, %s)",(firstname, lastname, usernames, contacts, password))
		e.commit()
		e.close()
		f.close()
		return redirect(url_for('login'))
	return render_template('signup.html')

if __name__=='__main__':
	app.secret_key = 'super secret key '
	app.run(debug=True)
