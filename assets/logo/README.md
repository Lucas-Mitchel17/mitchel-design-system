# Logos

## Lucas Mitchel Dev

Vetorizada a partir do estudo que o Lucas gerou online (`< LM >` com barra
diagonal). A geometria foi **regularizada**, não copiada pixel a pixel: os dois
chevrons tinham ~4px de desvio entre si e as arestas não fechavam — imagem
gerada por IA nunca sai simétrica.

| Arquivo | Uso | Lê bem até |
|---|---|---|
| `lucas-mitchel-dev-mark.svg` | marca completa, `currentColor` | ~40px |
| `lucas-mitchel-dev-mark-compact.svg` | favicon, ícone de app, navbar densa | **16px** |
| `lucas-mitchel-dev-mark-gradient.svg` | hero, capa, imagem de OG | grande |

### Por que existe uma compacta

A marca completa tem seis formas: dois chevrons, L, M, a barra e a cauda.
Abaixo de ~40px os chevrons (que são finos) somem e o resto vira borrão.
A compacta descarta chevrons e cauda e mantém L + M + barra — o que sobrevive.

Isso é **logo responsiva**, prática normal: a marca completa acima de 40px,
a compacta abaixo. Não são duas marcas, são dois recortes da mesma.

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
