"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ProjectCard } from "@/components/project-card"
import { ChevronUp, ChevronDown } from "lucide-react"
import type { Project } from "@/types/employee"

interface ProjectsSectionProps {
  projects: Project[]
  employeeName: string
  employeeId: string
}

export function ProjectsSection({ projects, employeeName, employeeId }: ProjectsSectionProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  // Sort projects by start date (newest first)
  const sortedProjects = [...projects].sort((a, b) => new Date(b.startDate).getTime() - new Date(a.startDate).getTime())

  // Get the latest project
  const latestProject = sortedProjects.length > 0 ? sortedProjects[0] : null

  // Determine which projects to display based on expanded state
  const projectsToDisplay = isExpanded ? sortedProjects : latestProject ? [latestProject] : []

  return (
    <Card className="w-full mb-6">
      <CardHeader className="pb-2 flex flex-row items-center justify-between">
        <CardTitle>{employeeName}'s Projects</CardTitle>
        {projects.length > 1 && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="h-8 w-8 p-0"
            aria-label={isExpanded ? "Collapse projects" : "Expand projects"}
          >
            {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </Button>
        )}
      </CardHeader>
      <CardContent>
        {projectsToDisplay.length > 0 ? (
          <div className="space-y-4">
            {projectsToDisplay.map((project) => (
              <ProjectCard key={project.id} project={project} employeeId={employeeId} />
            ))}
          </div>
        ) : (
          <p className="text-center text-muted-foreground py-4">No projects found for this employee.</p>
        )}

        {!isExpanded && projects.length > 1 && (
          <div className="text-center mt-2">
            <Button variant="ghost" size="sm" onClick={() => setIsExpanded(true)}>
              Show {projects.length - 1} more {projects.length - 1 === 1 ? "project" : "projects"}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
