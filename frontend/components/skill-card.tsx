"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { Skill } from "@/types/employee"
import { Rocket, Plus, Minus } from "lucide-react"
import { cn } from "@/lib/utils"

interface SkillCardProps {
  skill: Skill
}

export function SkillCard({ skill }: SkillCardProps) {
  const maxLevel = 4

  return (
    <Card className="mb-4 h-full">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg">{skill.skill_name}</CardTitle>
        <CardDescription>{skill.level_description}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="mb-4">
          <div className="flex items-center justify-between mb-1">
            <span className="text-sm font-medium">
              Skill Level: {skill.employee_level}/{maxLevel}
            </span>
          </div>
          <div className="flex h-4 rounded-full overflow-hidden bg-muted">
            {Array.from({ length: maxLevel }).map((_, index) => (
              <div
                key={index}
                className={cn(
                  "h-full transition-all",
                  index < skill.employee_level ? "bg-primary" : "bg-transparent border-r border-background",
                )}
                style={{ width: `${100 / maxLevel}%` }}
              />
            ))}
          </div>
        </div>

        <div className="text-sm text-muted-foreground mb-4">
          <h4 className="text-sm font-medium mb-1">Summary:</h4>
          <p>{skill.reasoning}</p>
        </div>

        <div className="space-y-4">
          <h4 className="text-sm font-medium">Feedback Evidence:</h4>
          {skill.feedback_quotes.map((quote, index) => (
            <div key={index} className="p-3 rounded-md bg-muted/50">
              <div className="flex items-start gap-2">
                {quote.type === "positive" && <Plus className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />}
                {quote.type === "negative" && <Minus className="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />}
                {quote.type === "constructive" && <Rocket className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />}
                <div className="space-y-2 w-full">
                  {quote.justification && <p className="text-sm">{quote.justification}</p>}

                  {quote.direct_quote && (
                    <div className="relative pl-8 pr-2 py-2 border border-muted-foreground/20 rounded bg-background">
                      <div className="absolute left-2 top-2 text-muted-foreground/40">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="20"
                          height="20"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          className="opacity-70"
                        >
                          <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z" />
                          <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z" />
                        </svg>
                      </div>
                      <p className="text-sm italic">{quote.direct_quote}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
