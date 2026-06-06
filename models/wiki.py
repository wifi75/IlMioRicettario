from extensions import db


class WikiArticle(db.Model):

    __tablename__ = "wiki_articles"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(255),
        nullable=False
    )

    slug = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    content = db.Column(
        db.Text
    )

    category = db.Column(
        db.String(100),
        nullable=False,
        default="Generale"
    )