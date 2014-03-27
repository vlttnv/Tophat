from server import models, db
from sqlalchemy.exc import IntegrityError

def updateHeartBeat(producer):
    """
    Update producer's information. If the producer does not exist,
    add a new record to the database

    Producer data format:
    {
        'ip': ID address,
        'id': producer ID (mobile phone unique ID),
        'location': location,
        'timestamp': timestamp
    }
    """

    producers = models.Producer.query.filter_by(id=producer['id'])
    producers_count = producers.count()

    if producers_count == 0:
        # add a new producer
        producer_new = models.Producer(
            id = producer['id'],
            location = producer['location'],
            ip_address = producer['ip'],
            timestamp = producer['timestamp']
        )

        try:
            db.session.add(producer_new)
            db.session.commit()
            print 'Added new producer:', producer['id']
            return True

        except IntegrityError as err:
            print 'Failed to add a new producer:', producer['id']
            return False

    elif producers_count == 1:
        # update producer info
        producer_old = producers.first()

        try:
            # update ip & timestamp
            producer_old.ip_address = producer['ip']
            producer_old.timestamp = producer['timestamp']
            db.session.commit()
            print 'Updated heartbeat for producer:', producer['id']
            return True

        except IntegrityError as err:
            print 'Failed to update heartbeat for producer:', producer['id']
            return False

    else:
        print 'Found more than one producer with the same id:', producer['id']
        return False


def addProducerData(dataset):
    """
    Add producer data to the database

    Dataset format:
    {
        'id': dataset ID
        'producer_id': producer ID (mobile phone unique ID),
        'data': data,
        'timestamp': timestamp
    }
    """

    dataset_new = models.ProducerDataSet(
        id = dataset['id'],
        producer_id = dataset['producer_id'],
        data = dataset['data'],
        timestamp = dataset['timestamp']
    )

    try:
        db.session.add(dataset_new)
        db.session.commit()
        print 'Added new dataset:', dataset['id']
        return True

    except IntegrityError as err:
        print 'Failed to add a new dataset:', dataset['id']
        return False

def getProducerData(producer_id):
    """
    Retrieve latest producer data
    """

    datasets = models.ProducerDataSet.filter_by(producer_id=producer_id)
    datasets_count = datasets.count()

    if datasets_count == 0:
        print 'Dataset not found'
        return None

    elif datasets_count == 1:
        print 'Found dataset:', datasets.first().id

    else:
        print 'Found more than one producer'

    # use first result for now
    data = datasets.first().data

    return data

def doesProducerExist(producer_id):
    """
    Return true if a record of the producer exists in the database
    """

    if models.Producer.query.filter_by(id=producer_id).count() > 0:
        return True
    else:
        return False

def getProducerIP(producer_id):
    """
    Retrieve the producer IP address from the ID
    """

    producers = models.Producer.query.filter_by(id=producer_id)

    if producers.count() == 0:
        print 'Producer not found'
        return None

    elif producers.count() == 1:
        print 'Found producer:', producer_id

    else:
        print 'Found more than one producer'

    # use first result for now
    ip_address = producers.first().ip_address

    return ip_address