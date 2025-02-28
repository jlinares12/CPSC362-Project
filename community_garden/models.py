from community_garden import db

user_garden_volunteer = db.Table(
    'user_garden_volunteer',  # Name of the table
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),  # Foreign key to User
    db.Column('garden_id', db.Integer(), db.ForeignKey('garden.id'), primary_key=True)  # Foreign key to Garden
)

class User(db.Model):
    id = db.Column( db.Integer(), primary_key=True, nullable=False, unique=True )
    name = db.Column( db.String(length=30), nullable=False, unique=True )
    email = db.Column( db.String(length=320), nullable=False, unique=True)
    # Relationship to Garden (assuming a Garden table exists)
    administered_gardens = db.relationship('Garden', backref='admin', lazy=True)

    volunteer_gardens = db.relationship(
        'Garden',  # Target model
        secondary=user_garden_volunteer,  # Association table
        backref='volunteers'  # Name of the reverse relationship
    )

    def __repr__(self):
        return f'{self.name}'

class Garden(db.Model):
    id = db.Column(db.Integer(), primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(length=50), nullable=False)
    admin_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    
    def __repr__(self):
        return f'{self.name}'