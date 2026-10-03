import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Badge } from './badge'

describe('Badge', () => {
  it('renders its children', () => {
    render(<Badge>3</Badge>)
    expect(screen.getByText('3')).toBeInTheDocument()
  })

  it('defaults to the red tone', () => {
    render(<Badge>1</Badge>)
    expect(screen.getByText('1')).toHaveClass('bg-red-primary')
  })

  it('applies the requested tone', () => {
    render(<Badge tone="green">ok</Badge>)
    expect(screen.getByText('ok')).toHaveClass('bg-green-positive')
  })

  it('applies the amber tone', () => {
    render(<Badge tone="amber">warning</Badge>)
    expect(screen.getByText('warning')).toHaveClass('bg-amber-secondary')
  })

  it('applies the region tone with font-mono', () => {
    render(<Badge tone="region">IN</Badge>)
    const badge = screen.getByText('IN')
    expect(badge).toHaveClass('bg-ink')
    expect(badge).toHaveClass('font-mono')
  })

  it('merges a caller className with the variant classes', () => {
    render(<Badge className="custom-class">2</Badge>)
    const badge = screen.getByText('2')
    expect(badge).toHaveClass('custom-class')
    expect(badge).toHaveClass('bg-red-primary')
  })
})
