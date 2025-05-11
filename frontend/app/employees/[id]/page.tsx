"use client"

import { useState, useEffect } from "react"
import { Header } from "@/components/header"
import { SkillCard } from "@/components/skill-card"
import { EmployeeChat } from "@/components/employee-chat"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { ChevronLeft, Mail, Phone, Calendar, Users, RefreshCw } from "lucide-react"
import Link from "next/link"
import { ProjectsSection } from "@/components/projects-section"
import { fetchEmployeeById, fetchEmployeeSkills, fetchEmployeeProjects } from "@/services/employee-service"
import { mapDbEmployeeToEmployee } from "@/types/employee"
import type { Employee, Skill, Project } from "@/types/employee"
import { useToast } from "@/components/ui/use-toast"
import { DemoFeedbackPopup } from "@/components/demo-feedback-popup"
import { NextStepsPopup } from "@/components/next-steps-popup"
import { PopupProvider, usePopup } from "@/contexts/popup-context"

function EmployeeDetailContent({ params }: { params: { id: string } }) {
  const [employee, setEmployee] = useState<Employee | null>(null)
  const [skills, setSkills] = useState<Skill[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const { setShowDemoPopup } = usePopup()
  const { toast } = useToast()

  const loadEmployeeData = async () => {
    try {
      setLoading(true)

      // Fetch employee details
      const dbEmployee = await fetchEmployeeById(params.id)
      if (!dbEmployee) {
        setError("Employee not found")
        return
      }

      // Map DB employee to our app's Employee type
      const employeeData = mapDbEmployeeToEmployee(dbEmployee)
      setEmployee(employeeData)

      // Fetch skills
      const skillsData = await fetchEmployeeSkills(params.id)
      setSkills(skillsData)

      // Fetch projects
      const projectsData = await fetchEmployeeProjects(params.id)
      setProjects(projectsData)

      setError(null)
    } catch (err) {
      console.error("Failed to fetch employee data:", err)
      setError("Failed to load employee data. Please try again later.")
      toast({
        title: "Error",
        description: "Failed to load employee data. Please try again later.",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
      setIsRefreshing(false)
    }
  }

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await loadEmployeeData()
    toast({
      title: "Refreshed",
      description: "Employee data has been refreshed.",
    })
  }

  useEffect(() => {
    loadEmployeeData()

    // Show the demo popup after a short delay
    const timer = setTimeout(() => {
      setShowDemoPopup(true)
    }, 500)

    return () => clearTimeout(timer)
  }, [params.id, setShowDemoPopup])

  if (loading && !isRefreshing) {
    return (
      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex-1 p-6 flex justify-center items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </main>
      </div>
    )
  }

  if (error || !employee) {
    return (
      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex-1 p-6">
          <Button variant="ghost" asChild className="mb-4">
            <Link href="/">
              <ChevronLeft className="mr-2 h-4 w-4" />
              Back to Employees
            </Link>
          </Button>
          <Card>
            <CardContent className="p-6">
              <div className="text-center">
                <p className="text-red-500 mb-4">{error || "Employee not found"}</p>
                <Button onClick={loadEmployeeData}>Try Again</Button>
              </div>
            </CardContent>
          </Card>
        </main>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1 p-6">
        <div className="mb-6">
          <div className="flex justify-between items-center mb-4">
            <Button variant="ghost" asChild>
              <Link href="/">
                <ChevronLeft className="mr-2 h-4 w-4" />
                Back to Employees
              </Link>
            </Button>

            <Button
              variant="outline"
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="flex items-center gap-2"
            >
              <RefreshCw className={`h-4 w-4 ${isRefreshing ? "animate-spin" : ""}`} />
              {isRefreshing ? "Refreshing..." : "Refresh"}
            </Button>
          </div>

          <Card className="mb-6">
            <CardContent className="p-6">
              <div className="flex flex-col md:flex-row gap-8">
                {/* Left column - Avatar and basic info */}
                <div className="flex flex-col items-center text-center md:w-1/4">
                  <Avatar className="h-32 w-32 mb-4">
                    <AvatarImage src={employee.avatar || "/placeholder.svg?height=128&width=128"} alt={employee.name} />
                    <AvatarFallback>
                      {employee.name
                        .split(" ")
                        .map((n) => n[0])
                        .join("")}
                    </AvatarFallback>
                  </Avatar>
                  <h2 className="text-2xl font-bold">{employee.name}</h2>
                  <p className="text-muted-foreground mb-2">{employee.position}</p>
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                      employee.status === "Active"
                        ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                        : "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
                    }`}
                  >
                    {employee.status}
                  </span>
                </div>

                {/* Right section - Details */}
                <div className="flex-1">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Contact info */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-medium">Contact Information</h3>
                      <div className="space-y-3">
                        {employee.email && (
                          <div className="flex items-center">
                            <Mail className="h-4 w-4 mr-3 text-muted-foreground" />
                            <span>{employee.email}</span>
                          </div>
                        )}
                        {employee.phone && (
                          <div className="flex items-center">
                            <Phone className="h-4 w-4 mr-3 text-muted-foreground" />
                            <span>{employee.phone}</span>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Work info */}
                    <div className="space-y-4">
                      <h3 className="text-lg font-medium">Work Information</h3>
                      <div className="grid grid-cols-1 gap-4">
                        {employee.department && (
                          <div className="flex items-center">
                            <Users className="h-4 w-4 mr-3 text-muted-foreground" />
                            <span>CDTM Class of Spring 2025</span>
                          </div>
                        )}
                        {employee.hireDate && (
                          <div className="flex items-center">
                            <Calendar className="h-4 w-4 mr-3 text-muted-foreground" />
                            <span>Hire Date: {new Date(employee.hireDate).toLocaleDateString()}</span>
                          </div>
                        )}
                        {employee.manager && (
                          <div className="flex items-start">
                            <Users className="h-4 w-4 mr-3 text-muted-foreground mt-1" />
                            <div>
                              <span className="block">Manager: {employee.manager}</span>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Bio section */}
                  {employee.bio && (
                    <div className="mt-6 pt-4 border-t">
                      <h3 className="text-lg font-medium mb-2">Bio</h3>
                      <p className="text-muted-foreground">{employee.bio}</p>
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Popups */}
          {employee && <DemoFeedbackPopup employeeId={employee.id} employeeName={employee.name} />}
          <NextStepsPopup />

          {/* Chat section */}
          <div className="mb-6">
            <EmployeeChat employeeId={employee.id} employeeName={employee.name} />
          </div>

          {/* Projects section */}
          {projects.length > 0 && (
            <ProjectsSection projects={projects} employeeName={employee.name} employeeId={employee.id} />
          )}

          {/* Skills section */}
          {skills.length > 0 && (
            <div>
              <h2 className="text-xl font-bold mb-4">Skills & Feedback</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {skills.map((skill, index) => (
                  <SkillCard key={index} skill={skill} />
                ))}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default function EmployeeDetailPage({ params }: { params: { id: string } }) {
  return (
    <PopupProvider>
      <EmployeeDetailContent params={params} />
    </PopupProvider>
  )
}
