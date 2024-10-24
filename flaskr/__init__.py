import os

from flask import ( Flask, render_template)

def create_app(test_config=None):
   # création et configuration de l'app
   app = Flask(__name__, instance_relative_config=True)
   app.config.from_mapping(
      SECRET_KEY="dev",
      DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
   )

   if test_config is None:
      # charger l'instance de la config depuis le fichier
      app.config.from_pyfile("config.py", silent=True)
   else:
      # charger la config passée en paramètre
      app.config.from_mapping(test_config)
   
   try:
      os.makedirs(app.instance_path)
   except OSError:
      pass

   # une simple page qui dit hello
   @app.route("/")
   def home():
      return render_template("index.html")
   
   from . import db
   db.init_app(app)

   from . import dataviz
   app.register_blueprint(dataviz.bp)
   
   return app