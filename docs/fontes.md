# Pendência: a fonte de corpo da Mitchel Sistemas

## O problema

Com a decisão D7, a Orbitron ficou restrita a display (logo, H1, números) e **H2/H3
passaram para `--font-body`**. Só que a Play é importada apenas nos pesos **400 e 700**.

Sem 500 e 600, a hierarquia de peso vira um degrau só: ou é normal, ou é negrito.
Um H3 que precisa ser mais leve que um H2 não tem para onde ir.

A Play também não foi desenhada para texto corrido longo — ela é uma display de letra
quadrada, como a Orbitron, só que mais contida.

## Três substitutas, todas no Google Fonts

### 1. Chakra Petch — a recomendada
Pesos 300, 400, 500, 600, 700. Mantém o DNA quadrado e técnico da Play, então o site
não muda de personalidade — ganha só a escala de peso que faltava.
**Troca de menor risco.** Se você não quiser pensar muito, é essa.

### 2. Archivo
Variável de 100 a 900. Grotesca de trabalho, legibilidade excelente em qualquer
tamanho, e neutra o bastante para deixar a Orbitron carregar toda a personalidade.
**Escolha se o site tiver texto longo** — artigo, documentação, estudo de caso.

### 3. Saira
Variável de 100 a 900, um pouco mais estreita e técnica. Rende mais palavra por linha
e tem cara de painel/telemetria.
**Escolha se você quiser densidade** sem perder o tom tech.

## Como testar sem compromisso

A fonte é valor de tema, não token. Trocar é uma linha:

```css
/* tokens/themes/mitchel-sistemas.css */
--font-body: "Chakra Petch", system-ui, sans-serif;
```

Mais o `<link>` do Google Fonts. Nada mais no sistema precisa saber.
Abra `docs/index.html` depois de trocar: o espécime tipográfico e a escala
inteira já renderizam na fonte nova.
