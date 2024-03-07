from datetime import datetime
from sqlalchemy.orm import Session
from models.models import PostStatsRecord

def insert_post_stats_record(db: Session, data: dict):
    post_stats_record = PostStatsRecord(
        post_tiktok_id=str(data['post_tiktok_id']),
        content=str(data['content']),
        collect_count=int(data['collect_count']),
        digg_count=int(data['digg_count']),
        share_count=int(data['share_count']),
        comment_count=int(data['comment_count']),
        play_count=int(data['play_count']),
        post_created_time=data['post_created_time'],
        scraped_time=datetime.now()
        )
    db.add(post_stats_record)
    db.commit()
    db.refresh(post_stats_record)
    return post_stats_record

def create_bulk_posts(db: Session, bulk: list[dict]):
    db.bulk_insert_mappings(PostStatsRecord, bulk)
    db.commit()
    return bulk

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
    