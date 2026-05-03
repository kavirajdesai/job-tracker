import re

class Job:
    def __init__(self, company, role, date, status, notes):
        self.company= company
        self.role= role
        self.date= date
        self.status=status
        self.notes= notes

    def to_dict(self):
        data= {
            "company": self.company,
            "role": self.role,
            "date": self.date,
            "status": self.status,
            "notes": self.notes,
        }

        return data
    
    def __str__(self):
        return (f"{self.company} | {self.role} | {self.date} | {self.status} | {self.notes}")
    

# Date Validation:
def validate_date(date):
    if (matches:= re.fullmatch(r"\d{4}-(?P<month>1[0-2]|0[1-9])-(?P<days>0[1-9]|[1-2][0-9]|3[0-1])", date)):
        return True
    else:
        return False


#TEST FUNCTIONS
print(validate_date("2025-05-01"))   # True
print(validate_date("01-05-2025"))   # False
print(validate_date("abcd-ef-gh"))   # False

# if __name__ == "__main__":
#     job = Job("Google", "Data Analyst", "2025-05-01", "Applied", "LinkedIn")
#     print(job)
#     print(job.to_dict())


 