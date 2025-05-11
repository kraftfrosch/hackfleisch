// This file contains safe methods for client components to interact with Supabase
// without exposing sensitive environment variables

/**
 * Example of a client-safe function that fetches data through an API route
 * instead of directly using Supabase credentials
 */
export async function fetchDataSafely(endpoint: string) {
  try {
    const response = await fetch(`/api/${endpoint}`)
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error(`Error fetching from ${endpoint}:`, error)
    throw error
  }
}

// Add more client-safe methods as needed
