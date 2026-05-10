from project import validate_date, validate_status, Job
from datetime import datetime as dt
import pytest


# 1. Date Validation Tests:
def test_validate_date_valid():
    assert validate_date("2025-01-01") == True

def test_validate_date_future():
    assert validate_date("2099-01-01") == False

def test_validate_date_wrong_format():
    assert validate_date("01-01-2025") == False

def test_validate_date_invalid_month():
    assert validate_date("2025-13-01") == False

def test_validate_date_letters():
    assert validate_date("abcd-ef-gh") == False


# 2. Status Validation Tests:
def test_validate_status_applied():
    assert validate_status("Applied") == True

def test_validate_status_interview():
    assert validate_status("Interview") == True

def test_validate_status_offer():
    assert validate_status("Offer") == True

def test_validate_status_rejected():
    assert validate_status("Rejected") == True

def test_validate_status_lowercase():
    assert validate_status("applied") == True

def test_validate_status_invalid():
    assert validate_status("Maybe") == False


# 3. Job Class Tests:
def test_job_to_dict_keys():
    job = Job("Google", "Data Analyst", "2025-01-01", "Applied", "LinkedIn")
    assert list(job.to_dict().keys()) == ["company", "role", "date", "status", "notes"]

def test_job_to_dict_values():
    job = Job("Google", "Data Analyst", "2025-01-01", "Applied", "LinkedIn")
    assert job.to_dict()["company"] == "Google"
    assert job.to_dict()["role"] == "Data Analyst"
    assert job.to_dict()["status"] == "Applied"

def test_job_str():
    job = Job("Google", "Data Analyst", "2025-01-01", "Applied", "LinkedIn")
    assert "Google" in str(job)
    assert "Data Analyst" in str(job)
    assert "Applied" in str(job)