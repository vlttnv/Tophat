from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
producer = Table('producer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('location', String(length=120)),
    Column('ip_adress', String(length=120)),
    Column('timestamp', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['producer'].columns['ip_adress'].create()
    post_meta.tables['producer'].columns['timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['producer'].columns['ip_adress'].drop()
    post_meta.tables['producer'].columns['timestamp'].drop()
