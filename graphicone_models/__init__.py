from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Boolean, String, JSON, DateTime, Integer, ForeignKey, func, schema, text,\
    PrimaryKeyConstraint, BigInteger, Float
from sqlalchemy.orm import relationship
import datetime


Base = declarative_base()
BOARD_ID = schema.Sequence('board_id', start=1000000000000, increment=1)
GRAPH_ID = schema.Sequence('graph_id', start=1000000000000, increment=1)


class Account(Base):
    __tablename__ = 'account'

    username = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    interests = Column(JSON, nullable=False, default={})
    favorite = Column(JSON, nullable=False, default=[])
    name = Column(String, nullable=False)
    image_url = Column(JSON, nullable=False, default=[])
    occupation = Column(String, nullable=False, default='')
    join_date = Column(DateTime(timezone=True), nullable=False, default=func.current_timestamp())
    following_allow = Column(Boolean, nullable=False, default=False)
    subscriptions = Column(JSON, nullable=False, default=[])
    is_social_notification = Column(Boolean, nullable=False, default=True)


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
    push_notification_day = Column(String, nullable=False, default='THU')
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
    subscription = Column(String, ForeignKey('subscription.name', ondelete='CASCADE', onupdate='CASCADE'))
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
    insert_timestamp = Column(DateTime(timezone=True), nullable=False, default=func.current_timestamp())


class Subscription(Base):
    __tablename__ = 'subscription'

    username = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='NO ACTION'),
                      primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False, default='')
    description = Column(String, nullable=False, default='')
    demo_board_id = Column(String, ForeignKey('board.id', ondelete='CASCADE', onupdate='NO ACTION'))
    purchase_id = Column(String, nullable=False)
    subscription_folder_id = Column(String)
    price = Column(Float)


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


class IntrinioDump(Base):
    __tablename__ = 'intrinio_dump'

    ticker = Column(String, primary_key=True)
    id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    lei = Column(String)
    cik = Column(String)
    marketcap = Column(BigInteger)
    pricetoearnings = Column(Float)
    evtoebitda = Column(Float)
    short_interest = Column(Float)
    roe = Column(Float)
    hundred_days_trading_range = Column(Float, default=0)
    trading_range_low = Column(Float)
    trading_range_high = Column(Float)
    change = Column(Float, default=0)
    industry = Column(String, nullable=False, default='')


class Equity(Base):
    __tablename__ = 'equity'

    ticker = Column(String, ForeignKey('intrinio_dump.ticker', onupdate='CASCADE', ondelete='CASCADE'),
                    primary_key=True)
    name = Column(String)
    trend_1_name = Column(String, nullable=False, default='')
    trend_1_value = Column(Integer)
    trend_2_name = Column(String, nullable=False, default='')
    trend_2_value = Column(Integer)
    trend_3_name = Column(String, nullable=False, default='')
    trend_3_value = Column(Integer)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.current_timestamp())
    tags = Column(JSON, nullable=False, default=[])


class Tag(Base):

    __tablename__ = 'tag'
    __table_args__ = (
        PrimaryKeyConstraint('value', 'graph_id', 'author'),
    )

    value = Column(String, nullable=False)
    graph_id = Column(String, ForeignKey('graph.id', ondelete='NO ACTION', onupdate='NO ACTION'))
    author = Column(String, ForeignKey('account.username', ondelete='NO ACTION', onupdate='NO ACTION'))


class ExposedEquity(Base):

    __tablename__ = 'exposed_equity'
    __table_args__ = (
        PrimaryKeyConstraint('equity_id', 'graph_id', 'author'),
    )

    equity_id = Column(String, ForeignKey('equity.ticker', ondelete='CASCADE', onupdate='CASCADE'))
    graph_id = Column(String, ForeignKey('graph.id', ondelete='CASCADE', onupdate='NO ACTION'))
    author = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='NO ACTION'))
    equity_data = relationship('Equity',
                               primaryjoin='foreign(ExposedEquity.equity_id) == Equity.ticker')


class PCArguments(Base):
    __tablename__ = 'p_c_arguments'

    argument = Column(String, ForeignKey('pros_and_cons.name', ondelete='NO ACTION', onupdate='NO ACTION'),
                      primary_key=True)
    category = Column(String, nullable=False)


class ProsAndConsSelect(Base):
    __tablename__ = 'pros_and_cons_select'

    id = Column(Integer, primary_key=True)
    pros_and_cons_id = Column(Integer, ForeignKey('pros_and_cons.id', ondelete='CASCADE', onupdate='CASCADE'))
    vote_author = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='CASCADE'))
    value = Column(Boolean, nullable=False)


class ProsAndCons(Base):
    __tablename__ = 'pros_and_cons'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    theme = Column(String, nullable=False)
    ticker = Column(String, nullable=False)
    graph_id = Column(String, ForeignKey('graph.id', ondelete='CASCADE', onupdate='NO ACTION'))
    author = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='CASCADE'))
    # count_pros = Column(Integer, nullable=False, default=0)
    # count_cons = Column(Integer, nullable=False, default=0)
    cv = Column(Boolean, nullable=False, default=False)
    graphs = Column(JSON, nullable=False, default={})
    count_pros = Column(Integer)
    count_cons = Column(Integer)
    pros_and_cons_votes = relationship(ProsAndConsSelect)
    category = relationship(PCArguments)


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
    tags = relationship(Tag)
    equities = relationship(ExposedEquity)
    pros_and_cons = relationship(ProsAndCons)


class Interests(Base):
    __tablename__ = 'interests'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    link_active_small = Column(String, nullable=False)
    link_active_medium = Column(String, nullable=False)
    link_active_large = Column(String, nullable=False)
    link_disable_small = Column(String, nullable=False)
    link_disable_medium = Column(String, nullable=False)
    link_disable_large = Column(String, nullable=False)


class BlockedUser(Base):
    __tablename__ = 'blockeduser'

    id = Column(Integer, primary_key=True)
    id_blocking_user = Column(String, nullable=False)
    id_blocked_user = Column(String, nullable=False)


class TemporaryPass(Base):
    __tablename__ = 'temporary_pass'

    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='CASCADE'))
    email = Column(String, nullable=False)
    temp_pass = Column(String, nullable=False)
    valid_until = Column(DateTime(timezone=True), nullable=False,
                         default=func.current_timestamp() + datetime.timedelta(days=1))


class AccessData(Base):
    __tablename__ = 'access_data'

    id = Column(Integer, primary_key=True)
    username = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='CASCADE'))
    login = Column(DateTime(timezone=True), nullable=True)
    logout = Column(DateTime(timezone=True), nullable=True)
    password = Column(DateTime(timezone=True), nullable=True)


class ExposedEquityFields(Base):
    __tablename__ = 'ee_fields'
    __table_args__ = (
        PrimaryKeyConstraint('equity_ticker', 'username'),
    )

    username = Column(String, ForeignKey('account.username', ondelete='CASCADE', onupdate='CASCADE'))
    equity_ticker = Column(String, nullable=False)
    fields = Column(JSON, nullable=False)


def to_dict(record: Base):
    dict_ = {}
    for key in record.__mapper__.c.keys():
        dict_[key] = getattr(record, key)
    return dict_
