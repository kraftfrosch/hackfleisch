"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { Project } from "@/types/employee"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Check } from "lucide-react"
import { chatEvents } from "./employee-chat"
import { useState } from "react"
import { useToast } from "@/components/ui/use-toast"

interface ProjectCardProps {
  project: Project
  employeeId: string
}

export function ProjectCard({ project, employeeId }: ProjectCardProps) {
  const [isRequestingFeedback, setIsRequestingFeedback] = useState(false)
  const [memberFeedbackStatus, setMemberFeedbackStatus] = useState<Record<string, boolean>>(() => {
    // Initialize with the current status - assume no feedback collected initially
    const initialStatus: Record<string, boolean> = {}
    project.teamMembers.forEach((member) => {
      initialStatus[member.id] = false // Default to no feedback collected
    })
    return initialStatus
  })
  const { toast } = useToast()

  const formatDate = (dateString?: string) => {
    if (!dateString) return "Present"
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
    })
  }

  const handleRequestFeedback = (memberId: string, memberName: string) => {
    setIsRequestingFeedback(true)

    // Get the name of the employee whose profile is being viewed
    const currentEmployeeName = project.teamMembers.find((member) => member.id === employeeId)?.name || "the employee"

    // Base prompt that explains the context of the request (only for API)
    const basePrompt = `I am interacting with you through a chat window in ${currentEmployeeName}'s profile. Please only collect, process and explain feedback about this person.`

    // Create the feedback request message for the specific team member (for API)
    const apiMessage = `${basePrompt} I'd like to request feedback on the "${project.name}" project from ${memberName}. Please analyze their skills and contributions in relation to ${currentEmployeeName}.`

    // Create a user-friendly message (for display in chat)
    const displayMessage = `I'd like to request feedback on the "${project.name}" project from ${memberName}. Please analyze their skills and contributions.`

    // Add the message to the chat with separate display and API messages
    chatEvents.addMessage(employeeId, displayMessage, apiMessage)

    // Update state to show feedback has been requested for this member
    setMemberFeedbackStatus((prev) => ({
      ...prev,
      [memberId]: true,
    }))

    // Show toast notification
    toast({
      title: "Feedback Requested",
      description: `Feedback request for ${memberName} has been sent to the assistant.`,
    })

    setIsRequestingFeedback(false)
  }

  return (
    <Card className="mb-4 relative bg-slate-50 dark:bg-slate-900/20">
      <CardHeader>
        <CardTitle>{project.name}</CardTitle>
      </CardHeader>

      <CardContent>
        <div className="mb-4">
          <p className="text-sm text-muted-foreground mb-2">
            {formatDate(project.startDate)} - {formatDate(project.endDate)}
          </p>
          <p>{project.description}</p>
        </div>

        <div>
          <h4 className="text-sm font-medium mb-4">Team Members ({project.teamMembers.length})</h4>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {project.teamMembers.map((member) => (
              <div key={member.id} className="flex flex-col items-center text-center relative">
                <Avatar className="h-10 w-10 mb-1">
                  <AvatarImage src={member.avatar || "/placeholder.svg"} alt={member.name} />
                  <AvatarFallback>
                    {member.name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </AvatarFallback>
                </Avatar>
                <span className="text-xs truncate w-full">{member.name}</span>
                {member.role && (
                  <span className="text-xs text-muted-foreground truncate w-full h-4">{member.role}</span>
                )}
                {!member.role && <div className="h-4"></div>}

                <div className="mt-2 w-full">
                  {member.id === employeeId ? (
                    <span className="inline-block w-full text-xs px-2 py-1 bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300 rounded-full">
                      No Feedback Needed
                    </span>
                  ) : memberFeedbackStatus[member.id] ? (
                    <span className="inline-block w-full text-xs px-2 py-1 bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300 rounded-full">
                      <Check className="h-3 w-3 inline mr-1" />
                      Feedback Collected
                    </span>
                  ) : (
                    <button
                      onClick={() => handleRequestFeedback(member.id, member.name)}
                      disabled={isRequestingFeedback}
                      className="w-full text-xs px-2 py-1 bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300 rounded-full hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
                    >
                      Request Feedback
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
