"use client"

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { X } from "lucide-react"
import { usePopup } from "@/contexts/popup-context"

export function NextStepsPopup() {
  const { showNextStepsPopup, setShowNextStepsPopup } = usePopup()

  if (!showNextStepsPopup) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-md relative">
        <Button
          variant="ghost"
          size="icon"
          className="absolute right-2 top-2"
          onClick={() => setShowNextStepsPopup(false)}
          aria-label="Close"
        >
          <X className="h-4 w-4" />
        </Button>

        <CardHeader>
          <CardTitle>Next Steps</CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <p>
            After you've finished the call, ask the bot about the person's core competencies to update the visualization bellow. This is when the bot processes the transcripts. Write something like this:
          </p>
          <div className="bg-muted p-3 rounded-md">
            <p className="font-medium italic">
              "Please give the person a competency rating based on the feedback transcripts"
            </p>
          </div>
          <p>
            This will take some time to analyze the feedback and transform it into a structured format. You can refresh
            the page to see the changes once it has been processed.
          </p>
        </CardContent>

        <CardFooter>
          <Button onClick={() => setShowNextStepsPopup(false)} className="w-full">
            Got it
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
