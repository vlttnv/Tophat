from server import models, db

def updateHeartBeat(producer):
    """
    producer = {
        'ip': ID address,
        'id': producer ID (mobile phone unique ID),
        'location': location,
        'timestamp': timestamp
    }
    """

    if models.Producer.query.filter_by(id=producer['id']).count() == 0:
        producer_model = models.Producer(
            id = producer['id'],
            location = producer['location'],
            ip_address = producer['ip'],
            timestamp = producer['timestamp']
        )
        db.session.add(producer_model)
        db.session.commit()

        print 'Added new producer:', producer['id']

    else:
        producer_model = models.Producer.query.filter_by(id=producer['id']).first()
        producer_model.timestamp = producer['timestamp']
        db.session.commit()

        print 'Updated heartbeat for producer:', producer['id']

    return True

def addProducerData(package):
    """
     package = {
        'id': data package ID
        'producer_id': producer ID (mobile phone unique ID),
        'data': data,
        'timestamp': timestamp
    }
    """

    data_set = models.ProducerDataSet(
        id = package['id'],
        producer_id = package['producer_id'],
        data = package['data'],
        timestamp = package['timestamp']
    )

    db.session.add(data_set)
    db.session.commit()

    return true

def getProducerData(producer_id):
    # get latest producer data
    return 'Location: St Andrews'

def doesProducerExist(producer_id):
    if models.Producer.query.filter_by(id=producer_id).count() > 0:
        return True
    else:
        return False

def getProducerIP(producer_id):
    results = models.Producer.query.filter_by(id=producer_id)

    if results.count() == 0:
        return None

    else if results.count() == 1:
        print 'Found producer'

    else
        print 'Found more than one producer'

    # use first result for now
    ip_address = results.first().ip_address

    return ip_address