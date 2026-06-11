from extensions import db
from datetime import datetime


class MasterImage(db.Model):
    """
    Anagrafica centralizzata delle immagini ricette.
    Ogni immagine catalogata può essere assegnata dinamicamente a più ricette.
    """

    __tablename__ = "master_images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    caption = db.Column(
        db.String(255),
        nullable=True
    )

    alt_text = db.Column(
        db.String(255),
        nullable=True
    )

    upload_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # Relazione con Recipe (One-to-Many)
    recipes = db.relationship(
        "Recipe",
        back_populates="featured_image",
        lazy=True,
        foreign_keys="Recipe.image_id"
    )

    def __repr__(self):
        return f"<MasterImage {self.id}: {self.filename}>"

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "caption": self.caption,
            "alt_text": self.alt_text,
            "upload_date": self.upload_date.isoformat(),
            "url": f"/static/uploads/recipes/{self.filename}"
        }