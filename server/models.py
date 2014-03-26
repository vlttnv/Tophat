from server import db

sets = db.Table('sets',
		db.Column('producer_id', db.Integer, db.ForeignKey('producer.id')),
		db.Column('set_id', db.Integer, db.ForeignKey('producerdataset.id'))
		)


class Producer(db.Model):
	id		= db.Column(db.Integer, primary_key = True)
	location	= db.Column(db.String(120))
	ip_adress	= db.Column(db.String(120))
	timestamp	= db.Column(db.DateTime)


	def __repr__(self):
		return '<Producer %r>' % (self.id)

class ProducerDataSet(db.Model):
	id		= db.Column(db.Integer, primary_key = True)
	producer_id	= db.Column(db.Integer, db.ForeignKey('producer.id'))
	data		= db.Column(db.LargeBinary)
	time_stamp	= db.Column(db.DateTime)
