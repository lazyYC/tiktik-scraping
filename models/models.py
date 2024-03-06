from sqlalchemy import Column, Integer, String, DateTime, ForeignKey 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 我認為較完整的 schemas，為求 demo 方便在此先省略
# class Channel(Base):
#     __tablename__ = 'channel'
#     id = Column(String, primary_key=True, index=True, autoincrement=True)
#     name = Column(String, nullable=False, unique=True)
#     posts = relationship('Post', back_populates='channel')


# class VideoPost(Base):
#     __tablename__ = 'video_posts'
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     tiktok_id = Column(String, unique=True)
#     channel_name = Column(String, ForeignKey('channel.name'))
#     content = Column(String)
#     scraped_time = Column(DateTime)
#     post_created_time = Column(DateTime)
#     stats_record = relationship('PostStatsRecord', back_populates='video_posts')


class PostStatsRecord(Base):
    __tablename__ = 'post_stats_records'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_tiktok_id = Column(Integer)
    content = Column(String(1000))
    collect_count = Column(Integer)
    digg_count = Column(Integer)
    share_count = Column(Integer)
    comment_count = Column(Integer)
    play_count = Column(Integer)
    post_created_time = Column(DateTime)
    scraped_time = Column(DateTime)
