export interface DbEmployee {
  id: string
  Name: string
  picture?: string
  role?: string
  bio?: string
  project?: string
  phone?: string
  project_responsibilities?: string
  satisfaction?: number

  // Competency 1
  competency_name1?: string
  competency_description1?: string
  competency_currentlevel1?: number
  competency_proposed_level1?: number
  justification1?: any

  // Competency 2
  competency_name2?: string
  compentency_description2?: string
  competency_currentlevel2?: number
  competency_proposed_level2?: number
  justification2?: any

  // Competency 3
  competency_name3?: string
  compentency_description3?: string
  competency_currentlevel3?: number
  competency_proposed_level3?: number
  justification3?: any

  // Competency 4
  competency_name4?: string
  compentency_description4?: string
  competency_currentlevel4?: number
  competency_proposed_level4?: number
  justification4?: any
}

export interface Employee {
  id: string
  name: string
  position: string
  department?: string
  email?: string
  phone?: string
  hireDate?: string
  manager?: string
  status: "Active" | "On Leave" | "Terminated"
  bio?: string
  avatar?: string
  satisfaction?: number
}

export interface FeedbackItem {
  text: string
  direct_quote?: string
  justification: string
  type: "positive" | "negative" | "constructive"
}

export interface Skill {
  skill_name: string
  employee_level: number
  proposed_level?: number
  level_description: string
  reasoning: string
  feedback_quotes: FeedbackItem[]
}

export interface ChatMessage {
  id: string
  content: string
  sender: "user" | "assistant"
  timestamp: Date
}

export interface TeamMember {
  id: string
  name: string
  avatar: string
  role?: string
}

export interface Project {
  id: string
  name: string
  description: string
  startDate: string
  endDate?: string
  feedbackCollected: boolean
  teamMembers: TeamMember[]
  responsibilities?: string
}

// Helper function to convert DB employee to our app's Employee type
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

// Helper function to extract skills from DB employee
export function extractSkillsFromDbEmployee(dbEmployee: DbEmployee): Skill[] {
  const skills: Skill[] = []

  // Helper function to process each competency
  const processCompetency = (
    name?: string,
    description?: string,
    currentLevel?: number,
    proposedLevel?: number,
    justification?: any,
  ) => {
    if (!name || currentLevel === undefined) return null

    // Parse justification JSON if it exists
    let feedbackQuotes: FeedbackItem[] = []
    const reasoning = description || "No description available"

    if (justification) {
      try {
        // If justification is a string, parse it
        let justData = justification
        if (typeof justification === "string") {
          justData = JSON.parse(justification)
        }

        // Handle array of feedback items
        if (Array.isArray(justData)) {
          feedbackQuotes = justData.map((item) => {
            // Map the type from the database to our application types
            let feedbackType: "positive" | "negative" | "constructive" = "constructive"
            if (item.type === "positive") {
              feedbackType = "positive"
            } else if (item.type === "negative") {
              feedbackType = "negative"
            } else if (item.type === "actionable_advice") {
              feedbackType = "constructive"
            }

            return {
              text: item.quote || "",
              direct_quote: item.direct_quote || "",
              justification: item.justification || "",
              type: feedbackType,
            }
          })
        }
      } catch (e) {
        console.error("Error parsing justification:", e)
      }
    }

    return {
      skill_name: name,
      employee_level: currentLevel,
      proposed_level: proposedLevel,
      level_description: getLevelDescription(currentLevel),
      reasoning: reasoning,
      feedback_quotes:
        feedbackQuotes.length > 0
          ? feedbackQuotes
          : [{ text: "No feedback available", justification: "", type: "constructive" }],
    }
  }

  // Helper function to get level description based on level number
  const getLevelDescription = (level: number): string => {
    switch (level) {
      case 1:
        return "Basic"
      case 2:
        return "Intermediate"
      case 3:
        return "Advanced"
      case 4:
        return "Expert"
      default:
        return "Unknown"
    }
  }

  // Process each competency
  const skill1 = processCompetency(
    dbEmployee.competency_name1,
    dbEmployee.competency_description1,
    dbEmployee.competency_currentlevel1,
    dbEmployee.competency_proposed_level1,
    dbEmployee.justification1,
  )
  if (skill1) skills.push(skill1)

  const skill2 = processCompetency(
    dbEmployee.competency_name2,
    dbEmployee.competency_description2,
    dbEmployee.competency_currentlevel2,
    dbEmployee.competency_proposed_level2,
    dbEmployee.justification2,
  )
  if (skill2) skills.push(skill2)

  const skill3 = processCompetency(
    dbEmployee.competency_name3,
    dbEmployee.competency_description3,
    dbEmployee.competency_currentlevel3,
    dbEmployee.competency_proposed_level3,
    dbEmployee.justification3,
  )
  if (skill3) skills.push(skill3)

  const skill4 = processCompetency(
    dbEmployee.competency_name4,
    dbEmployee.competency_description4,
    dbEmployee.competency_currentlevel4,
    dbEmployee.competency_proposed_level4,
    dbEmployee.justification4,
  )
  if (skill4) skills.push(skill4)

  return skills
}
