import uuid
from app import create_app, db
from app.models.user import User
from app.models.role import Role
from app.security.password import hash_password

ADMIN_USER_ID = uuid.UUID("543c73ca-2f9c-420f-a789-6ab770ef0f39")
ADMIN_EMAIL = "admin@admin.com.br"


def run_seed():
    app = create_app()

    with app.app_context():
        created = False

        # -------- ROLE --------
        role = Role.query.filter_by(id=1).first()
        if not role:
            role = Role(id=1, name="Admin")
            db.session.add(role)
            created = True
            print("✔ Role Admin criada")
        else:
            print("ℹ Role Admin já existe")

        # -------- USER --------
        user = User.query.filter_by(email=ADMIN_EMAIL).first()
        if not user:
            user = User(
                id=ADMIN_USER_ID,
                name="Admin",
                email=ADMIN_EMAIL,
                password_hash=hash_password("123"),
                role_id=1,
                is_active=True
            )
            db.session.add(user)
            created = True
            print("✔ Usuário Admin criado")
        else:
            print("ℹ Usuário Admin já existe")

        if created:
            db.session.commit()
        else:
            db.session.rollback()