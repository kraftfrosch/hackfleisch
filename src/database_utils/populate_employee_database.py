import os
import sys
from supabase import create_client, Client
from pprint import pprint

# initialize your Supabase client
db_web_link = "https://hkqvoplmxbycptpqjghe.supabase.co"
keyy = os.getenv('SUPABASE_KEY', "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhrcXZvcGxteGJ5Y3B0cHFqZ2hlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njg2ODA4MywiZXhwIjoyMDYyNDQ0MDgzfQ.wLT-6nThQhgXGREUEThA5Uzb6KcrU8ITwgGfTI_dd5A")

def load_employee_directory():
    """Load and display all employees from the directory."""
    try:
        # Query all records from the employee_directory table
        response = supabase.table("employee_directory").select("*").execute()
        
        if response.data:
            print("\nEmployee Directory Contents:")
            print("=" * 80)
            for employee in response.data:
                print(f"\nName: {employee['name']}")
                print(f"Department: {employee['department']}")
                print(f"Job Title: {employee['job_title']}")
                print(f"Skills: {', '.join(employee['skillset'])}")
                print(f"Projects: {', '.join(employee['projects'])}")
                print(f"Personal History: {employee['personal_history']}")
                print("-" * 80)
            print(f"\nTotal employees found: {len(response.data)}")
        else:
            print("No employees found in the directory.")
            
    except Exception as e:
        print(f"Error loading employee directory: {str(e)}")

# Initialize Supabase client
print("Initializing Supabase client...")
try:
    supabase: Client = create_client(db_web_link, keyy)
    print("Successfully initialized Supabase client")
except Exception as e:
    print(f"Error initializing Supabase client: {str(e)}")
    sys.exit(1)

# 1) Create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS employee_directory (
    id              SERIAL       PRIMARY KEY,
    name            TEXT         NOT NULL,
    department      TEXT         NOT NULL,
    skillset        TEXT[]       NOT NULL,
    job_title       TEXT         NOT NULL,
    projects        TEXT[]       NOT NULL,
    personal_history TEXT        NOT NULL
);
"""
print("\nCreating employee_directory table...")
try:
    result = supabase.rpc('execute_sql', {'query': create_table_sql}).execute()
    print("Successfully created employee_directory table")
except Exception as e:
    print(f"Error creating table: {str(e)}")
    sys.exit(1)

# 2) Insert 10 employees
print("\nStarting employee data insertion...")
success_count = 0
error_count = 0

employees = [
    {
        "name": "Fabian",
        "department": "Engineering",
        "skillset": ["Python", "Django", "Docker"],
        "job_title": "Senior Backend Engineer",
        "projects": ["API v2", "Deployment Automation"],
        "personal_history": (
            "Fabian grew up in Berlin and developed an early interest in computing, "
            "leading him to pursue a degree in computer science at TU Berlin. "
            "After graduation, he contributed to open-source projects before joining "
            "the company to focus on backend development."
        )
    },
    {
        "name": "Vishwa",
        "department": "Data Science",
        "skillset": ["SQL", "R", "TensorFlow"],
        "job_title": "Data Scientist",
        "projects": ["Customer Churn Model", "Sales Forecasting"],
        "personal_history": (
            "Vishwa was born in Mumbai and studied statistics at IIT Bombay. "
            "He completed a master's in machine learning at UCL, and worked on "
            "several R&D projects before bringing his expertise to our data team."
        )
    },
    {
        "name": "Johannes",
        "department": "Product",
        "skillset": ["Roadmapping", "User Research", "Figma"],
        "job_title": "Product Manager",
        "projects": ["Mobile App Redesign", "Feature Prioritization"],
        "personal_history": (
            "Johannes hails from Vienna, where he earned a dual degree in business "
            "and psychology. He began his career in UX research before transitioning "
            "to product management in the tech sector."
        )
    },
    {
        "name": "Joshua",
        "department": "Marketing",
        "skillset": ["SEO", "Content Strategy", "Google Ads"],
        "job_title": "Marketing Specialist",
        "projects": ["SEO Overhaul", "Campaign Q3"],
        "personal_history": (
            "Joshua grew up in London and studied communications at King's College. "
            "He cut his teeth at a digital agency, running paid-search and content campaigns, "
            "and now drives our online presence."
        )
    },
    {
        "name": "Maria",
        "department": "Sales",
        "skillset": ["Negotiation", "CRM", "Presentation"],
        "job_title": "Account Executive",
        "projects": ["Enterprise Deals", "Partner Outreach"],
        "personal_history": (
            "Maria is from Madrid and holds a degree in international business. "
            "She started in B2B sales at a SaaS startup and consistently exceeded quotas."
        )
    },
    {
        "name": "Aisha",
        "department": "Human Resources",
        "skillset": ["Recruiting", "Onboarding", "Labor Law"],
        "job_title": "HR Manager",
        "projects": ["Talent Acquisition", "Employee Wellness"],
        "personal_history": (
            "Aisha was raised in Cairo and studied human resource management at AUC. "
            "She has over 8 years of experience establishing hiring pipelines and culture programs."
        )
    },
    {
        "name": "Carlos",
        "department": "Finance",
        "skillset": ["Excel", "Budgeting", "SAP"],
        "job_title": "Financial Analyst",
        "projects": ["Quarterly Forecast", "Cost Analysis"],
        "personal_history": (
            "Carlos is originally from São Paulo and holds a finance degree from USP. "
            "He spent five years at a Big Four firm before joining our finance team."
        )
    },
    {
        "name": "Chen",
        "department": "Design",
        "skillset": ["Adobe XD", "Illustrator", "Sketch"],
        "job_title": "UI/UX Designer",
        "projects": ["Web Dashboard", "Brand Guidelines"],
        "personal_history": (
            "Chen comes from Shanghai and studied graphic design at the Central Academy "
            "of Fine Arts. She has a keen eye for minimalistic interfaces."
        )
    },
    {
        "name": "Priya",
        "department": "Customer Success",
        "skillset": ["Zendesk", "Account Management", "Training"],
        "job_title": "Customer Success Lead",
        "projects": ["Onboarding Program", "Retention Initiative"],
        "personal_history": (
            "Priya grew up in Bangalore and holds an MBA from ISB. "
            "She's passionate about building long-term client relationships and runs our CS team."
        )
    },
    {
        "name": "David",
        "department": "Operations",
        "skillset": ["Logistics", "Process Improvement", "ERP"],
        "job_title": "Operations Manager",
        "projects": ["Supply Chain Optimization", "Vendor Management"],
        "personal_history": (
            "David is from Toronto and earned an engineering degree at U of T. "
            "He spent several years improving manufacturing workflows before joining us."
        )
    }
]

for employee in employees:
    # try:
    result = supabase.table("employee_directory").insert(employee).execute()
    print(f"✓ Successfully added employee: {employee['name']}")
    success_count += 1
    # except Exception as e:
    #     print(f"✗ Error adding employee {employee['name']}: {str(e)}")
    #     error_count += 1

print(f"\nInsertion complete. Successfully added {success_count} employees. Failed to add {error_count} employees.")

# Call the function to load and display the directory
if __name__ == "__main__":
    load_employee_directory()
