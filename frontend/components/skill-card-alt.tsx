"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import type { Skill } from "@/types/employee"
import { Rocket, Plus, Minus } from "lucide-react"
import { cn } from "@/lib/utils"

interface SkillCardProps {
  skill: Skill
}

export function SkillCardAlt({ skill }: SkillCardProps) {
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

                  {quote.text && (
                    <div className="relative border-l-4 pl-4 py-1 border-muted-foreground/30 bg-background rounded-r">
                      <div className="absolute -left-6 top-0 text-muted-foreground/60">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="24"
                          height="24"
                          viewBox="0 0 24 24"
                          fill="currentColor"
                          className="opacity-20"
                        >
                          <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z" />
                        </svg>
                      </div>
                      <p className="text-sm italic">{quote.text}</p>
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
