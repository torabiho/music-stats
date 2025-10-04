from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime, func, UniqueConstraint


class Base(DeclarativeBase):
    pass


# --- Users & Auth ---
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    # relationships
    tokens: Mapped[list["OAuthToken"]] = relationship(back_populates="user")
    plays: Mapped[list["Play"]] = relationship(back_populates="user")


class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)  # e.g., "spotify"
    auth_url: Mapped[str] = mapped_column(String, nullable=True)


class OAuthToken(Base):
    __tablename__ = "oauth_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"))
    access_token: Mapped[str] = mapped_column(String)
    refresh_token: Mapped[str] = mapped_column(String)
    expires_at: Mapped[DateTime] = mapped_column(DateTime)

    # relationships
    user: Mapped["User"] = relationship(back_populates="tokens")
    provider: Mapped["Provider"] = relationship()


# --- Music Catalog ---
class Artist(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)


class Album(Base):
    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"))


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"))
    album_id: Mapped[int] = mapped_column(ForeignKey("albums.id"))
    provider_id: Mapped[int] = mapped_column(ForeignKey("providers.id"))
    provider_track_id: Mapped[str] = mapped_column(String)  # unique ID from provider

    __table_args__ = (
        UniqueConstraint("provider_id", "provider_track_id", name="uq_provider_track"),
    )


# --- Plays / Listening History ---
class Play(Base):
    __tablename__ = "plays"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"))
    played_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), index=True)

    # relationships
    user: Mapped["User"] = relationship(back_populates="plays")
    track: Mapped["Track"] = relationship()


# --- Aggregated Views (optional materialized table) ---
class TopTrack7d(Base):
    __tablename__ = "top_tracks_7d"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"))
    play_count: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("user_id", "track_id", name="uq_user_track_7d"),
    )
