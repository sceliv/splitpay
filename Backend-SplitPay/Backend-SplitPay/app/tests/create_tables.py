from app.database import Base, engine
from app.models.user import User
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.expense import Expense
from app.models.settlement import Settlement

print("Creando tablas...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas.")
