import { useState, useRef, useEffect, type HTMLAttributes } from 'react'
import { cn } from '@/lib/cn'
import psLogo from '@/assets/ps-logo.svg'
import { Button } from '@/components/ui/button'
import { Chip } from '@/components/ui/chip'
import type { AuthUser } from '@/lib/auth-contract'

export interface TopBarProps extends HTMLAttributes<HTMLElement> {
  /** Surface name shown after "Pattern Specular ·". @default "JD Studio" */
  surface?: string
  /** Context chips (subject, role/tier, scope). */
  chips?: string[]
  /** Avatar initials. @default "DK" */
  initials?: string
  /** Current signed-in user object for profile card. */
  user?: AuthUser | null
  /** Primary action label (renders a red button). Omit for none. */
  action?: string | null
  onAction?: () => void
  /** When set, the avatar becomes a log-out control. */
  onLogout?: () => void
}

/** Persistent app top bar: wordmark + breadcrumb left, context chips + avatar (+ optional action) right. */
export function TopBar({
  surface = 'JD Studio',
  chips = [],
  initials = 'DK',
  user = null,
  action = null,
  onAction,
  onLogout,
  className,
  ...props
}: TopBarProps) {
  const [isOpen, setIsOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen])

  const avatarClass =
    'flex size-9 items-center justify-center rounded-full bg-chip-track font-sans text-label font-semibold text-ink-muted'

  return (
    <header
      className={cn(
        'relative flex h-16 items-center justify-between border-b border-border bg-surface px-6',
        className,
      )}
      {...props}
    >
      <div className="flex items-center gap-3">
        <img src={psLogo} alt="Pattern Specular" className="h-6 w-auto" />
        <span className="font-logo text-[20px] font-black tracking-tight text-ink select-none">
          Pattern Specular
        </span>
        <span className="h-4 w-px bg-border" aria-hidden="true" />
        <span className="font-sans text-label font-medium text-ink-muted">
          {surface}
        </span>
      </div>
      <div className="flex items-center gap-3">
        {chips.map((chip, index) => (
          <Chip key={index}>{chip}</Chip>
        ))}
        {action && (
          <Button variant="primary" size="md" onClick={onAction}>
            {action}
          </Button>
        )}
        <div className="relative" ref={menuRef}>
          <button
            type="button"
            onClick={() => setIsOpen((prev) => !prev)}
            aria-expanded={isOpen}
            aria-haspopup="true"
            title="Profile & Settings"
            className={cn(avatarClass, 'transition-colors hover:bg-border cursor-pointer focus:outline-none focus:ring-2 focus:ring-ink')}
          >
            {user?.initials || initials}
          </button>

          {isOpen && (
            <div className="absolute right-0 top-12 z-50 w-64 rounded-card border border-border bg-surface p-4 shadow-ring-card animate-in fade-in slide-in-from-top-1 duration-150">
              <div className="flex items-center gap-3 pb-3 border-b border-border">
                <span className={cn(avatarClass, 'bg-ink text-white')}>
                  {user?.initials || initials}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="truncate font-sans text-body-sm font-semibold text-ink">
                    {user?.legalName || 'User'}
                  </p>
                  <p className="truncate font-sans text-meta text-ink-muted">
                    {user?.email || ''}
                  </p>
                </div>
              </div>
              <div className="py-2.5 flex items-center justify-between font-sans text-meta text-ink-muted">
                <span>Role</span>
                <span className="rounded-pill bg-chip-track px-2 py-0.5 font-semibold capitalize text-ink">
                  {user?.role || 'manager'}
                </span>
              </div>
              {onLogout && (
                <button
                  type="button"
                  onClick={() => {
                    setIsOpen(false)
                    onLogout()
                  }}
                  className="mt-1 w-full rounded-md bg-red-primary/10 py-2 text-center font-sans text-meta font-semibold text-red-primary transition-colors hover:bg-red-primary hover:text-white cursor-pointer"
                >
                  Sign out
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
