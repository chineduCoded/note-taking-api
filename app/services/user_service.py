
User = {}
db = {}

class UserService:

    @staticmethod
    def get_user_by_id(user_id: int):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_user(email: str, password: str):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update_user(user_id: int, email: str, password: str):
        user = UserService.get_user_by_id(user_id)
        user.email = email
        user.password = password
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id: int):
        user = UserService.get_user_by_id(user_id)
        db.session.delete(user)
        db.session.commit()
        return user

    @staticmethod
    def get_all_users():
        return User.query.all()
    
    @staticmethod
    def authenticate_user(credentials: dict) -> str:
        email = credentials.get('email')
        password = credentials.get('password')
        user = UserService.get_user_by_email(email)
        if user and user.password == password:
            return 'Authenticated'
        return 'Not authenticated'
    
    @staticmethod
    def authorize_user(user_id: str, action: str, resource_id: str) -> bool:
        return True
    
    @staticmethod
    def get_user_info(user_id: int):
        user = UserService.get_user_by_id(user_id)
        return {
            'email': user.email,
            'password': user.password
        }
    
    @staticmethod
    def get_users_info():
        users = UserService.get_all_users()
        return [{
            'email': user.email,
            'password': user.password
        } for user in users]