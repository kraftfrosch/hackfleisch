import { NextResponse } from "next/server"
import { createClient } from "@supabase/supabase-js"

// Server-side access to environment variables
const supabaseUrl = process.env.SUPABASE_URL || ""
const supabaseKey = process.env.SUPABASE_KEY || ""
const supabase = createClient(supabaseUrl, supabaseKey)

// The correct table name in your Supabase database
const TABLE_NAME = "employee"

export async function GET(request: Request, { params }: { params: { id: string } }) {
  try {
    const projectId = params.id

    // Query all employees with the same project ID
    const { data, error } = await supabase.from(TABLE_NAME).select("id, Name, picture, role").eq("project", projectId)

    if (error) {
      console.error(`Error fetching team members for project ${projectId}:`, error)
      return NextResponse.json({ error: error.message }, { status: 500 })
    }

    return NextResponse.json(data)
  } catch (error) {
    console.error("Error in project members API route:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
