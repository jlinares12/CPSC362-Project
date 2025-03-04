from community_garden import db, bcrypt, login_manager
from sqlalchemy import JSON
from flask_login import UserMixin


# Bridge to connect users and gardens to form a many-to-many relationship between volunteers and gardens
user_garden_volunteer = db.Table(
    'user_garden_volunteer',                                                                # Name of the table
    db.Column( 'user_id',   db.Integer(), db.ForeignKey( 'user.id'   ), primary_key=True ), # Foreign key to User
    db.Column( 'garden_id', db.Integer(), db.ForeignKey( 'garden.id' ), primary_key=True )  # Foreign key to Garden
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_passaword):
        return bcrypt.check_password_hash(self.password_hash, attempted_passaword)

    volunteered_gardens = db.relationship( 'Garden', secondary=user_garden_volunteer, backref='volunteers', lazy=True )
        # Many-to-many relationship
        # 'Garden'  =  Target model
        # 'user_garden_volunteer' = Association table
        # 'volunteers' = allows us to get the list of volunteers when referencing a garden
        # "lazy=True", allows us to get all garden's a use has volunteered in one command

    def __repr__(self):
        return f'{self.name}'

class Garden(db.Model):
    id             = db.Column( db.Integer(           ), primary_key=True                        )
    name           = db.Column( db.String ( length=50 ), nullable=False                          )
    street_address = db.Column( db.String ( length=70 ), nullable=False,           unique=True   )
    city           = db.Column( db.String ( length=35 ), nullable=False                          )
    wish_list      = db.Column( JSON                                                             )
    admin_id       = db.Column( db.Integer(           ), db.ForeignKey('user.id'), nullable=False)  # Foreign key to User
    def __repr__(self):
        return f'{self.name}'