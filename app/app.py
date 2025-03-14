from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # Use o URI do banco de dados desejado
    db.init_app(app)
    
    # Importa init_routes aqui para evitar importação circular
    from app_routes import init_routes
    init_routes(app)
    
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)