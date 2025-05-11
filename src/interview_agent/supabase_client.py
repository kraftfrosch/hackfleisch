import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Missing Supabase credentials. Please ensure SUPABASE_URL and SUPABASE_KEY are set in your environment variables."
    )

# Initialize Supabase client
SUPABASE_CLIENT: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Export the client for use in other modules
__all__ = ["SUPABASE_CLIENT"]
