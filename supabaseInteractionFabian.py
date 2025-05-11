from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get credentials from environment variables
db_web_link = os.getenv("SUPABASE_URL")
keyy = os.getenv("SUPABASE_KEY")

if not db_web_link or not keyy:
    raise ValueError("Missing required environment variables SUPABASE_URL or SUPABASE_KEY")

supabase: Client = create_client(db_web_link, keyy)

create_table_sql = """
CREATE TABLE IF NOT EXISTS competency_framework (
    uuid UUID PRIMARY KEY,
    type TEXT NOT NULL,
    applicable_to TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    level_1 TEXT,
    level_2 TEXT,
    level_3 TEXT,
    level_4 TEXT,
    created_at TIMESTAMP DEFAULT now()
);
"""

# 2. Execute table creation via RPC
supabase.rpc('execute_sql', {'query': create_table_sql}).execute()
print("✅ Table created successfully.")

# 3. Insert first 3 dummy entries
dummy_data = [
    {
        "uuid": "279fbcf7-8951-411f-979e-6e6a59f79be8",
        "type": "core",
        "applicable_to": "company",
        "name": "Ownership for collective achievement",
        "description": "Understand what needs to be done and take ownership for getting it over the finish line.",
        "level_1": "Consistently completes tasks and communicates delays.",
        "level_2": "Sets ambitious goals and aligns them with company direction.",
        "level_3": "Pushes through blockers and improves standards.",
        "level_4": "Inspires others and fosters a culture of shared success."
    },
    {
        "uuid": "93fefac1-eef6-41e1-a931-6705eeb18ae5",
        "type": "core",
        "applicable_to": "company",
        "name": "Trustful collaboration",
        "description": "Build trust by being reliable and communicating transparently.",
        "level_1": "Shows up, contributes respectfully, and shares updates.",
        "level_2": "Divides and tracks work collectively.",
        "level_3": "Builds strong relationships and adapts communication.",
        "level_4": "Fosters psychological safety and models transparency."
    },
    {
        "uuid": "14cd0195-a468-41a6-aa96-90f7e20366c7",
        "type": "core",
        "applicable_to": "company",
        "name": "Bias for action and positivity",
        "description": "Tackle challenges head-on with positivity and focus.",
        "level_1": "Stays positive and keeps moving through challenges.",
        "level_2": "Energizes others and offers simple solutions.",
        "level_3": "Boosts team morale and inspires action.",
        "level_4": "Builds a culture of action, positivity, and alignment."
    }
]

# 4. Insert data
for entry in dummy_data:
    supabase.table("competency_framework").insert(entry).execute()
print("✅ 3 dummy rows inserted.") 