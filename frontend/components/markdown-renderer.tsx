"use client"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

interface MarkdownRendererProps {
  content: string
  className?: string
}

export function MarkdownRenderer({ content, className = "" }: MarkdownRendererProps) {
  return (
    <ReactMarkdown
      className={`prose prose-sm dark:prose-invert max-w-none break-words ${className}`}
      remarkPlugins={[remarkGfm]}
      components={{
        // Override default element styling
        p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
        ul: ({ children }) => <ul className="list-disc pl-4 mb-2">{children}</ul>,
        ol: ({ children }) => <ol className="list-decimal pl-4 mb-2">{children}</ol>,
        li: ({ children }) => <li className="mb-1">{children}</li>,
        h1: ({ children }) => <h1 className="text-lg font-bold mb-2 mt-3">{children}</h1>,
        h2: ({ children }) => <h2 className="text-base font-bold mb-2 mt-3">{children}</h2>,
        h3: ({ children }) => <h3 className="text-sm font-bold mb-1 mt-2">{children}</h3>,
        a: ({ href, children }) => (
          <a href={href} className="text-primary underline" target="_blank" rel="noopener noreferrer">
            {children}
          </a>
        ),
        blockquote: ({ children }) => (
          <blockquote className="border-l-2 border-muted-foreground pl-3 italic my-2">{children}</blockquote>
        ),
        code: ({ children }) => <code className="bg-muted px-1 py-0.5 rounded text-xs">{children}</code>,
        pre: ({ children }) => <pre className="bg-muted p-2 rounded-md overflow-x-auto my-2">{children}</pre>,
        table: ({ children }) => (
          <div className="overflow-x-auto my-2">
            <table className="min-w-full divide-y divide-border">{children}</table>
          </div>
        ),
        th: ({ children }) => <th className="px-2 py-1 bg-muted font-medium text-left">{children}</th>,
        td: ({ children }) => <td className="px-2 py-1 border-t border-border">{children}</td>,
      }}
    >
      {content}
    </ReactMarkdown>
  )
}
