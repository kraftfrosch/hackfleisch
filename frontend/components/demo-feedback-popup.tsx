"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { X } from "lucide-react"
import { usePopup } from "@/contexts/popup-context"

interface DemoFeedbackPopupProps {
  employeeId: string
  employeeName: string
}

export function DemoFeedbackPopup({ employeeId, employeeName }: DemoFeedbackPopupProps) {
  const [phoneNumber, setPhoneNumber] = useState("")
  const [firstName, setFirstName] = useState("")
  const { showDemoPopup, setShowDemoPopup, handleDemoSubmit, setEmployeeInfo } = usePopup()

  // Set employee info when component mounts or props change
  useEffect(() => {
    setEmployeeInfo(employeeId, employeeName)
  }, [employeeId, employeeName, setEmployeeInfo])

  if (!showDemoPopup) return null

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!phoneNumber.trim() || !firstName.trim()) return

    handleDemoSubmit(firstName, phoneNumber)
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-md relative">
        <Button
          variant="ghost"
          size="icon"
          className="absolute right-2 top-2"
          onClick={() => setShowDemoPopup(false)}
          aria-label="Close"
        >
          <X className="h-4 w-4" />
        </Button>

        <CardHeader>
          <CardTitle>For Demo Purposes</CardTitle>
          <CardDescription>
            To experience the feedback collection feature, enter your phone number below. You'll receive a call to
            provide feedback on this team member, and you can then see how it's integrated into their skill matrix.
            <strong>
              {" "}
              The longer you stay on the line, the better the output becomes. To get anything meaningful, stay on the
              line at least for 30 seconds.
            </strong>
          </CardDescription>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="firstName">First Name</Label>
              <Input
                id="firstName"
                placeholder="Enter your first name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="phoneNumber">Phone Number</Label>
              <Input
                id="phoneNumber"
                type="tel"
                placeholder="Enter your phone number"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
                required
              />
            </div>
          </CardContent>

          <CardFooter>
            <Button type="submit" className="w-full">
              Submit
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
