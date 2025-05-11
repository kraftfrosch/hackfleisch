"use client"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { X } from "lucide-react"

interface WelcomePopupProps {
  onClose: () => void
}

export function WelcomePopup({ onClose }: WelcomePopupProps) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-md relative">
        <Button variant="ghost" size="icon" className="absolute right-2 top-2" onClick={onClose} aria-label="Close">
          <X className="h-4 w-4" />
        </Button>

        <CardContent className="pt-6 pb-4">
          <h3 className="text-xl font-bold mb-4">Hi there Demo-er</h3>
          <p>
            Not all profiles are populated with data. If you want to try to give feedback to somebody with an empty profile by talking to our Voice Agent, feel free to check out{" "}
            <strong>Henri's</strong> profile.
          </p>
          <p className="mb-3">
            If you want to see a profile page where feedback has already been given and processed, checkout <strong>Vishwa's</strong> and <strong>Johannes's</strong> page.
          </p>
        </CardContent>

        <CardFooter>
          <Button onClick={onClose} className="w-full">
            Got it
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
