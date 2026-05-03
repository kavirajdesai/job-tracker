import re
import csv
import sys
from tabulate import tabulate as tb 


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
    

# 1. Date Validation:
def validate_date(date):
    return bool(re.fullmatch(r"\d{4}-(?P<month>1[0-2]|0[1-9])-(?P<days>0[1-9]|[1-2][0-9]|3[0-1])", date))

# 2. Status Validation:
def validate_status(status):
    return status.lower() in ("applied", "interview", "offer", "rejected")

# 3. Append Job:
def save_job(job):
    with open("application.csv", "a", newline="") as file:
        writer= csv.DictWriter(file, fieldnames=["company", "role", "date", "status", "notes"])
        job= job.to_dict()
        writer.writerow(job)

# 4. Load Jobs:
def load_jobs():
    job_list=[]
    with open("application.csv", "r") as file:
        reader=csv.DictReader(file)
        for row in reader:
            job_list.append(Job(row["company"], row["role"], row["date"], row["status"], row["notes"]))
    
    return job_list       
                
# 5. Add Job:
def add_job():
    while True:
        i_company= input("Company Name:").strip()
        if len(i_company)<3:
            print("Enter minimum 3 characters! Try again!")
            continue
        else:
            break
    
    while True:
        i_role= input("Role Applied:")
        if len(i_role)<2:
            print("Enter minimum 2 characters! Try again! ")
            continue
        else:
            break
    
    while True:
        i_date= input("Date Applied(yyyy-mm-dd):")
        if validate_date(i_date):
            break
        else:
            print("Invalid date format!! Try Again!")
            continue

    while True:
        i_status= input("Status:")
        if validate_status(i_status):
            break
        else:
            print("Invalid Status!! Select one from below:\n1. applied\n2. interview\n3. rejected\n4. offer")
            continue
                    
    i_notes= input("Notes: ") or "No notes availabele"
    job= Job(i_company,i_role,i_date,i_status,i_notes)
    save_job(job)
    print(f"Job at {i_company} for {i_role} role successfully added!!")

# 6. List Job:
def list_jobs():
    jobs=load_jobs()
    if len(jobs)<1:
        print("No job application found!!")
        return
    result=[]
    for number, job in enumerate(jobs, start=1):
        result.append([number] + list(job.to_dict().values()))

    return tb(result, headers=["#", "Company", "Role", "Date", "Status", "Notes" ], tablefmt="grid")
print(list_jobs())
'''TEST FUNCTIONS'''

# 1. Date Validation:
# print(validate_date("2025-05-01"))   # True
# print(validate_date("01-05-2025"))   # False
# print(validate_date("abcd-ef-gh"))   # False


# 2. Status Validation:
# print(validate_status("Applied"))    # True
# print(validate_status("Rejected"))   # True
# print(validate_status("Maybe"))      # False
# print(validate_status("applied"))    # True — case insensitive


# 3. Save Job:
# job = Job("Apple", "Data Analyst", "2025-05-01", "Applied", "Handshake")
# save_job(job)

# 4. Load Jobs:
# jobs = load_jobs()
# for job in jobs:
#     print(job)


# if __name__ == "__main__":
#     job = Job("Google", "Data Analyst", "2025-05-01", "Applied", "LinkedIn")
#     print(job)
#     print(job.to_dict())

 