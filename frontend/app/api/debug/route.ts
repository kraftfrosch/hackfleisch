import { NextResponse } from "next/server"
import { createClient } from "@supabase/supabase-js"

// Server-side access to environment variables
const supabaseUrl = process.env.SUPABASE_URL || ""
const supabaseKey = process.env.SUPABASE_KEY || ""
const supabase = createClient(supabaseUrl, supabaseKey)

export async function GET() {
  try {
    // Check connection by getting the list of tables
    const { data, error } = await supabase.from("pg_tables").select("tablename").eq("schemaname", "public")

    if (error) {
      console.error("Error connecting to Supabase:", error)
      return NextResponse.json(
        {
          success: false,
          error: error.message,
          url: supabaseUrl ? "URL is set" : "URL is missing",
          key: supabaseKey ? "Key is set" : "Key is missing",
        },
        { status: 500 },
      )
    }

    return NextResponse.json({
      success: true,
      message: "Successfully connected to Supabase",
      tables: data.map((row) => row.tablename),
    })
  } catch (error) {
    console.error("Error in debug API route:", error)
    return NextResponse.json(
      {
        success: false,
        error: "Internal server error",
        message: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 },
    )
  }
}
