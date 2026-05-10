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
        print("─" * 65)
        i_company= input(f"{'Company Name':<45}: ").strip().capitalize()
        if len(i_company)<3:
            print("\n⚠️  Enter minimum 3 characters! Try again!")
            print("─" * 45)
            continue
        else:
            break
    
    while True:
        i_role= input(f"{'Role Applied':<45}: ").capitalize()
        if len(i_role)<2:
            print("\n⚠️  Enter minimum 2 characters! Try again! ")
            print("─" * 45)
            continue
        else:
            break
    
    while True:
        i_date= input(f"{'Date Applied(yyyy-mm-dd)':<45}: ")
        if validate_date(i_date):
            break
        else:
            print("\n⚠️  Invalid date format!! Try Again!")
            print("─" * 45)
            continue

    while True:
        i_status= input(f"{'Status (applied/interview/offer/rejected)':<45}: ").capitalize()
        if validate_status(i_status):
            break
        else:
            print("\n⚠️  Invalid Status!! Select one from below:\n1. applied\n2. interview\n3. rejected\n4. offer")
            print("─" * 45)
            continue
                    
    i_notes= input(f"{'Notes':<45}: ") or "No notes available".capitalize()
    job= Job(i_company,i_role,i_date,i_status,i_notes)
    save_job(job)
    print(f"\n✅  Job at {i_company} for {i_role} role successfully added!!")
    print("─" * 65)

# 6. List Job:
def list_jobs():
    jobs=load_jobs()
    if len(jobs)<1:
        print("-"*45)
        print("⚠️ No job application found!!")
        print("-"*45)
        return
    result=[]
    for number, job in enumerate(jobs, start=1):
        result.append([number] + list(job.to_dict().values()))

    return tb(result, headers=["#", "Company", "Role", "Date", "Status", "Notes" ], tablefmt="grid")

# 7. Show Stats
def shows_stats():
    jobs=load_jobs()
    if len(jobs)<1:
        print("⚠️  No job application found!!")
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

    print("-" * 45)
    print(f"{'| Total Application':<22}: {total}")
    print(f"{'| Applied':<22}: {applied}")
    print(f"{'| Interview':<22}: {interview}")
    print(f"{'| Rejected':<22}: {rejected}")
    print(f"{'| Offer':<22}: {offer}")
    print(f"{'| Response Ratio':<22}: {responseratio:.2f}%")
    print("-" * 45)

# 8. Filter Jobs using keyword:
def filter_job(keyword):
    jobs=load_jobs()
    if len(jobs)<1:
        print("-"*45)
        print("⚠️  No job application found!!")
        print("-"*45)
        return
    search_list=[]
    for job in jobs:
        if (keyword.lower() in job.company.lower() or keyword.lower() in job.role.lower() or keyword.lower() in job.status.lower()):
            search_list.append(list(job.to_dict().values()))
    
    if len(search_list)>=1:
        return tb(search_list, headers=["Company", "Role", "Date", "Status", "Notes" ], tablefmt="grid")
    else:
        return(f"--------------------------------------------------------\n⚠️  No job application found with keyword '{keyword}'\n--------------------------------------------------------")

# 9. Update Job Status:
def update_job():
    print(list_jobs())
    jobs=load_jobs()
    while True:
        try:
            job_number= int(input("\nEnter Job Number to Update: "))
            if job_number < 1 or job_number > len(jobs):
                raise ValueError
            break
        except ValueError:
            print("\n⚠️  Invalid Input!!\nEnter a number OR Enter number within range.")
            print("─" * 45)
            continue
    
    while True:
        try:
            update= input("What would you like to update? (Status/Notes): ").strip().capitalize()
            if update in ("Status", "Notes"):
                break
            else:
                raise ValueError

        except ValueError:
            print("\n⚠️  Invalid Input!!\nChoose Status or Notes.") 
            print("─" * 45)
            continue
    
    if update== "Status":
        while True:
            new_value= input("New Status (applied/interview/offer/rejected): ").strip().capitalize()
            if validate_status(new_value):
                break
            else:
                print("\n⚠️  Invalid Status!!")
                print("─" * 45)
                continue

    elif update == "Notes":
        while True:
            new_value = input("New Notes: ").strip().capitalize()
            if len(new_value) > 0:
                break
            else:
                print("\n⚠️  Notes cannot be empty!")
                print("─" * 45)

    setattr(jobs[job_number - 1], update.lower(), new_value)

    with open("application.csv", "w", newline="") as file:
        writer= csv.DictWriter(file, fieldnames=["company", "role", "date", "status", "notes"])
        writer.writeheader()

        for job in jobs:
            writer.writerow(job.to_dict())
    print(f"\n✅  {update} updated successfully!")
    print("─" * 45)


    while True:
        try:
            result= input("Press 'p' for listing jobs OR Press 'q' to exit: ").lower()
            if result== "p":
                print(list_jobs())
                break
            elif result== "q":
                sys.exit()
            else:
                raise ValueError
        except ValueError:
            print("\n⚠️  Press 'p' or 'q'")
            print("─" * 45)
            continue
    
            


    



# 10. Main Function:
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
            elif sys.argv[1]=="--update":
                update_job()
            else:
                raise ValueError
        elif len(sys.argv)==3 and sys.argv[1]=="--filter":
            print(filter_job(sys.argv[2]))
        else:
            raise ValueError
    
    except ValueError:
        sys.exit("\n-----------------------------------------------------------------------------------------\nUsuage:\n python project.py --add\n python project.py --list\n python project.py --stats\n python project.py --filter <keyword>\n python project.py --update\n-----------------------------------------------------------------------------------------\n")


if __name__ == "__main__":
    main()
 