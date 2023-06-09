from match_job_app.models import (
Employer,
Employee
)
from random import choice
from typing import Tuple

class RandomUserRoller:

    def __init__(self) -> None:
        self.emoployyes = Employee.objects.all()
        self.employers = Employer.objects.all()

    def random_one_eployee_and_employer(self) -> Tuple[Employee,Employer]:

        pack_employee_employer = (choice(self.emoployyes),choice(self.employers))
        return pack_employee_employer
