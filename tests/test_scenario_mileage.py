import datetime
import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.account.tests.tools import (create_chart,
                                                 create_fiscalyear,
                                                 get_accounts)
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules


class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Activate modules
        activate_modules('employee_mileage')
        Configuration = Model.get('account.configuration')
        Journal = Model.get('account.journal')

        # Create company
        _ = create_company()
        company = get_company()

        # Create fiscal year
        fiscalyear = create_fiscalyear(company)
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)
        accounts = get_accounts(company)
        payable = accounts['payable']

        # Create parties
        Party = Model.get('party.party')
        customer = Party(name='Customer')
        customer.save()
        address, = customer.addresses

        # Configure journal
        journal, = Journal.find([], limit=1)
        Configuration = Model.get('account.configuration')
        configuration = Configuration()
        configuration.employee_mileage_journal = journal
        configuration.save()

        # Create Employee
        Employee = Model.get('company.employee')
        Party = Model.get('party.party')
        employee_party = Party(name='Employee')
        employee_party.save()
        employee = Employee()
        employee.company = company
        employee.price_per_km = Decimal('6.8785')
        employee.debit_account = payable
        employee.party = employee_party
        employee.save()

        # Create Mileage Period
        Period = Model.get('employee.mileage.period')
        period = Period()
        period.name = 'Name'
        period.employee = employee
        mileage = period.mileage.new()
        mileage.distance = 4
        mileage.address = address
        mileage.date = datetime.date.today()
        mileage.period = period
        period.save()

        # Buttons
        period.click('confirm')
        period.click('post')

        # Check move
        self.assertNotEqual(period.move, None)
        self.assertEqual(period.move.origin, period)
        lines = sorted(period.move.lines, key=lambda x: x.debit)
        self.assertEqual(lines[0].credit, Decimal('27.51'))
        self.assertEqual(lines[0].debit, Decimal('0'))
        self.assertEqual(lines[1].debit, Decimal('27.51'))
        self.assertEqual(lines[1].credit, Decimal('0'))
