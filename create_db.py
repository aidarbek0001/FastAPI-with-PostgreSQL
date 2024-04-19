from database import Base, engine
from models import User, Pizza  # Импортируйте все необходимые модели

print("Creating database...")
Base.metadata.create_all(engine)


