from datetime import datetime
from sqlalchemy.orm import Session
from models.models import PostStatsRecord

def insert_post_stats_record(db: Session, data: dict):
    post_stats_record = PostStatsRecord(
        post_tiktok_id=data['post_tiktok_id'],
        content=data['content'],
        collect_count=data['collect_count'],
        digg_count=data['digg_count'],
        share_count=data['share_count'],
        comment_count=data['comment_count'],
        play_count=data['play_count'],
        post_created_time=data['post_created_time'],
        scraped_time=datetime.now()
        )
    db.add(post_stats_record)
    db.commit()
    db.refresh(post_stats_record)
    return post_stats_record

# def insert_channel(db: Session, channel_id: str, channel_name: str):
#     channel = Channel(id=channel_id, name=channel_name)
#     db.add(channel)
#     db.commit()
#     db.refresh(channel)
#     return channel

# def insert_video_post(db: Session, data: dict):
#     video_post = VideoPost(
#         tiktok_id=data['tiktok_id'], 
#         channel_name=data['channel_name'],
#         content=data['content'],
#         scraped_time=data['scraped_time'], 
#         post_created_time=data['post_created_time']
#         )
#     db.add(video_post)
#     db.commit()
#     db.refresh(video_post)
#     return video_post
    