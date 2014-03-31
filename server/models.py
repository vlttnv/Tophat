from server import db

class Producer(db.Model):
	id		= db.Column(db.Integer, primary_key = True)
	location	= db.Column(db.String(120))
	ip_address	= db.Column(db.String(120))
	timestamp	= db.Column(db.String(120))
	data		= db.Column(db.LargeBinary)

	def __repr__(self):
		return '<Producer %r>' % (self.id)
