from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object('automarked.config')
Bootstrap(app)

db = SQLAlchemy(app)
hs = Bcrypt(app)

import automarked.views