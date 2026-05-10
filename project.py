import re
import csv
import sys
from tabulate import tabulate as tb
from datetime import datetime as dt 


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
    return bool((re.fullmatch(r"\d{4}-(?P<month>1[0-2]|0[1-9])-(?P<days>0[1-9]|[1-2][0-9]|3[0-1])", date)) and (dt.strptime(date, "%Y-%m-%d") < dt.today()))

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
        i_company= input(f"{'Company Name':<30}: ").strip().capitalize()
        if len(i_company)<3:
            print("Enter minimum 3 characters! Try again!")
            continue
        else:
            break
    
    while True:
        i_role= input(f"{'Role Applied':<30}: ").capitalize()
        if len(i_role)<2:
            print("Enter minimum 2 characters! Try again! ")
            continue
        else:
            break
    
    while True:
        i_date= input(f"{'Date Applied(yyyy-mm-dd)':<30}: ")
        if validate_date(i_date):
            break
        else:
            print("Invalid date format!! Try Again!")
            continue

    while True:
        i_status= input(f"{'Status':<30}: ").capitalize()
        if validate_status(i_status):
            break
        else:
            print("Invalid Status!! Select one from below:\n1. applied\n2. interview\n3. rejected\n4. offer")
            continue
                    
    i_notes= input(f"{'Notes':<30}: ") or "No notes availabele".capitalize()
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

# 7. Show Stats
def shows_stats():
    jobs=load_jobs()
    if len(jobs)<1:
        print("No job application found!!")
        return
    total=0
    applied=0
    interview=0
    offer=0
    rejected=0

    for job in jobs:
        if job.status.lower()=="applied":
            applied+=1
        elif job.status.lower()=="interview":
            interview+=1
        elif job.status.lower()=="offer":
            offer+=1
        else:
            rejected+=1
        total+=1

    responseratio= ((interview + offer + rejected)/total)*100

    print("-" * 30)
    print(f"{'| Total Application':<22}: {total}")
    print(f"{'| Applied':<22}: {applied}")
    print(f"{'| Interview':<22}: {interview}")
    print(f"{'| Rejected':<22}: {rejected}")
    print(f"{'| Offer':<22}: {offer}")
    print(f"{'| Response Ratio':<22}: {responseratio:.2f}%")
    print("-" * 30)

# 8. Filter Jobs using keyword:
def filter_job(keyword):
    jobs=load_jobs()
    if len(jobs)<1:
        print("No job application found!!")
        return
    search_list=[]
    for job in jobs:
        if (keyword.lower() in job.company.lower() or keyword.lower() in job.role.lower() or keyword.lower() in job.status.lower()):
            search_list.append(list(job.to_dict().values()))
    
    if len(search_list)>=1:
        return tb(search_list, headers=["Company", "Role", "Date", "Status", "Notes" ], tablefmt="grid")
    else:
        return(f"No job application found with keyword {keyword}")

# 9. Main Function:
def main():
    try:
        if len(sys.argv) < 2:
            raise ValueError
        elif len(sys.argv) == 2:
            if sys.argv[1]=="--add":
                add_job()
            elif sys.argv[1]=="--list":
                print(list_jobs())
            elif sys.argv[1]=="--stats":
                shows_stats()
            else:
                raise ValueError
        elif len(sys.argv)==3 and sys.argv[1]=="--filter":
            print(filter_job(sys.argv[2]))
        else:
            raise ValueError
    
    except ValueError:
        sys.exit("Usuage:\n python project.py --add\n python project.py --list\n python project.py --stats\n python project.py --filter <keyword>")


if __name__ == "__main__":
    main()
 