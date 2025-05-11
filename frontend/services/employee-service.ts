import {
  type DbEmployee,
  type Employee,
  type Skill,
  type Project,
  type TeamMember,
  extractSkillsFromDbEmployee,
} from "@/types/employee"

// Correct table name in Supabase
const EMPLOYEES_TABLE = "employee"

// In the mapDbEmployeeToEmployee function, ensure we're mapping the satisfaction field
export function mapDbEmployeeToEmployee(dbEmployee: DbEmployee): Employee {
  return {
    id: dbEmployee.id,
    name: dbEmployee.Name,
    position: dbEmployee.role || "Employee",
    department: "Not specified",
    status: "Active",
    bio: dbEmployee.bio,
    avatar: dbEmployee.picture,
    phone: dbEmployee.phone,
    satisfaction: dbEmployee.satisfaction,
  }
}

// Fetch all employees
export async function fetchEmployees(): Promise<Employee[]> {
  try {
    const response = await fetch("/api/employees")

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = (await response.json()) as DbEmployee[]
    return data.map(mapDbEmployeeToEmployee)
  } catch (error) {
    console.error("Error in fetchEmployees:", error)
    return []
  }
}

// Fetch a single employee by ID
export async function fetchEmployeeById(id: string): Promise<DbEmployee | null> {
  try {
    const response = await fetch(`/api/employees/${id}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = (await response.json()) as DbEmployee
    return data
  } catch (error) {
    console.error(`Error in fetchEmployeeById for ID ${id}:`, error)
    return null
  }
}

// Get skills for an employee
export async function fetchEmployeeSkills(employeeId: string): Promise<Skill[]> {
  try {
    const employee = await fetchEmployeeById(employeeId)
    if (!employee) return []

    return extractSkillsFromDbEmployee(employee)
  } catch (error) {
    console.error(`Error in fetchEmployeeSkills for ID ${employeeId}:`, error)
    return []
  }
}

// Fetch team members for a project
export async function fetchProjectTeamMembers(projectId: string): Promise<TeamMember[]> {
  try {
    const response = await fetch(`/api/projects/${projectId}/members`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    // Map the data to TeamMember type
    return data.map((member: any) => ({
      id: member.id,
      name: member.Name,
      avatar: member.picture || "/placeholder.svg?height=40&width=40",
      role: member.role || "Team Member",
    }))
  } catch (error) {
    console.error(`Error in fetchProjectTeamMembers for project ID ${projectId}:`, error)
    return []
  }
}

// Fetch project details by ID
export async function fetchProjectById(projectId: string): Promise<any | null> {
  try {
    const response = await fetch(`/api/projects/${projectId}`)

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error(`Error in fetchProjectById for ID ${projectId}:`, error)
    return null
  }
}

// Get projects for an employee with all team members
export async function fetchEmployeeProjects(employeeId: string): Promise<Project[]> {
  try {
    const employee = await fetchEmployeeById(employeeId)
    if (!employee || !employee.project) return []

    // Fetch project details from the project table
    const projectDetails = await fetchProjectById(employee.project)

    // Fetch all team members for this project
    const teamMembers = await fetchProjectTeamMembers(employee.project)

    return [
      {
        id: employee.project,
        name: projectDetails?.name || "Unknown Project",
        description: projectDetails?.description || employee.project_responsibilities || "No description available",
        startDate: projectDetails?.start_date || new Date().toISOString().split("T")[0],
        endDate: projectDetails?.end_date,
        feedbackCollected: false,
        teamMembers: teamMembers,
        responsibilities: employee.project_responsibilities,
      },
    ]
  } catch (error) {
    console.error(`Error in fetchEmployeeProjects for ID ${employeeId}:`, error)
    return []
  }
}
