import type { HTMLAttributes, ReactNode } from 'react'
import { cn } from '@/lib/cn'

export interface EditorProps extends Omit<
  HTMLAttributes<HTMLDivElement>,
  'title'
> {
  /** Document title value. */
  title?: string
  /** When provided, the title renders as an editable field. */
  onTitleChange?: (value: string) => void
  /** Placeholder shown while the title is empty. */
  titlePlaceholder?: string
  /** Faint meta line, e.g. "Job description · draft". */
  meta?: ReactNode
}

/** The left-pane writing surface: serif title, faint meta, then the document body. */
export function Editor({
  title,
  onTitleChange,
  titlePlaceholder,
  meta,
  className,
  children,
  ...props
}: EditorProps) {
  const titleClasses = 'font-logo text-2xl font-bold tracking-tight text-ink'

  return (
    <div className={cn('h-full bg-transparent', className)} {...props}>
      {onTitleChange ? (
        <input
          type="text"
          value={title ?? ''}
          onChange={(event) => onTitleChange(event.target.value)}
          placeholder={titlePlaceholder}
          className={cn(
            'w-full bg-transparent outline-none placeholder:text-ink-faint/60',
            titleClasses,
          )}
        />
      ) : (
        title && <h2 className={titleClasses}>{title}</h2>
      )}
      {meta && (
        <p className="mt-2 font-sans text-meta text-ink-muted">{meta}</p>
      )}
      <div className="mt-6 font-sans text-body leading-relaxed text-ink">
        {children}
      </div>
    </div>
  )
}
