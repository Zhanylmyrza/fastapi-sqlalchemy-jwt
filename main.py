import os
import sys


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

try:
    from .models import Base
    from .database import engine
    from .routers import auth, todos, admin, users
except ImportError:
    from models import Base
    from database import engine
    from routers import auth, todos, admin, users

from fastapi import FastAPI, Depends

def create_app():
    app = FastAPI()
    
    app.include_router(auth.router)
    app.include_router(todos.router)
    app.include_router(admin.router)
    app.include_router(users.router)
    
    @app.get('/healthy')
    def health_check():
        return {'status': 'healthy'}
    
    return app

app = create_app()