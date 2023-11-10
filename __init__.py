from trytond.pool import Pool
from . import mileage

def register():
    Pool.register(
        mileage.Mileage,
        mileage.Period,
        mileage.Employee,
        mileage.AccountConfiguration,
        mileage.MileageCompany,
        mileage.Move,
        module='employee_mileage', type_='model'
    )