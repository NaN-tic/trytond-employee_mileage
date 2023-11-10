======================
Mileage Scenario
======================

Imports::

    >>> from decimal import Decimal
    >>> from proteus import Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts
    >>> import datetime

Activate modules::

    >>> config = activate_modules('employee_mileage')
    >>> Configuration = Model.get('account.configuration')
    >>> Journal = Model.get('account.journal')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = create_fiscalyear(company)
    >>> fiscalyear.click('create_period')

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> payable = accounts['payable']

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.save()

Configure journal::

    >>> journal, = Journal.find([], limit=1)
    >>> Configuration = Model.get('account.configuration')
    >>> configuration = Configuration()
    >>> configuration.employee_mileage_journal = journal
    >>> configuration.save()

Create Employee::

    >>> Employee = Model.get('company.employee')
    >>> Party = Model.get('party.party')
    >>> employee_party = Party(name='Employee')
    >>> employee_party.save()
    >>> employee = Employee()
    >>> employee.company = company
    >>> employee.price_per_km = Decimal('6.8785')
    >>> employee.debit_account = payable
    >>> employee.party = employee_party
    >>> employee.save()

Create Mileage Period::

    >>> Period = Model.get('employee.mileage.period')
    >>> period = Period()
    >>> period.name = 'Name'
    >>> period.employee = employee
    >>> mileage = period.mileage.new()
    >>> mileage.distance = 4
    >>> mileage.address = customer
    >>> mileage.date = datetime.date.today()
    >>> mileage.period = period
    >>> period.save()
   
Buttons::

    >>> period.click('confirm')
    >>> period.click('post')

Check move::

    >>> period.move != None
    True
    >>> period.move.origin == period
    True
    >>> lines = sorted(period.move.lines, key=lambda x: x.debit)
    >>> lines[0].credit
    Decimal('27.51')
    >>> lines[0].debit
    Decimal('0')
    >>> lines[1].debit
    Decimal('27.51')
    >>> lines[1].credit
    Decimal('0')
