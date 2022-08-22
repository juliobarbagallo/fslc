from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from app.api.db import db
from app.api.model.cuboid import Cuboid


class Bag(db.Model):
    __tablename__ = "bags"

    id = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=True)
    cuboids = db.relationship(Cuboid, backref="bag")


    @hybrid_property
    def payload_volume(self):
        payload_volume = 0
        for cuboid in self.cuboids:
            payload_volume += cuboid.volume
        return payload_volume


    @hybrid_property
    def available_volume(self):
        return self.volume - self.payload_volume


    @hybrid_method
    def has_volume(self, cuboid, updated_cuboid):
        # adds = 1
        current_taken_volume = 0
        for each_cub in self.cuboids:
            if each_cub.id != cuboid:
                # adds = each_cub.width * each_cub.height * each_cub.depth
                current_taken_volume += each_cub.volume
                # adds = 1
        available_volume = self.volume - current_taken_volume
        new_cubo_volume = updated_cuboid.width * updated_cuboid.height * updated_cuboid.depth
        return bool(available_volume >= new_cubo_volume)
        