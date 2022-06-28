from database import SessionLocal
from utils import utils


if __name__ == '__main__':
    db = SessionLocal()
    utils.create_users(utils.user_objs, db)
    # delete_user_by_ids(user_ids)
