"use client"

import { useState, useEffect } from "react"
import { Header } from "@/components/header"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Search } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { fetchEmployees } from "@/services/employee-service"
import type { Employee } from "@/types/employee"
import { useToast } from "@/components/ui/use-toast"
import { WelcomePopup } from "@/components/welcome-popup"

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState("")
  const [showWelcomePopup, setShowWelcomePopup] = useState(false)
  const { toast } = useToast()

  const loadEmployees = async () => {
    try {
      setLoading(true)
      const data = await fetchEmployees()
      setEmployees(data)
      setError(null)
    } catch (err) {
      console.error("Failed to fetch employees:", err)
      setError("Failed to load employees. Please try again later.")
      toast({
        title: "Error",
        description: "Failed to load employees. Please try again later.",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadEmployees()

    // Show welcome popup after a short delay
    const timer = setTimeout(() => {
      setShowWelcomePopup(true)
    }, 500)

    return () => clearTimeout(timer)
  }, [])

  const handleCloseWelcomePopup = () => {
    setShowWelcomePopup(false)
  }

  // Filter employees based on search term
  const filteredEmployees = employees.filter((employee) => {
    if (searchTerm === "") return true

    const searchLower = searchTerm.toLowerCase()
    return (
      employee.name.toLowerCase().includes(searchLower) ||
      (employee.position && employee.position.toLowerCase().includes(searchLower)) ||
      (employee.email && employee.email.toLowerCase().includes(searchLower))
    )
  })

  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1 p-6">
        <Card className="border-0 shadow-none">
          <CardHeader className="pb-2">
            <CardTitle>Employee Directory</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center mb-4">
              <div className="relative w-full max-w-sm">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  type="search"
                  placeholder="Search employees..."
                  className="w-full pl-8"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>

            {loading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : error ? (
              <div className="text-center p-4">
                <p className="text-red-500 mb-4">{error}</p>
                <Button onClick={loadEmployees}>Try Again</Button>
              </div>
            ) : (
              <>
                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Position</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredEmployees.length > 0 ? (
                        filteredEmployees.map((employee) => (
                          <TableRow key={employee.id}>
                            <TableCell className="font-medium">
                              <Link href={`/employees/${employee.id}`} className="hover:underline">
                                {employee.name}
                              </Link>
                            </TableCell>
                            <TableCell>{employee.position || "N/A"}</TableCell>
                            <TableCell>
                              <span
                                className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                                  employee.status === "Active"
                                    ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300"
                                    : "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
                                }`}
                              >
                                {employee.status}
                              </span>
                            </TableCell>
                            <TableCell className="text-right">
                              <Link
                                href={`/employees/${employee.id}`}
                                className="text-sm font-medium text-primary hover:underline"
                              >
                                View
                              </Link>
                            </TableCell>
                          </TableRow>
                        ))
                      ) : (
                        <TableRow>
                          <TableCell colSpan={4} className="h-24 text-center">
                            No employees found matching your search.
                          </TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </div>

                {filteredEmployees.length > 0 && (
                  <div className="text-sm text-muted-foreground mt-2">
                    Showing {filteredEmployees.length} of {employees.length} employees
                  </div>
                )}
              </>
            )}
          </CardContent>
        </Card>
      </main>

      {showWelcomePopup && <WelcomePopup onClose={handleCloseWelcomePopup} />}
    </div>
  )
}
