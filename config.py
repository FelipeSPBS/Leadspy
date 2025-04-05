import os

class Config:
    SECRET_KEY = os.urandom(24)  # chave secreta para autenticação
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:hd1450@localhost:5432/typebot'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
