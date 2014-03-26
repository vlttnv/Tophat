from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
producer_data_set = Table('producer_data_set', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('producer_id', Integer),
    Column('data', LargeBinary),
    Column('time_stamp', DateTime),
)

sets = Table('sets', post_meta,
    Column('producer_id', Integer),
    Column('set_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['producer_data_set'].create()
    post_meta.tables['sets'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['producer_data_set'].drop()
    post_meta.tables['sets'].drop()
