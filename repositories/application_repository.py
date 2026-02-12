from models.models import Application

def create_application(db, application_data):
    db_application = Application(**application_data)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_application(db, application_id):
    return db.query(Application).filter(Application.id == application_id).first()