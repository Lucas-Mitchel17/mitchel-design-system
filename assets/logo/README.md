# Logos

Ambas as marcas são **monoline sobre grade de 48, traço 3, junta e ponta
arredondadas**. É a construção compartilhada que cria o parentesco — não a forma.

| Arquivo | Marca | Lê bem até |
|---|---|---|
| `mitchel-sistemas-mark.svg` | círculo + linhas de sinal | ~24px |
| `lucas-mitchel-dev-mark.svg` | monograma LM | ~17px |

## currentColor

Nenhuma das duas tem cor embutida: as duas herdam `currentColor`. Para colorir,
defina `color` no elemento pai — normalmente `var(--icon-default)` ou
`var(--text-primary)`. É isso que faz a logo acompanhar a troca de tema, e é o
que a versão antiga em PNG não conseguia fazer.

```html
<span style="color: var(--icon-default)">
  <!-- svg inline aqui -->
</span>
```

## Assinatura (marca + nome)

O nome **não** está no SVG, de propósito: texto dentro de SVG depende da fonte
estar carregada e não é selecionável nem lido direito por leitor de tela.
A assinatura se monta em HTML, com a marca ao lado do nome em `--font-display`.

⚠️ Para uso impresso ou em fundo de terceiros, o nome deveria estar vetorizado
em curvas. Isso exige o arquivo da fonte ou um redesenho — fica como pendência,
não bloqueia o uso em web.
