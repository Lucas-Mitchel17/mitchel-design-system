# Logos

## Lucas Mitchel Dev

Vetorizada a partir do estudo que o Lucas gerou online (`< LM >` com barra
diagonal). A geometria foi **regularizada**, não copiada pixel a pixel: os dois
chevrons tinham ~4px de desvio entre si e as arestas não fechavam — imagem
gerada por IA nunca sai simétrica.

| Arquivo | Uso | Faixa |
|---|---|---|
| `lucas-mitchel-dev-mark.svg` | marca completa, `currentColor` | acima de 40px |
| `lucas-mitchel-dev-mark-lockup.svg` | **assinatura: navbar, rodapé** | 24 – 40px |
| `lucas-mitchel-dev-mark-compact.svg` | favicon, ícone de app | abaixo de 24px |
| `lucas-mitchel-dev-mark-gradient.svg` | hero, capa, imagem de OG | grande |

### Peso óptico

A marca completa tem seis formas: dois chevrons, L, M, a barra e a cauda.
Reduzida, ela não some por igual — **os chevrons somem primeiro**, porque são
os traços mais finos.

Por isso as três variantes não são recortes arbitrários, são pesos ópticos:

- **completa** — tudo, no traço do desenho original.
- **assinatura** — chevrons ~45% mais grossos (senão desaparecem nessa faixa)
  e sem a cauda, que desequilibra a marca ao lado do nome.
- **compacta** — sem chevrons. Abaixo de 24px nem engrossados eles sobrevivem;
  resta L + M + barra, que é o que ainda lê a 16px.

Fonte tem peso óptico e ninguém estranha. Logo tem pelo mesmo motivo.

## Mitchel Sistemas

`mitchel-sistemas-mark.svg` — círculo com linhas de sinal, reconstruído em
vetor a partir do PNG do Canva.

## currentColor

Nenhuma tem cor embutida: todas herdam `currentColor`. Defina `color` no pai —
normalmente `var(--icon-default)` ou `var(--text-primary)`. É isso que faz a
logo acompanhar a troca de tema, e é o que o PNG antigo não conseguia.

A versão de gradiente lê os tokens do tema quando o SVG está inline no HTML,
e cai nos hex de fallback quando é carregada como `<img>`.

## Assinatura (marca + nome)

O nome **não** está dentro do SVG, de propósito: texto em SVG depende da fonte
carregada, não é selecionável e não é lido direito por leitor de tela. A
assinatura se monta em HTML — marca ao lado do nome em `--font-display`.

⚠️ Para impressão ou fundo de terceiros, o nome precisaria estar vetorizado em
curvas. Fica como pendência; não bloqueia uso em web.
