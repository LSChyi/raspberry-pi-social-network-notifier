from db import db
import requests
import json

class Medium:
	def __init__(self, media_id, comment_num, like_num, link):
		self.media_id, self.comment_num, self.like_num, self.link = media_id, comment_num, like_num, link

	def has_changed(comment_num, like_num):
		return False if ((self.like_num == like_num) and (self.comment_num == comment_num)) else True

	def __str__(self):
		return "id: %s, comments: %i, likes: %i, link: %s" % (self.media_id, self.comment_num, self.like_num, self.link)

user_id, token = db.query_token('instagram')
recent_media_url = "https://api.instagram.com/v1/users/%s/media/recent/?access_token=%s&count=10" % (user_id, token)

def update_id_token(new_id, new_token):
	global user_id, token, recent_media_url
	user_id, token = new_id, new_token
	recent_media_url = "https://api.instagram.com/v1/users/%s/media/recent/?access_token=%s&count=10" % (user_id, token)

def retrieve_recent_media():
	global recent_media_url
	req = requests.get(recent_media_url)
	if req.status_code == 200:
		return req.json()
	else:
		return None

def is_state_different():
	results = retrieve_recent_media()
	different = False
	if results != None:
		media = [ Medium(medium['id'], medium['comments']['count'], medium['likes']['count'], medium['link']) for medium in results['data'] ]
		db_data = db.query("Select media_id, like_num, comment_num from Instagram_media where media_id in ('%s')" % "', '".join([ medium.media_id for medium in media ]))
		db_ids = [ row[0] for row in db_data ]
		for medium in media:
			if medium.media_id not in db_ids:
				db.query("Insert into Instagram_media values ('%s', %i, %i, '%s')" % (medium.media_id, medium.like_num, medium.comment_num, medium.link))
				different = True if (medium.comment_num != 0 or medium.like_num != 0) else different
			else:
				db_record_medium = next((x for x in db_data if x[0] == medium.media_id), None)
				if db_record_medium[1] != medium.like_num or db_record_medium[2] != medium.comment_num:
					different = True
					db.query("Update Instagram_media set comment_num = %i, like_num = %i where media_id = '%s'" % (medium.comment_num, medium.like_num, medium.media_id))
	return different

if __name__ == "__main__":
	print "user_id:", user_id, "token:", token
	print "recent_media_url", recent_media_url
	print is_state_different()
