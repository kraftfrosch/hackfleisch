"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import type { ChatMessage } from "@/types/employee"
import { Send, ChevronUp, ChevronDown } from "lucide-react"
import { v4 as uuidv4 } from "uuid"
import { cn } from "@/lib/utils"
import { useToast } from "@/components/ui/use-toast"
import { MarkdownRenderer } from "./markdown-renderer"

interface EmployeeChatProps {
  employeeId: string
  employeeName: string
}

// Create a global event emitter for chat messages
export const chatEvents = {
  listeners: new Map<string, (displayMessage: string, apiMessage?: string) => void>(),

  // Add a message to a specific employee's chat
  addMessage: (employeeId: string, displayMessage: string, apiMessage?: string) => {
    const listener = chatEvents.listeners.get(employeeId)
    if (listener) {
      listener(displayMessage, apiMessage)
    }
  },

  // Register a listener for a specific employee
  registerListener: (employeeId: string, callback: (displayMessage: string, apiMessage?: string) => void) => {
    chatEvents.listeners.set(employeeId, callback)
    return () => {
      chatEvents.listeners.delete(employeeId)
    }
  },
}

export function EmployeeChat({ employeeId, employeeName }: EmployeeChatProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      content: `Ask me anything about ${employeeName}'s skills and performance.`,
      sender: "assistant",
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isExpanded, setIsExpanded] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const chatContentRef = useRef<HTMLDivElement>(null)
  const { toast } = useToast()

  // Generate and keep chat ID per session
  const [chatId] = useState(() => `employee-${employeeId}-${uuidv4().slice(0, 8)}`)

  // Scroll to bottom of chat container when messages change
  useEffect(() => {
    if (isExpanded && messagesEndRef.current && chatContentRef.current) {
      // Use scrollIntoView with behavior: "auto" to avoid smooth scrolling which can cause page scrolling
      messagesEndRef.current.scrollIntoView({ behavior: "auto", block: "end" })
    }
  }, [messages, isExpanded])

  // Update the useEffect hook that registers the listener
  useEffect(() => {
    const unregister = chatEvents.registerListener(employeeId, (displayMessage, apiMessage) => {
      addUserMessage(displayMessage, apiMessage)
    })

    return unregister
  }, [employeeId])

  // Update the addUserMessage function to handle separate API messages
  const addUserMessage = async (content: string, apiMessage?: string) => {
    const userMessage: ChatMessage = {
      id: uuidv4(),
      content,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])

    if (!isExpanded) {
      setIsExpanded(true)
    }

    // If apiMessage is provided, use it; otherwise, create one with the base prompt
    const messageToSend =
      apiMessage ||
      `I am interacting with you through a chat window in ${employeeName}'s profile. Please only collect, process and explain feedback about this person. ${content}`

    await processMessage(messageToSend)
  }

  // Update the processMessage function to use the provided message
  const processMessage = async (content: string) => {
    setIsLoading(true)

    try {
      // Call the actual API endpoint
      const response = await fetch("https://chatbot-cdtmhack.ngrok.app/run-agent", {
        method: "POST",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          input: content,
          chat_id: chatId,
        }),
      })

      if (!response.ok) {
        throw new Error(`API responded with status: ${response.status}`)
      }

      const data = await response.json()

      const assistantMessage: ChatMessage = {
        id: uuidv4(),
        content: data.response,
        sender: "assistant",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])

      // Optional: Log the full history from the response if needed
      console.log("Chat history:", data.history)
    } catch (error) {
      console.error("Error calling chat API:", error)

      // Add fallback response in case of API failure
      const errorMessage: ChatMessage = {
        id: uuidv4(),
        content: "I'm having trouble connecting to the server right now. Please try again in a moment.",
        sender: "assistant",
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, errorMessage])

      toast({
        title: "Error",
        description: "Failed to get a response from the chat service.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const displayMessage = inputValue
    const apiMessage = `I am interacting with you through a chat window in ${employeeName}'s profile. Please only collect, process and explain feedback about this person. ${inputValue}`

    setInputValue("")
    await addUserMessage(displayMessage, apiMessage)
  }

  return (
    <Card className="w-full">
      <CardHeader className="pb-2 flex flex-row items-center justify-between">
        <CardTitle>Chat about {employeeName}</CardTitle>
        <Button variant="ghost" size="sm" onClick={() => setIsExpanded(!isExpanded)} className="h-8 w-8 p-0">
          {isExpanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </Button>
      </CardHeader>

      {isExpanded && (
        <CardContent
          className="max-h-[400px] overflow-y-auto"
          ref={chatContentRef}
          style={{ scrollBehavior: "auto" }} // Prevent smooth scrolling
        >
          <div className="space-y-4">
            {messages.map((message) => (
              <div key={message.id} className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-2 ${
                    message.sender === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
                  }`}
                >
                  {message.sender === "assistant" ? (
                    <MarkdownRenderer content={message.content} />
                  ) : (
                    <p className="text-sm">{message.content}</p>
                  )}
                  <p className="text-xs opacity-70 mt-1">
                    {message.timestamp.toLocaleTimeString([], {
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </CardContent>
      )}

      <CardFooter className={cn("pt-2", isExpanded ? "" : "pt-0")}>
        <form
          onSubmit={(e) => {
            e.preventDefault()
            handleSendMessage()
          }}
          className="flex w-full items-center space-x-2"
        >
          <Input
            placeholder="Type your message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading}
          />
          <Button type="submit" size="icon" disabled={isLoading || !inputValue.trim()}>
            {isLoading ? (
              <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </form>
      </CardFooter>
    </Card>
  )
}
