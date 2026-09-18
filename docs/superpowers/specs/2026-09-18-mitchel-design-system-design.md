# Mitchel Design System — desenho das fundações

**Data:** 2026-09-18
**Autor:** Lucas Mitchel (com Claude)
**Status:** desenho aprovado, aguardando plano de implementação

---

## 1. Objetivo

Criar um design system de marca, próprio, que sirva:

- **mitchelsistemas.com** — site institucional da empresa, já existente (Astro 2 + Tailwind 3)
- **lucasmitchel.dev** — marca pessoal, site ainda inexistente (só o domínio)
- **projetos de cliente** — como base white-label, um tema por cliente

Objetivo secundário e igualmente importante: Lucas nunca construiu um design system.
O processo é material de estudo, não só entrega. Decisões devem vir acompanhadas do
mecanismo que as justifica.

## 2. Decisões tomadas

| # | Decisão | Escolha | Motivo |
|---|---|---|---|
| D1 | Identidade | Sistematizar a que existe | Aprender o mecanismo com material real; trocar a paleta depois fica barato — é justamente o ponto do sistema |
| D2 | Relação entre marcas | Marcas irmãs (arquitetura endossada) | Mitchel Sistemas é a empresa que assina; Lucas Mitchel Dev é a pessoa por trás. Mesma família, peles diferentes |
| D3 | Alcance | Projetos próprios **e** de cliente | Exige nomenclatura 100% agnóstica de marca desde a primeira linha |
| D4 | Stacks-alvo | Astro (última) + Tailwind 4 para estáticos; Vue + PrimeVue no futuro | PrimeVue 4 usa o mesmo modelo de três camadas — plugar depois é mapeamento, não reescrita |
| D5 | Fonte da verdade | CSS custom properties | Funciona em qualquer stack, troca de tema em runtime sem rebuild, e é o caminho oficial do Tailwind 4 (CSS-first) |
| D6 | Escala de superfícies | Numerada (`--surface-1..n`) | Escala melhor quando aparecer o quarto nível; é o que o PrimeVue usa |
| D7 | Orbitron | Só display: logo, H1, números | Display geométrica de letra quadrada: forte em pouca quantidade, cansativa e pouco legível em H2/H3 longos |
| D8 | Escala tipográfica | Modular, razão 1.25, base 16px | Os tamanhos que Lucas já escolheu no olho caem quase em cima dessa progressão |

### Rejeitado

- **Tokens em JSON + Style Dictionary.** É o caminho de empresa grande e escala melhor pro
  white-label, mas custa um build step e uma pilha de conceitos antes de os primeiros estarem
  entendidos. A nomenclatura definida aqui é compatível — migrar depois é mecânico.
- **Copiar e colar entre projetos.** Zero infra, divergência garantida.
- **Uma marca só / marcas separadas.** Ver D2.

## 3. Arquitetura de tokens

Três camadas. A regra que sustenta tudo: **componente nunca consome primitivo, só semântico.**

```
PRIMITIVO    --green-500: #43ea80                      "que cor é"      ← muda por marca
SEMÂNTICO    --action-primary: var(--green-500)        "que papel tem"  ← igual em todos
COMPONENTE   --cta-section-surface: var(--surface-2)   "quem usa"       ← por projeto
```

A camada semântica é a que viaja entre projetos. É o contrato do sistema.

**Teste de nomenclatura:** se você precisa saber em que tela o token é usado pra entender o
nome, o nome está na camada errada.

### 3.1 Cor — camada semântica

Derivada do inventário de papéis reais do site atual.

| Token | Papel | Valor no tema Mitchel Sistemas |
|---|---|---|
| `--surface-1` | superfície base da página | `#080c1c` |
| `--surface-2` | superfície mais funda (seções, CTA) | `#050813` |
| `--text-primary` | texto sobre superfície | `#ffffff` |
| `--text-highlight` | ênfase em texto | `#43ea80` |
| `--action-primary` | fundo da ação principal | `#43ea80` |
| `--text-on-action-primary` | texto sobre a ação principal | `#080c1c` |
| `--surface-disabled` | fundo de elemento desabilitado | neutro, na implementação |
| `--text-disabled` | texto de elemento desabilitado | neutro, na implementação |
| `--border-disabled` | contorno de elemento desabilitado | neutro, na implementação |
| `--border-default` | contorno padrão | `#43ea80` |
| `--icon-default` | ícone | `#43ea80` |
| `--divider` | separador entre blocos | `#38f8d4` |
| `--scrim` | escurece mídia para dar legibilidade | `#080c1cad` |
| `--focus-ring` | indicador de foco de teclado | derivado do verde de marca |
| `--glow-action` | feedback de hover na ação | `#43ea80bd` |
| `--danger-*` | erro | ver pendência abaixo |
| `--success-*` | sucesso | ver pendência abaixo |
| `--warning-*` | atenção | ver pendência abaixo |

Os três tokens de `disabled` saem de uma escala neutra a ser criada junto com os primitivos —
não são decisão de marca, são consequência de ter uma escala de cinzas. O `--focus-ring` deriva
do verde de marca, com contraste conferido contra `--surface-1` e `--surface-2`.

**Pendência de marca:** o verde é ao mesmo tempo a cor da marca e a cor convencional de
sucesso. Sucesso e ação primária vão colidir na mesma tela. Resolver ao definir os tokens de
feedback — provavelmente deslocando o sucesso para outro matiz ou diferenciando por forma/ícone.

**Regras:**

- Todo token de fundo tem par de conteúdo legível. Contraste por construção, não por conferência.
- `surface` é tela/container. `action` (ou `interactive`) é coisa clicável. Substantivos não se
  misturam, senão "quais são minhas superfícies?" deixa de ter resposta coerente.
- Um papel, um token — mesmo que dois tokens apontem hoje para o mesmo hex.
- `inactive` (aba não selecionada) e `disabled` (não aceita interação) são estados distintos.

### 3.2 Tipografia

```
--font-display   títulos de display, logo, números grandes   → Orbitron
--font-body      texto corrido, UI, H2/H3                    → Play
--font-mono      código, dados                               → escolher na implementação
```

Escala modular, base 16px, razão 1.25: **16 · 20 · 25 · 31 · 39 · 49 · 61**.
Fluida via `clamp()` — elimina os saltos por breakpoint.

Tokens adicionais: `--leading-tight` (~1.1, títulos) · `--leading-normal` (~1.6, corrido) ·
`--tracking-tight` (negativo, títulos grandes) · `--measure` (45–75ch).

**Restrição conhecida:** Play só é importada nos pesos 400 e 700. Com H2/H3 passando para
`--font-body`, a hierarquia de peso fica em degraus grandes. Revisitar — a Khula, hoje baixada
e nunca usada, pode ter sido essa intenção.

### 3.3 Espaçamento

Base 4px, escala numérica `--space-1` (4px) … `--space-24` (96px). O Tailwind já usa essa base.

Acima dela, tokens semânticos de layout — onde mora o ritmo da página e a diferença de
densidade entre as duas marcas:

- `--section-padding-block`
- `--container-gutter`
- `--stack-gap`
- `--container-max` (hoje inexistente)

### 3.4 Raio, elevação, movimento

```
--radius-sm 4px · --radius-md 8px · --radius-lg 16px · --radius-full 9999px
--elevation-1/2/3          sombras de profundidade
--glow-action              feedback de interação — NÃO é elevação, papel diferente
--duration-fast 150ms · --duration-base 250ms · --duration-slow 400ms
--ease-out · --ease-in-out
```

### 3.5 Acessibilidade — regras do sistema, não do componente

- **`:focus-visible` obrigatório** em tudo que é interativo, com `--focus-ring`. Hoje o projeto
  não tem nenhum; o único `focus:` existente é um `focus:outline-none` que piora a situação.
- **`prefers-reduced-motion`** respeitado globalmente. O site anima fade, blur e slide em quase
  tudo e não trata isso hoje.
- Contraste mínimo garantido pelos pares fundo/conteúdo.
- Nada de `transition-all` — declarar as propriedades animadas.

## 4. Estrutura do repositório

```
mitchel-design-system/
├── tokens/
│   ├── primitives.css               escala crua
│   ├── semantic.css                 papéis (o contrato)
│   └── themes/
│       ├── mitchel-sistemas.css
│       └── lucas-mitchel-dev.css
├── base/
│   ├── reset.css                    reset moderno
│   └── a11y.css                     focus-visible, reduced-motion
├── tailwind/preset.css              expõe os tokens pro Tailwind 4
└── docs/                            página viva do sistema
```

Tema aplicado por `[data-theme="..."]` no `<html>`. Por serem custom properties, a troca é em
runtime, sem rebuild — é isso que permite entregar tema de cliente sem forkar o sistema.

## 5. Achados no site atual

Backlog levantado na auditoria. Alguns são bugs, não questões de estilo.

**Bugs**

1. `global.css` aplica `user-select: none` a `p`, `span`, `h1` e a lista inteira do reset —
   ninguém consegue copiar texto do site.
2. `is-error` e `is-success` herdam `hover:bg-blue-400` e não sobrescrevem: hover azul, fora
   da paleta.
3. `is-inactive`: `text-gray-800` sobre `bg-gray-700`, ilegível.
4. `is-link` / `is-card`: `text-black` em página de fundo escuro.
5. `BaseLink` só renderiza se `href && variation` — sem `variation`, o link some silenciosamente.
6. H1 e H2 são ambos `text-4xl` no mobile: hierarquia nula em telas pequenas.
7. `astro.config.mjs` com `site: 'https://meusite.com'` — o `sitemap-index.xml` está sendo
   gerado com URLs erradas.
8. `og:image` aponta para `https://url/share-thumb`.
9. Caminhos de favicon e manifest usando `../assets/...` e `src/assets/...` no `<head>`.

**Dívida de sistema**

10. Cor definida em três lugares: `tailwind.config.cjs`, `variables.css` e hex soltos.
11. `DependenciesLayout` importa `main.css` e também os três arquivos que ele já importa —
    tudo entra duas vezes.
12. Duas definições concorrentes de `.container` (a do projeto, sem `max-width`, e a do Tailwind).
13. Khula baixada do Google Fonts e nunca usada.
14. Valores mágicos: `rounded-[15px]`, `min-h-[130px]`, `min-w-[140px]`, `min-w-[172px]`,
    `box-shadow: 6px 4px 4px`.
15. `tracking-wider` aplicado a texto corrido (`.is-paragraph` e parágrafo do hero).
16. `max-w-7xl` (1280px) como largura de leitura no hero — cerca do dobro do confortável.
17. `package.json` com `name: "shaky-pulsar"`.
18. Astro 2 + Tailwind 3 + `@astrojs/image` (descontinuado).

## 6. Escopo

**Dentro:** os tokens (primitivo, semântico, temas), o reset, as regras de acessibilidade, o
preset do Tailwind 4, a página de documentação viva e os dois temas.

**Fora, por enquanto:** biblioteca de componentes versionada, Style Dictionary, preset de
PrimeVue, publicação em registry npm, modo claro.

## 7. Ordem de trabalho

1. **DS + tema Mitchel Sistemas** — tokens, reset, a11y, preset, página de docs.
2. **Tema Lucas Mitchel Dev** — só o arquivo de tema. É o teste do sistema: se exigir mexer em
   qualquer coisa fora de `themes/`, a camada semântica tem vazamento.
3. **Migrar o mitchelsistemas** — Astro 5 + Tailwind 4 consumindo o DS. Cada valor hardcoded
   que não encontrar token é um buraco no sistema, e aqui eles aparecem todos de uma vez.
4. **Construir o lucasmitchel.dev** sobre o sistema já testado.

O passo 2 exige uma conversa de marca própria: o que a marca pessoal comunica que a da empresa
não comunica. Não é derivável do código.

## 8. Critérios de sucesso

- Trocar a paleta inteira de uma marca = editar um arquivo de tema, nada mais.
- Nenhum componente referencia primitivo ou hex literal.
- Nenhum nome de token semântico menciona cor, marca ou tela.
- Criar o segundo tema não exige tocar em `semantic.css`.
- Todo elemento interativo tem foco visível; o site respeita `prefers-reduced-motion`.
- Lucas consegue explicar, sem consultar, por que cada camada existe.
