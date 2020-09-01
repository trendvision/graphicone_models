from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, String, JSON, DateTime, Integer, ForeignKey, func, schema, text
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION


Base = declarative_base()
BOARD_ID = schema.Sequence('board_id', start=1000000000000, increment=1)
GRAPH_ID = schema.Sequence('graph_id', start=1000000000000, increment=1)


class Account(Base):
    __tablename__ = 'account'

    username = Column(String, primary_key=True, index=True)
    password_hash = Column(String)
    email = Column(String, unique=True)
    interests = Column(JSON)
    favorite = Column(JSON)
    name = Column(String)
    image_url = Column(JSON)
    occupation = Column(String)
    join_date = Column(DateTime(timezone=True))
    following_allow = Column(Boolean)
    subscriptions = Column(JSON)
    is_social_notification = Column(Boolean)


class Device(Base):
    __tablename__ = 'device_info'

    device_id = Column(String)
    username = Column(String)
    locale_timestamp = Column(DateTime(timezone=True))
    device_token = Column(String, primary_key=True) # https://stackoverflow.com/questions/34283259/how-to-define-a-table-without-primary-key-with-sqlalchemy


class Follower(Base):
    __tablename__ = 'follower'

    id = Column(Integer, primary_key=True)
    follower = Column(String, nullable=False)
    following = Column(String, nullable=False)
    fellow = Column(Boolean, nullable=False, default=False)
    accept_status = Column(Boolean, nullable=False, default=False)
    timestamp = Column(DateTime(timezone=True))
    declined = Column(Boolean, nullable=False, default=False)


class EmailNotification(Base):
    __tablename__ = 'email_notification'

    username = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='NO ACTION'),
                      primary_key=True, nullable=False)
    push_notification_day = Column(String, nullable=False)
    enable = Column(Boolean, nullable=False)


class PushNotificationTypes(Base):
    __tablename__ = 'push_notification_types'

    type = Column(String, primary_key=True, nullable=False)
    general_type = Column(String, nullable=False)
    allowed_days = Column(JSON, nullable=False, default=[])
    allowed_frequency = Column(JSON, nullable=False, default=[])
    allowed_graph_count = Column(JSON, nullable=False, default=[])


class PushNotificationSettings(Base):
    __tablename__ = 'push_notification_settings'

    username = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='NO ACTION'),
                      primary_key=True, nullable=False)
    type = Column(String, ForeignKey('push_notification_types.type', ondelete='CASCADE', onupdate='NO ACTION'),
                  nullable=False)
    frequency = Column(String, nullable=False)
    notification_days = Column(JSON, nullable=False)
    notification_graph_count = Column(Integer)
    notification_time = Column(String, nullable=False, default='14:00')
    enable = Column(Boolean, nullable=False)


class Spaces(Base):
    __tablename__ = 'spaces'

    id = Column(String, primary_key=True, nullable=False)
    subscription = Column(String)
    name = Column(String, nullable=False, default='')
    link_disable = Column(String, nullable=False, default='')
    link_active = Column(String, nullable=False, default='')


class TrialPeriod(Base):
    __tablename__ = 'trial_periods'

    username = Column(String, primary_key=True, nullable=False)
    subscription = Column(String, nullable=False)
    until_timestamp = Column(DateTime(timezone=True), nullable=False)


class Payment(Base):
    __tablename__ = 'payment'

    user_id = Column(String, primary_key=True)
    environment = Column(String)
    notification_type = Column(String)
    original_transaction_id = Column(String)
    latest_expires_date = Column(DateTime(timezone=True))
    is_subscribed = Column(Boolean, nullable=False, default=True)
    will_auto_renew = Column(Boolean)
    cancellation_date = Column(DateTime(timezone=True))
    latest_receipt = Column(String)
    latest_expired_receipt = Column(String)
    transaction_id = Column(String)
    auto_renew_product_id = Column(String)
    promotional_offer_id = Column(String)
    product_id = Column(String)
    web_order_line_item_id = Column(String)
    is_intro_period = Column(Boolean)
    is_trial_period = Column(Boolean)
    insert_timestamp = Column(DateTime(timezone=True), nullable=False, default=func.cuurrent_timestamp())


class Subscription(Base):
    __tablename__ = 'subscription'

    username = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='NO ACTION'),
                      primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False, default='')
    description = Column(String, nullable=False, default='')
    demo_board_id = Column(String)
    purchase_id = Column(String)
    subscription_folder_id = Column(String)
    price = Column(DOUBLE_PRECISION)


class Board(Base):
    __tablename__ = 'board'

    id = Column(String, BOARD_ID, primary_key=True, default=text("'B' || nextval('board_id')"))
    name = Column(String, nullable=False)
    owner = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='NO ACTION'))
    members = Column(JSON, nullable=False, default=[])
    preview_img_url = Column(String, nullable=False, default='')
    graphs_count = Column(Integer, default=0, autoincrement=False)
    privacy = Column(String)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.current_timestamp())


class Graph(Base):
    __tablename__ = 'graph'

    id = Column(String, GRAPH_ID, primary_key=True, default=text("'G' || nextval('board_id')"))
    name = Column(String, nullable=False, default='')
    location = Column(String, nullable=False)
    location_id = Column(String)
    link_small = Column(JSON, nullable=False)
    link_medium = Column(JSON, nullable=False)
    link_large = Column(JSON, nullable=False)
    owner = Column(JSON, nullable=False)
    source = Column(String, nullable=False, default='')
    description = Column(String, nullable=False, default='')
    parent = Column(String, default=None)
    publish_date = Column(DateTime(timezone=True), nullable=False, default=func.current_timestamp())
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.current_timestamp())
    article_link = Column(String, nullable=False, default='')
    publisher = Column(String, ForeignKey('account.username', ondelete='NO ACTION', onupdate='NO ACTION'))
    mongo_id = Column(String)
    graph_type = Column(String)
    shifts = Column(JSON, nullable=False, default=[])
    industries = Column(JSON, nullable=False, default=[])
    upvote = Column(Integer, nullable=False, default=0)
