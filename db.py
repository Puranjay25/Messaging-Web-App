import MySQLdb

def connect():
	a=MySQLdb.connect(host="localhost",user="root",passwd="#your_own_password",db="#your_own_database_name")
	b=a.cursor()
	return a,b
