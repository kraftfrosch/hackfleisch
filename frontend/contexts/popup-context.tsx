"use client"

import type React from "react"
import { createContext, useState, useContext, useEffect, useCallback } from "react"

interface PopupContextType {
  showDemoPopup: boolean
  showNextStepsPopup: boolean
  setShowDemoPopup: (show: boolean) => void
  setShowNextStepsPopup: (show: boolean) => void
  employeeId: string | null
  employeeName: string | null
  setEmployeeInfo: (id: string, name: string) => void
  handleDemoSubmit: (firstName: string, phoneNumber: string) => void
}

const PopupContext = createContext<PopupContextType | undefined>(undefined)

// Import chatEvents outside of the component to avoid circular dependencies
let chatEvents: any = null

// This will be called only on the client side
if (typeof window !== "undefined") {
  // Dynamic import to avoid circular dependencies
  import("@/components/employee-chat").then((module) => {
    chatEvents = module.chatEvents
  })
}

export function PopupProvider({ children }: { children: React.ReactNode }) {
  const [showDemoPopup, setShowDemoPopup] = useState(false)
  const [showNextStepsPopup, setShowNextStepsPopup] = useState(false)
  const [employeeId, setEmployeeId] = useState<string | null>(null)
  const [employeeName, setEmployeeName] = useState<string | null>(null)
  const [nextStepsTimer, setNextStepsTimer] = useState<NodeJS.Timeout | null>(null)

  // Clear the timer when component unmounts
  useEffect(() => {
    return () => {
      if (nextStepsTimer) {
        clearTimeout(nextStepsTimer)
      }
    }
  }, [nextStepsTimer])

  // Use useCallback to memoize these functions
  const setEmployeeInfo = useCallback((id: string, name: string) => {
    setEmployeeId(id)
    setEmployeeName(name)
  }, [])

  const handleDemoSubmit = useCallback(
    (firstName: string, phoneNumber: string) => {
      if (!employeeId || !employeeName || !chatEvents) {
        console.error("Missing required data for demo submission", { employeeId, employeeName, chatEvents })
        return
      }

      // Create the display message for the chat window
      const displayMessage = `Please call ${firstName} at ${phoneNumber} to collect feedback about ${employeeName} based on their employee context.`

      // Create the API message with the base prompt
      const apiMessage = `I am interacting with you through a chat window in ${employeeName}'s profile. Please only help with analyzing and collecting feedback on him or her. Please call ${firstName} at ${phoneNumber} to collect feedback about ${employeeName}'s skills and performance.`

      // Add the message to the chat
      chatEvents.addMessage(employeeId, displayMessage, apiMessage)

      // Close the demo popup
      setShowDemoPopup(false)

      // Clear any existing timer
      if (nextStepsTimer) {
        clearTimeout(nextStepsTimer)
      }

      // Set a timer to show the next steps popup after 15 seconds
      const timer = setTimeout(() => {
        console.log("Showing next steps popup")
        setShowNextStepsPopup(true)
      }, 15000)

      setNextStepsTimer(timer)
    },
    [employeeId, employeeName, nextStepsTimer],
  )

  return (
    <PopupContext.Provider
      value={{
        showDemoPopup,
        showNextStepsPopup,
        setShowDemoPopup,
        setShowNextStepsPopup,
        employeeId,
        employeeName,
        setEmployeeInfo,
        handleDemoSubmit,
      }}
    >
      {children}
    </PopupContext.Provider>
  )
}

export function usePopup() {
  const context = useContext(PopupContext)
  if (context === undefined) {
    throw new Error("usePopup must be used within a PopupProvider")
  }
  return context
}
