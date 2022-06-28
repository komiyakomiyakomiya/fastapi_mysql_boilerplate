from fastapi import FastAPI, APIRouter
import routers.user as user_router
import routers.book as book_router

router = APIRouter()
router.include_router(
    user_router.router,
    prefix='/users',
    tags=['users']
)

router.include_router(
    book_router.router,
    prefix='/books',
    tags=['books']
)

app = FastAPI()
app.include_router(router)


# @app.get('/')
# async def hello():
#     return 'hello'
