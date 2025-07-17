class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Qwerty123456!@127.0.0.1:3306/sdp_project"
    SECRET_KEY = "your_secret_key"
    JWT_SECRET_KEY = "your_jwt_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
