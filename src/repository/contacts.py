# src\repository\contacts.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
import sys

sys.path.append(str(BASE_DIR))

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdatedModel


async def get_contacts(limit: int, offset: int, db: Session):
    """
    Get list of contacts from database with limit and offset

    :param limit: The maximum number of contacts to retrieve
    :param offset: Offset to select a specific subset of contacts
    :param db: The SQLAlchemy session object
    :return: List of contacts
    """
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    """     
    Retrieve a contact from the database by its ID 
    
    :param contact_id: Contact ID
    :param db: The SQLAlchemy session object
    :return: Contact or None if not found
     """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create(body: ContactModel, db: Session):
    """
    Create a new contact in the database based on the provided data

    :param body: Data for creating a new contact
    :param db: The SQLAlchemy session object
    :return: Contact created
    """
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    """
    Update an existing contact in the database by its ID

    :param contact_id: The ID of the contact to update
    :param body: Data to update the contact
    :param db: The SQLAlchemy session object
    :return: Updated contact or None if not found
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    """
    Delete a contact from the database by its ID

    :param contact_id: The ID of the contact to delete
    :param db: The SQLAlchemy session object
    :return: The deleted contact or None if not found
    
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def set_updated(contact_id: int, body: ContactUpdatedModel, db: Session):
    '''
    Set the update flag for a contact by its ID

    :param contact_id: The ID of the contact to set the update flag for
    :param body: Data to set the update flag
    :param db: The SQLAlchemy session object
    :return: Contact or None if not found
    '''
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.update = body.update
        db.commit()
    return contact
