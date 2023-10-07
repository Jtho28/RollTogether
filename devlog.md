Creating a database model in Flask is managed by an ORM (Object-Relational  
  Mapper) that allows applications to manage a database using high-level      
  entities such as classes, objects and methods instead of tables and SQL.    
  Here's an example of how to define a model using Flask-SQLAlchemy which is a
  Flask extension that simplifies the use of SQLAlchemy, which is an SQL      
  toolkit and ORM.                                                            
                                                                              
  First, install Flask-SQLAlchemy:                                            
                                                                              
    pip install Flask-SQLAlchemy                                              
                                                                              
  Next, we need to configure our database and initiate the SQLAlchemy object: 
                                                                              
    from flask import Flask                                                   
    from flask_sqlalchemy import SQLAlchemy                                   
                                                                              
    app = Flask(__name__)                                                     
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # This  
  can be any database                                                         
    db = SQLAlchemy(app)                                                      
                                                                              
  Next, you define your model (i.e., the table) in your database:             
                                                                              
    class User(db.Model):                                                     
        id = db.Column(db.Integer, primary_key=True)                          
        username = db.Column(db.String(80), unique=True, nullable=False)      
        email = db.Column(db.String(120), unique=True, nullable=False)        
                                                                              
        def __repr__(self):                                                   
            return '<User %r>' % self.username                                
                                                                              
  In this example,  User  is the model, which we declare as a class that      
  inherits from  db.Model .  id ,  username  and  email  are the fields in the
  model. The  db.Column  specifies the column in our Model.                   
                                                                              
  After defining your models, create the tables in the database with the      
  following command:                                                          
                                                                              
    db.create_all()                                                           
                                                                              
  Remember that  db.create_all()  will only creates tables for which a model  
  is defined and it's not already present in the database. It won't update or 
  alter existing tables.                                                      
                                                                              
  You can create a new  User  object (i.e., a record) as follows:             
                                                                              
    admin = User(username='admin', email='admin@example.com')                 
    db.session.add(admin)                                                     
    db.session.commit()                                                       
                                                                              
  You're essentially done! You can now interact with the  User  model to      
  create, retrieve, update, and delete records in your table. You should refer
  to the Flask-SQLAlchemy documentation for more complex usage. 


Yes, it is possible to have a field that only accepts values within a certain range, like 1 to 10, in Flask-SQLAlchemy. You can use SQLAlchemy's `CheckConstraint`.

But please note, SQLite, which comes by default with Python, ignores this `CheckConstraint`.

Here is how you can do it:

```python
from sqlalchemy.schema import CheckConstraint

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        CheckConstraint('score>=1 AND score<=10', name='score_check'),
    )
```

In this example, a `User` can only have a score between 1 and 10. The `CheckConstraint` ensures that the score inserted is between 1 and 10.

Please note if your database is SQLite it wouldn't enforce this constraint because SQLite does not support this, but in PostgreSQL or MySQL, this constraint would work.

