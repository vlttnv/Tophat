from server import db

class Producer(db.Model):
	id		= db.Column(db.Integer, primary_key = True)
	location	= db.Column(db.String(120))
	ip_address	= db.Column(db.String(120))
	timestamp	= db.Column(db.String(120))


	def __repr__(self):
		return '<Producer %r>' % (self.id)

class ProducerDataSet(db.Model):
	id		= db.Column(db.Integer, primary_key = True)
	producer_id	= db.Column(db.Integer, db.ForeignKey('producer.id'))
	data		= db.Column(db.LargeBinary)
	timestamp	= db.Column(db.String(120))
