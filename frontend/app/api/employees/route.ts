import { NextResponse } from "next/server"
import { createClient } from "@supabase/supabase-js"

// Server-side access to environment variables
const supabaseUrl = process.env.SUPABASE_URL || ""
const supabaseKey = process.env.SUPABASE_KEY || ""
const supabase = createClient(supabaseUrl, supabaseKey)

// The correct table name in your Supabase database
const TABLE_NAME = "employee"

export async function GET() {
  try {
    const { data, error } = await supabase.from(TABLE_NAME).select("*")

    if (error) {
      console.error("Error fetching employees:", error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json(data)
  } catch (error) {
    console.error("Error in employees API route:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
