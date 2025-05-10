from supabase import create_client
from dotenv import load_dotenv
import os

def load_env():
    load_dotenv()
    return {
        "supabase_url": os.getenv("SUPABASE_URL"),
        "supabase_key": os.getenv("SUPABASE_KEY")
    }

def create_table():
    env = load_env()
    supabase = create_client(env["supabase_url"], env["supabase_key"])

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS personality (
        id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
        unique_email text,
        openness int,
        conscientiousness int,
        extraversion int,
        agreeableness int,
        neuroticism int,
        iq int,
        eq int,
        advice_manager text,
        advice_colleagues text,
        reasoning text,
        inserted_at timestamp with time zone DEFAULT timezone('utc'::text, now())
    );
    """

    response = supabase.rpc('execute_sql', {'query': create_table_sql}).execute()

    if response.data is not None:
        print("✅ Table created or already exists.")
    else:
        print(f"❌ Failed to create table. Response: {response}")

if __name__ == "__main__":
    create_table()
