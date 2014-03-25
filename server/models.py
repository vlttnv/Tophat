from server import db


class Producer(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	location = db.Column(db.String(120), index = True)

	def __repr__(self):
		return '<Producer %r>' % (self.id)
