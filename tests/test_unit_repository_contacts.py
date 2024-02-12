from pathlib import Path
import unittest
BASE_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.append(str(BASE_DIR))

import pytest

from datetime import date
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdatedModel
from src.repository.contacts import get_contacts, get_contact_by_id, create, remove, update, set_updated


class TestContactsRepository(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.contact_from_test = ContactModel(
                    id=1,
                    first_name='Simon',
                    last_name='Cowell',
                    email ='Simon@exampl.ex',
                    phone_number = '+380959155738',
                    birth_date = date(1959, 10, 7),
                    additional_data = 'British television producer, competition shows Britain\'s Got Talent (2007–present)'
                    )

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().limit().offset().all.return_value = contacts
        result = await get_contacts(10, 0, self.session)
        self.assertEqual(result, contacts)


    async def test_create_contact(self):
        body = self.contact_from_test
        result = await create(body, self.session)
        # print(result)
        self.assertEqual(result.first_name, body.first_name)
        self.assertTrue(hasattr(result, 'id'))
    

    @pytest.mark.asyncio
    async def test_get_contact_by_id(self):
        test_contact = Contact(
            id=1,
            first_name='John',
            last_name='Doe',
            email='John@example.com',
            phone_number='+987654321',
            birth_date=date(2000, 1, 1),
            additional_data='TestAdditionalData'
        )
        self.session.query().filter_by().first.return_value = test_contact

        result_contact = await get_contact_by_id(test_contact.id, self.session)


        self.assertIsNotNone(result_contact)
        self.assertEqual(result_contact.id, test_contact.id)
        self.assertEqual(result_contact.first_name, test_contact.first_name)
        self.assertEqual(result_contact.last_name, test_contact.last_name)
        self.assertEqual(result_contact.email, test_contact.email)
        self.assertEqual(result_contact.phone_number, test_contact.phone_number)
        self.assertEqual(result_contact.birth_date, test_contact.birth_date)
        self.assertEqual(result_contact.additional_data, test_contact.additional_data)


    @pytest.mark.asyncio
    async def test_update_contact(self):
        test_contact = Contact(
            first_name='John',
            last_name='Doe',
            email='John@example.com',
            phone_number='+987654321',
            birth_date=date(2000, 1, 1),
            additional_data='TestAdditionalData'
        )

        # Оновлення тестового контакту
        updated_data = ContactModel(
            first_name='Mike',
            last_name='Tyson',
            email='Mike_Tyson@example.com',
            phone_number='+123456789',
            birth_date=date.today(),
            additional_data='UpdatedAdditionalData'
        )

        updated_contact = await update(test_contact.id, updated_data, self.session)

        # Перевірка, чи контакт оновлено коректно
        assert updated_contact is not None
        assert updated_contact.first_name == updated_data.first_name
        assert updated_contact.last_name == updated_data.last_name
        assert updated_contact.email == updated_data.email
        assert updated_contact.phone_number == updated_data.phone_number
        assert updated_contact.birth_date == updated_data.birth_date
        assert updated_contact.additional_data == updated_data.additional_data

    @pytest.mark.asyncio
    async def test_remove_contact(self):
        # Створення тестового контакту в базі даних
        test_contact = Contact(
                id=1,
                first_name='TestFirstName',
                last_name='TestLastName',
                email='test.email@example.com',
                phone_number='+987654321',
                birth_date=date(2000, 1, 1),
                additional_data='TestAdditionalData'
                )

        # Виклик функції видалення
        removed_contact = await remove(test_contact.id, self.session)

        # Перевірка, чи контакт видалено
        assert removed_contact is not None

        # Перевірка, чи контакт видалено з бази даних
        assert self.session.delete.called
        assert self.session.commit.called

    
    @pytest.mark.asyncio
    async def test_set_updated_contact(self):
        # Створення тестового контакту в базі даних
        test_contact = Contact(
                id=1,
                first_name='test_first_name',
                last_name='test_last_name',
                email='test_update.email@example.com',
                phone_number='+4165165484',
                birth_date=date(2000, 1, 1),
                additional_data='something data'
                )

        # Виклик функції set_updated
        updated_data = ContactUpdatedModel(updated=True)
        updated_contact = await set_updated(test_contact.id, updated_data, self.session)

        # Перевірка, чи контакт оновлено коректно
        assert updated_contact is not None
        assert updated_contact.update == updated_data.update

        # Перевірка, чи контакт оновлено в базі даних
        assert self.session.commit.called
