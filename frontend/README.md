# Pattern Specular — frontend

React 19 + TypeScript + Vite single-page app for the Pattern Specular manager and HR
surfaces, styled with Tailwind CSS v4 and the Rosewood design token architecture.
See [docs/adr](../docs/adr) for architectural records.

## Commands

```sh
npm install      # install dependencies
npm run dev      # start Vite dev server
npm run build    # type-check (tsc) and build for production
npm run lint     # eslint
npm run format   # prettier --write
npm test         # run Vitest suite (251 tests)
```

## Layout

- `src/components/ui/` — design-system components and TipTap writing surfaces
- `src/pages/` — surface screens (JD Studio, Feedback Checkpoint, Pattern Dashboard, Promotion Writeup, HR Trends & Growth Review)
- `src/router.tsx` — route table (TanStack Router)
- `src/styles/tokens/` — Rosewood design token definitions
- `src/index.css` — Tailwind CSS v4 entry and token bridge
