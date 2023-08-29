# services.py

from sqlalchemy.orm import Session
from app.models import song

# TODO: Create, Update, Delete


# Retrieve
def retrieve_all_songs(db: Session):
    return db.query(song.Song).all()


def retrieve_songs_by_year(db: Session, year: int):
    return db.query(song.Song).filter(song.Song.year == year).all()


def retrieve_song_by_rank(db: Session, rank: int):
    return db.query(song.Song).filter(song.Song.rank == rank).first()
