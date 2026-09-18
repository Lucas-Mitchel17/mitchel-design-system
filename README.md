# Mitchel Design System

Design system de marca da **Mitchel Sistemas** (a empresa) e do **Lucas Mitchel Dev**
(a pessoa), construído para servir também projetos de cliente como base white-label.

Fonte da verdade: **CSS custom properties**. Funciona em Astro, Laravel/Blade, Vue,
React ou HTML puro, e troca de tema em runtime, sem rebuild.

## A ideia em três linhas

```
PRIMITIVO    --ramp-brand-500: #43ea80                 "que cor é"      ← muda por marca
SEMÂNTICO    --action-primary: var(--ramp-brand-500)   "que papel tem"  ← igual em todos
COMPONENTE   --button-bg: var(--action-primary)        "quem usa"       ← por projeto
```

**Componente nunca consome primitivo, só semântico.** É a regra que sustenta tudo.

Teste de nomenclatura: se você precisa saber em que tela o token é usado para entender
o nome, o nome está na camada errada.

## Usando

```css
@import "mitchel-design-system/index.css";
```

```html
<html data-theme="mitchel-sistemas" data-mode="dark">
```

Com Tailwind 4:

```css
@import "tailwindcss";
@import "mitchel-design-system/index.css";
@import "mitchel-design-system/tailwind/preset.css";
```

## Estrutura

| Caminho | O que é |
|---|---|
| `tokens/primitives.css` | escalas sem marca: tipo, espaço, raio, movimento, camadas |
| `tokens/semantic.css` | **o contrato** — papéis, zero valores literais, claro e escuro |
| `tokens/themes/` | as rampas de cada marca |
| `base/reset.css` | reset moderno |
| `base/a11y.css` | foco visível, movimento reduzido, skip-link, alvo de toque |
| `tailwind/preset.css` | expõe os tokens ao Tailwind 4 |
| `assets/logo/` | as duas marcas em SVG, com `currentColor` |
| `docs/index.html` | documentação viva — lê os CSS de verdade, então não desatualiza |

## Documentação viva

```
python3 docs/build.py && xdg-open docs/index.html
```

`docs/build.py` gera duas versões do mesmo conteúdo a partir de uma fonte só:
`index.html` (lê os CSS reais do repo) e `_artifact.html` (CSS embutido, para publicar).

A página calcula o **contraste de cada par ao vivo**, nos dois temas e nos dois modos.
Foi ela que pegou o primeiro bug do sistema: `--text-disabled` sobre `--surface-disabled`
saiu em 2.45:1 — a mesma classe de erro que existia no site antigo.

## Um tema novo

Um cliente novo precisa entregar só isto:

```css
[data-theme="cliente"] {
  --ramp-neutral-0 … --ramp-neutral-950   /* 12 degraus */
  --ramp-brand-300 … --ramp-brand-800     /* 6 degraus  */
  --ramp-accent-500
  --font-display / --font-body / --font-mono
}
```

Se criar um tema exigir tocar em qualquer coisa fora de `tokens/themes/`, a camada
semântica tem vazamento e é isso que precisa ser corrigido — não o tema.

Requisito das rampas: `--ramp-brand-800` precisa ser escuro o bastante para servir de
texto sobre superfície clara (é o que o modo claro usa em `--text-highlight`).

## Decisões

Todas em [`docs/superpowers/specs/2026-09-18-mitchel-design-system-design.md`](docs/superpowers/specs/2026-09-18-mitchel-design-system-design.md),
com os motivos e o que foi rejeitado. Pendências abertas: [`docs/fontes.md`](docs/fontes.md).
