import { ModeToggle } from "@/components/mode-toggle"

export function Header() {
  return (
    <div className="border-b">
      <div className="flex h-16 items-center px-4">
        <div className="flex items-center font-semibold text-lg">
          <span>PEOPLEWORKS</span>
        </div>
        <div className="ml-auto flex items-center">
          <ModeToggle />
        </div>
      </div>
    </div>
  )
}
