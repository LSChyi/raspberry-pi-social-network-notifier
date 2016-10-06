import sqlite3

def connect_db():
	conn = sqlite3.connect("social_notifier.db")
	curs = conn.cursor()
	return (conn, curs)

def query(query_str):
	conn, curs = connect_db()
	result = curs.execute(query_str).fetchall()
	conn.close()
	return result

def query_token(service):
	conn, curs = connect_db()
	result = curs.execute("Select user_id, token from Access_token where service = '%s';" % service).fetchone()
	conn.close()
	return result

def save_token(service, user_id, token):
	conn, curs = connect_db()
	result = curs.execute("Insert into Access_token values ('%s', '%s', '%s');" % (service, user_id, token))
	conn.commit()
	conn.close()

def update_token(service, token):
	conn, curs = connect_db()
	curs.execute("Update Access_token set token = '%s' where service = '%s';" % (token, service))
	conn.commit()
	conn.close()

def delete_token(service):
	conn, curs = connect_db()
	curs.execute("Delete from Access_token where service = '%s'" % service)
	conn.commit()
	conn.close()

if __name__ == "__main__":
	print "save a fake facebook token"
	save_token('facebook', 'lschyi', 'test_token')

	print "query all token"
	print query("Select * from Access_token;")
	
	print "delete fake facebook token"
	delete_token('facebook')

	print "query all token"
	print query("Select * from Access_token;")
