import { cn } from "@/lib/utils"

interface SatisfactionBarProps {
  value: number
  maxValue?: number
  className?: string
}

export function SatisfactionBar({ value, maxValue = 10, className }: SatisfactionBarProps) {
  // Ensure value is within bounds
  const normalizedValue = Math.max(0, Math.min(value, maxValue))

  // Calculate percentage for positioning
  const percentage = (normalizedValue / maxValue) * 100

  // Generate gradient colors based on the value
  // Red (low) to Green (high)
  const getBarColor = () => {
    // Create a gradient from red to yellow to green
    return `linear-gradient(to right, 
      rgb(239, 68, 68), 
      rgb(239, 68, 68) 20%, 
      rgb(234, 179, 8) 50%,
      rgb(34, 197, 94) 80%,
      rgb(34, 197, 94) 100%)`
  }

  return (
    <div className={cn("w-full h-6 bg-gray-200 rounded-full overflow-hidden", className)}>
      <div
        className="h-full rounded-full transition-all duration-500 ease-in-out"
        style={{
          width: `${percentage}%`,
          background: getBarColor(),
        }}
      />
      <div
        className="relative h-full w-0.5 bg-white dark:bg-gray-800 -mt-6 pointer-events-none"
        style={{
          marginLeft: `${percentage}%`,
          boxShadow: "0 0 4px rgba(0, 0, 0, 0.3)",
        }}
      />
    </div>
  )
}
