from sqlalchemy.orm import Session
from app.models.document import Document

class DocumentRepository:
    @staticmethod
    def create(db: Session, document: Document):
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def get_all(db: Session):
        return db.query(Document).all()

    @staticmethod
    def get(db: Session, document_id):
        return db.get(Document, document_id)

    @staticmethod
    def delete(db: Session, document):
        db.delete(document)
        db.commit()