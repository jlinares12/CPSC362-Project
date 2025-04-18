from __init__ import db, bcrypt, login_manager, geolocator
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Bridge to connect users and gardens to form a many-to-many relationship between volunteers and gardens
user_garden_volunteer = db.Table(
    'user_garden_volunteer',
    db.Column( 'user_id',   db.Integer(), db.ForeignKey( 'user.id'   ), primary_key=True ), # Foreign key to User
    db.Column( 'garden_id', db.Integer(), db.ForeignKey( 'garden.id' ), primary_key=True )  # Foreign key to Garden
)

class User(db.Model, UserMixin):
    # Data
    id            = db.Column( db.Integer(),            primary_key=True            )
    name          = db.Column( db.String( length=50 ),  nullable=False              )
    username      = db.Column( db.String( length=20 ),  nullable=False, unique=True )
    email         = db.Column( db.String( length=65 ),  nullable=False, unique=True )
    password_hash = db.Column( db.String( length=60 ),  nullable=False              )
    # Relationships
    administered_gardens = db.relationship( 'Garden', backref='admin', lazy=True )
        # one-to-many relationship
        # 'Garden' = Target Model,
        # 'admin' = how we will get the admin of a garden when referencing a garden (garden.admin)
        # "lazy=True", allows us to get all gardens a user administer in one command
    volunteered_gardens = db.relationship('Garden', secondary=user_garden_volunteer, backref='volunteer_list', lazy=True)
        # Many-to-many relationship
        # 'Garden'  =  Target model
        # 'user_garden_volunteer' = Association table
        # 'volunteers' = allows us to get the list of volunteers when referencing a garden
        # "lazy=True", allows us to get all garden's a use has volunteered in one command

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'{self.name}'

class Garden(db.Model):
    id                 = db.Column( db.Integer (            ), primary_key=True                        )
    name               = db.Column( db.String  ( length=50  ), nullable=False                          )
    street_address     = db.Column( db.String  ( length=70  ), nullable=False,           unique=True   )
    city               = db.Column( db.String  ( length=35  ), nullable=False                          )
    state              = db.Column( db.String  ( length=2   )                                          )
    zip_code           = db.Column( db.String  ( length=5   )                                          )
    hours_of_operation = db.Column( db.String  ( length=70  ), nullable=False                          )
    wish_list          = db.Column( db.String  ( length=200 )                                          )
    description        = db.Column( db.String  ( length=500 ), unique=True                             )
    donation_link      = db.Column( db.String  ( length=500 ))
    admin_id           = db.Column( db.Integer (            ), db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    photo              = db.Column( db.String  ( length=100 ), nullable=False,           unique=True   )
    latitude           = db.Column( db.Float (            ))
    longitude          = db.Column( db.Float (            ))
    volunteers = db.Relationship('User', secondary=user_garden_volunteer, viewonly=True)

    def create_coordinates(self):
        location = geolocator.geocode(self.street_address)
        self.latitude = location.latitude
        self.longitude = location.longitude

    def __repr__(self):
        return f'{self.name}'