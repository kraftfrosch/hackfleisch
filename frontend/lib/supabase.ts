import { createClient } from "@supabase/supabase-js"

// This file should only be imported in server components or API routes
// Never import this in client components

// Server-side only - these environment variables are not exposed to the client
const supabaseUrl = process.env.SUPABASE_URL || ""
const supabaseKey = process.env.SUPABASE_KEY || ""

// Create the Supabase client for server-side use only
export const supabase = createClient(supabaseUrl, supabaseKey)

// Add a warning to prevent accidental client-side usage
if (typeof window !== "undefined") {
  console.error(
    "WARNING: lib/supabase.ts should only be imported in server components or API routes. " +
      "For client-side functionality, use the API endpoints instead.",
  )
}
