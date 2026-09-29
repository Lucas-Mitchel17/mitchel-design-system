#!/usr/bin/env python3
"""Gera as duas versoes da documentacao viva a partir de UMA fonte.

  docs/index.html     -> standalone, <link> para os CSS reais do repo.
                         Nunca desatualiza: renderiza os arquivos de verdade.
  docs/_artifact.html -> mesmo conteudo com o CSS embutido, para publicar.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Chakra+Petch:wght@400;500;600;700&'
         'family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&'
         'family=Orbitron:wght@500;700&family=Play:wght@400;700&display=swap">')

PAGE_CSS = """
html,body{background:#080c1c}
.page{font-family:var(--font-body);background:var(--surface-1);color:var(--text-primary);
  min-height:100%;padding-block:var(--space-8);
  padding-inline:clamp(var(--space-4),5vw,var(--space-16))}
.wrap{max-width:var(--container-max);margin-inline:auto;display:flex;flex-direction:column;gap:var(--space-16)}
.eyebrow{font-family:var(--font-mono);font-size:var(--text-caption);letter-spacing:var(--tracking-caps);
  text-transform:uppercase;color:var(--text-muted)}
h1{font-family:var(--font-display);font-size:var(--text-h2);margin:0;letter-spacing:var(--tracking-tight)}
h2{font-family:var(--font-display);font-size:var(--text-h3);margin:0}
h3{font-family:var(--font-display);font-size:var(--text-h4);margin:0}
p{margin:0;color:var(--text-secondary);max-width:var(--measure)}
section{display:flex;flex-direction:column;gap:var(--space-5)}
.bar{display:flex;flex-wrap:wrap;gap:var(--space-4);align-items:flex-end;
  padding-block-end:var(--space-6);border-bottom:1px solid var(--divider)}
.switch{display:flex;gap:var(--space-1);padding:var(--space-1);border:1px solid var(--border-default);
  border-radius:var(--radius-md);background:var(--surface-2)}
.switch button{font:inherit;font-size:var(--text-small);padding:var(--space-2) var(--space-4);
  border:none;border-radius:var(--radius-sm);background:none;color:var(--text-secondary);cursor:pointer;
  transition:background var(--duration-fast) var(--ease-out),color var(--duration-fast) var(--ease-out)}
.switch button[aria-pressed="true"]{background:var(--action-primary);color:var(--text-on-action-primary);
  font-weight:var(--weight-medium)}
.switch button:disabled{color:var(--text-disabled);cursor:not-allowed}
table{width:100%;border-collapse:collapse;font-size:var(--text-small)}
th{text-align:left;font-family:var(--font-mono);font-size:var(--text-caption);
  letter-spacing:var(--tracking-caps);text-transform:uppercase;color:var(--text-muted);
  font-weight:var(--weight-regular);padding-block:var(--space-2);border-bottom:1px solid var(--divider)}
td{padding-block:var(--space-3);border-bottom:1px solid var(--border-subtle);vertical-align:middle}
code,.mono{font-family:var(--font-mono);font-size:0.92em}
.scroller{overflow-x:auto}
.chip{display:inline-block;width:34px;height:22px;border-radius:var(--radius-sm);
  border:1px solid var(--border-subtle);vertical-align:middle}
.ratio{font-family:var(--font-mono);font-variant-numeric:tabular-nums}
.pass{color:var(--text-highlight)} .fail{color:#ff6b6b;font-weight:var(--weight-bold)}
.ramp{display:flex;gap:var(--space-1);flex-wrap:wrap}
.ramp>div{flex:1 1 56px;display:flex;flex-direction:column;gap:var(--space-1)}
.ramp .sw{height:48px;border-radius:var(--radius-sm);border:1px solid var(--border-subtle)}
.ramp .nm{font-family:var(--font-mono);font-size:10px;color:var(--text-muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:var(--space-5)}
.card{padding:var(--space-6);border:1px solid var(--border-subtle);border-radius:var(--radius-lg);
  background:var(--surface-3);box-shadow:var(--elevation-1);display:flex;flex-direction:column;gap:var(--space-3)}
.btn{font:inherit;font-weight:var(--weight-medium);padding:var(--space-3) var(--space-6);
  border-radius:var(--radius-md);border:1px solid transparent;cursor:pointer;
  transition:background var(--duration-base) var(--ease-out),color var(--duration-base) var(--ease-out)}
.btn-primary{background:var(--action-primary);color:var(--text-on-action-primary)}
.btn-primary:hover{background:var(--action-primary-hover)}
.btn-secondary{background:var(--action-secondary);color:var(--action-secondary-text);
  border-color:var(--action-secondary-border)}
.btn-secondary:hover{background:var(--action-primary);color:var(--text-on-action-primary)}
.btn:disabled{background:var(--surface-disabled);color:var(--text-disabled);
  border-color:var(--border-disabled);cursor:not-allowed}
.row{display:flex;gap:var(--space-4);flex-wrap:wrap;align-items:center}
.stack-demo{display:flex;flex-direction:column;gap:var(--space-2)}
.sp{background:var(--action-primary);height:14px;border-radius:2px}
.chain{display:flex;flex-wrap:wrap;gap:var(--space-3);align-items:center;font-family:var(--font-mono);
  font-size:var(--text-caption)}
.chain span{padding:var(--space-2) var(--space-3);border:1px solid var(--border-subtle);
  border-radius:var(--radius-sm);background:var(--surface-2)}
.chain b{color:var(--text-muted);font-weight:var(--weight-regular)}
.logo-row{display:flex;gap:var(--space-10);flex-wrap:wrap;align-items:flex-end;color:var(--icon-default)}
.logo-item{display:flex;flex-direction:column;gap:var(--space-3);align-items:flex-start;color:var(--icon-default)}
.log{display:flex;flex-direction:column;gap:var(--space-6)}
.log h3{font-size:var(--text-lead);font-family:var(--font-body);font-weight:var(--weight-medium)}
.log ul{margin:0;padding-left:var(--space-5);display:flex;flex-direction:column;gap:var(--space-2)}
.log li{color:var(--text-secondary);max-width:var(--measure)}
.log li b{color:var(--text-primary);font-weight:var(--weight-medium)}
.stamp{display:inline-flex;align-items:center;gap:var(--space-2);padding:var(--space-1) var(--space-3);
  border:1px solid var(--border-strong);border-radius:var(--radius-full);color:var(--text-highlight);
  font-family:var(--font-mono);font-size:var(--text-caption)}
.spec{display:flex;align-items:baseline;gap:var(--space-5);flex-wrap:wrap}
.spec .n{font-family:var(--font-mono);font-size:var(--text-caption);color:var(--text-muted);
  width:120px;flex-shrink:0}
.spec .t{font-family:var(--font-display);line-height:var(--leading-tight)}
:focus-visible{outline:2px solid var(--focus-ring);outline-offset:3px;border-radius:var(--radius-sm)}
@media (max-width:560px){.spec .n{width:100%}}
"""

# As logos vem dos ARQUIVOS de assets/logo/, nao de copias aqui dentro.
# Antes a do Lucas era um rascunho de L+M desenhado a mao neste script, e
# ficou para tras quando a marca `< LM >` foi vetorizada de verdade: a doc
# mostrava uma logo que nao existia mais. Lendo do arquivo, nao repete.
def logo(nome, altura):
    svg = (ROOT / "assets" / "logo" / f"{nome}.svg").read_text(encoding="utf-8")
    # fora o comentario XML e o <title>: o rotulo ja esta no aria-label, e
    # inline o <title> vira tooltip em cima do que a pagina diz do lado.
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    svg = re.sub(r"<title>.*?</title>", "", svg, flags=re.S)
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2)
    return svg.replace("<svg", f'<svg style="height:{altura}px;width:auto"', 1)

# (frente, fundo, papel, mínimo aplicável)
# 4.5 = texto corrido (WCAG 1.4.3 AA). 3.0 = texto grande.
# Desabilitado é isento pela 1.4.3, mas ilegível continua sendo ilegível:
# cobramos 3.0 por conta própria — foi esse par que produziu o cinza-sobre-
# cinza do site antigo.
PAIRS = [
 ("--text-primary","--surface-1","texto padrão sobre a base",4.5),
 ("--text-secondary","--surface-1","texto de apoio",4.5),
 ("--text-muted","--surface-1","texto discreto",4.5),
 ("--text-highlight","--surface-1","ênfase",4.5),
 ("--text-primary","--surface-2","texto sobre seção recuada",4.5),
 ("--text-primary","--surface-3","texto sobre card elevado",4.5),
 ("--text-on-action-primary","--action-primary","texto no botão primário",4.5),
 ("--action-secondary-text","--surface-1","texto do botão secundário",4.5),
 ("--brand-mark-from","--surface-1","marca · ponta clara do gradiente",3.0),
 ("--brand-mark-to","--surface-1","marca · ponta escura do gradiente",3.0),
 ("--brand-mark","--surface-1","marca · chapado de fallback",3.0),
 ("--text-disabled","--surface-disabled","desabilitado · isento na WCAG",3.0),
]
ROLES = ["--surface-1","--surface-2","--surface-3","--brand-mark-from","--brand-mark-to","--brand-mark","--text-primary","--text-secondary","--text-muted",
 "--text-highlight","--action-primary","--action-primary-hover","--text-on-action-primary",
 "--border-subtle","--border-default","--border-strong","--icon-default","--divider",
 "--focus-ring","--glow-action","--scrim","--surface-disabled","--text-disabled"]
RAMPS = ["neutral-950","neutral-900","neutral-800","neutral-700","neutral-600","neutral-500",
 "neutral-400","neutral-300","neutral-200","neutral-100","neutral-50","neutral-0"]
BRANDS = ["brand-300","brand-400","brand-500","brand-600","brand-700","brand-800","accent-500"]
SCALE = [("--text-h1 · degrau 6",61),("--text-h2 · degrau 5",49),("--text-h3 · degrau 4",39),
         ("--text-h4 · degrau 3",31),("--text-lead · degrau 2",25),("--text-body · degrau 1",20)]
SPACES = [1,2,3,4,5,6,8,10,12,16,20,24]

def rows_pairs():
    return "".join(f'<tr><td><code>{f}</code></td><td><code>{b}</code></td>'
        f'<td style="color:var(--text-muted)">{d}</td>'
        f'<td class="mono" style="color:var(--text-muted)">{m:.1f}</td>'
        f'<td class="ratio" data-fg="{f}" data-bg="{b}" data-min="{m}">—</td></tr>'
        for f,b,d,m in PAIRS)

def rows_roles():
    return "".join(f'<tr><td><span class="chip" data-swatch="{t}"></span></td>'
        f'<td><code>{t}</code></td><td class="mono" data-value="{t}" '
        f'style="color:var(--text-muted)">—</td></tr>' for t in ROLES)

def ramp(keys):
    return "".join(f'<div><div class="sw" style="background:var(--ramp-{k})"></div>'
        f'<div class="nm">{k.split("-")[-1]}</div></div>' for k in keys)

def spec():
    return "".join(f'<div class="spec"><span class="n">{n}</span>'
        f'<span class="t" style="font-size:{px}px">Feito pra durar</span></div>' for n,px in SCALE)

def spaces():
    return "".join(f'<div class="row"><span class="mono" style="width:96px;color:var(--text-muted)">'
        f'--space-{n}</span><span class="sp" style="width:var(--space-{n})"></span>'
        f'<span class="mono" style="color:var(--text-muted)">{n*4}px</span></div>' for n in SPACES)

BODY = f"""
<div class="page" id="app" data-theme="mitchel-sistemas" data-mode="dark">
<div class="wrap">

<header class="bar">
  <div style="flex-grow:1;display:flex;flex-direction:column;gap:var(--space-2)">
    <div class="eyebrow">Documentação viva</div>
    <h1>Mitchel Design System</h1>
    <p>Tudo nesta página é desenhado pelos próprios tokens do sistema. Troque a marca e
    veja o que muda — e, principalmente, o que não muda.</p>
  </div>
  <div style="display:flex;gap:var(--space-4);flex-wrap:wrap">
    <div><div class="eyebrow" style="margin-bottom:var(--space-2)">Marca</div>
      <div class="switch" role="group" aria-label="Marca">
        <button type="button" id="t-ms" data-theme-btn="mitchel-sistemas" aria-pressed="true">Mitchel Sistemas</button>
        <button type="button" id="t-lm" data-theme-btn="lucas-mitchel-dev" aria-pressed="false">Lucas Mitchel Dev</button>
      </div></div>
    <div><div class="eyebrow" style="margin-bottom:var(--space-2)">Modo</div>
      <div class="switch" role="group" aria-label="Modo">
        <button type="button" id="m-dark" data-mode-btn="dark" aria-pressed="true">Escuro</button>
        <button type="button" id="m-light" data-mode-btn="light" aria-pressed="false">Claro</button>
      </div></div>
  </div>
</header>

<section>
  <div class="eyebrow">Estado</div>
  <h2>O que mudou até aqui</h2>
  <p>Esta página é gerada a partir dos arquivos do repositório, então o que está acima
  é sempre o estado real do sistema. O que segue é o caminho até ele.</p>
  <div class="log">

    <div>
      <h3><span class="stamp">v0.2.0</span> &nbsp;O sistema</h3>
      <ul>
        <li><b>Reset e a11y foram para dentro de <code>@layer base</code>.</b> Fora de camada
        eles venciam qualquer utilitário: <code>button {{ background: none }}</code> atropelava
        <code>.bg-action</code> e todo botão saía transparente. Apareceu ao plugar o sistema
        no lucasmitchel.dev.</li>
        <li><b>O <code>index.css</code> parou de importar os dois temas.</b> O site pessoal
        carregava as rampas da empresa no bundle. Peso morto hoje, problema de verdade no dia
        que existir um tema por cliente. Cada projeto importa só o seu.</li>
        <li><b><code>@import</code> em forma de string, nunca <code>url()</code>.</b> O bundler
        embute a primeira e deixa a segunda como import de runtime — e aí os tokens não entram
        no CSS final.</li>
        <li><b>Container de 72rem para 84rem</b> (1344px), gutter de 20–40px para 24–64px.
        O container cresceu; o texto não — parágrafo continua preso em <code>--measure</code>.</li>
        <li><b><code>package.json</code> para consumo via npm</b>, direto do GitHub.</li>
      </ul>
    </div>

    <div>
      <h3>A marca</h3>
      <ul>
        <li><b>A marca <code>&lt; LM &gt;</code> foi vetorizada</b> a partir do estudo gerado
        online. A geometria foi regularizada, não copiada: os dois chevrons tinham ~4px de
        desvio entre si e as arestas não fechavam.</li>
        <li><b>Os chevrons subiram 32 unidades.</b> Estavam centrados em y=120, herdado da
        imagem original; L e M têm centro em ~80. Agora flanqueiam as letras em vez de ficarem
        caídos.</li>
        <li><b>O M recorta a chave da direita por máscara</b>, não por contorno colorido —
        assim funciona em qualquer cor e sobre qualquer fundo. Antes a barra diagonal cruzava
        a chave e as duas viravam um bloco só.</li>
        <li><b>A marca voltou a ter cor:</b> gradiente gelo → azul, com paradas diferentes por
        modo. Passou por uma versão monocromática antes — o gelo tem 1.31:1 sobre fundo claro,
        então o mesmo gradiente nos dois modos apagaria a marca no claro.</li>
        <li><b>Esta página mostrava um rascunho.</b> A logo do Lucas aqui era um L+M desenhado
        à mão dentro do gerador da doc, e ficou para trás quando a marca real foi vetorizada.
        Agora a página lê os arquivos de <code>assets/logo/</code> — não tem como repetir.</li>
      </ul>
    </div>

    <div>
      <h3>Quem já consome</h3>
      <ul>
        <li><b>lucasmitchel.dev</b> — Astro 5 + Tailwind 4, 4 páginas em 2 idiomas.
        Foi plugando o sistema nele que os quatro bugs de CSS acima apareceram.</li>
        <li><b>mitchelsistemas.com.br</b> — migrado de Astro 2 + Tailwind 3 para Astro 5 +
        Tailwind 4 consumindo o sistema. As cores da empresa não mudaram de valor: mudaram de
        casa, de <code>tailwind.config</code> para os tokens.</li>
      </ul>
    </div>

    <div>
      <h3>Em aberto</h3>
      <ul>
        <li>A <b>Play</b> do site da empresa precisa de substituta — três opções em
        <code>docs/fontes.md</code>, recomendação é Chakra Petch.</li>
        <li>O nome da assinatura <b>não está vetorizado em curvas</b>. Não bloqueia web;
        bloqueia impressão e fundo de terceiro.</li>
        <li>O <code>package.json</code> ainda declara <code>0.1.0</code> enquanto a tag já é
        <code>v0.2.0</code>.</li>
      </ul>
    </div>

  </div>
</section>

<section>
  <div class="eyebrow">As três camadas</div>
  <h2>Componente nunca toca no primitivo</h2>
  <p>É a regra que sustenta o sistema inteiro. Cada token aponta para o de cima, e só a
  primeira camada muda de marca para marca.</p>
  <div class="chain">
    <span><b>primitivo</b><br><span id="chain-1">—</span></span><b>→</b>
    <span><b>semântico</b><br>--action-primary</span><b>→</b>
    <span><b>componente</b><br>--button-bg</span>
  </div>
</section>

<section>
  <div class="eyebrow">Contraste</div>
  <h2>Os pares, conferidos agora</h2>
  <p>Calculado ao vivo a partir do que o navegador realmente resolveu — troque a marca
  ou o modo e os números mudam junto. Cada par é cobrado pelo mínimo que se aplica a ele:
  4.5 para texto corrido, 3.0 para texto grande e para estado desabilitado.</p>
  <div class="scroller"><table><thead><tr><th>Frente</th><th>Fundo</th><th>Papel</th>
  <th>Mínimo</th><th>Razão</th></tr></thead><tbody>{rows_pairs()}</tbody></table></div>
</section>

<section>
  <div class="eyebrow">Cor</div>
  <h2>Camada semântica</h2>
  <p>Vinte papéis. Nenhum deles menciona uma cor, uma marca ou uma tela.</p>
  <div class="scroller"><table><thead><tr><th></th><th>Token</th><th>Valor resolvido</th></tr></thead>
  <tbody>{rows_roles()}</tbody></table></div>
</section>

<section>
  <div class="eyebrow">Cor</div>
  <h2>Rampas do tema</h2>
  <p>A única camada que muda entre as duas marcas. Um cliente novo entrega estas rampas e
  ganha o sistema inteiro.</p>
  <div><div class="eyebrow" style="margin-bottom:var(--space-3)">Neutros</div>
    <div class="ramp">{ramp(RAMPS)}</div></div>
  <div><div class="eyebrow" style="margin-bottom:var(--space-3)">Marca e acento</div>
    <div class="ramp">{ramp(BRANDS)}</div></div>
</section>

<section>
  <div class="eyebrow">Tipografia</div>
  <h2>Escala modular 1.25</h2>
  <p>Mesma proporção nas duas marcas — muda a fonte, não a escala. Fluida por
  <code>clamp()</code>, então não existe salto de breakpoint.</p>
  {spec()}
  <div class="grid" style="margin-top:var(--space-4)">
    <div class="card"><div class="eyebrow">--font-display</div>
      <div style="font-family:var(--font-display);font-size:var(--text-h4)">Mitchel</div></div>
    <div class="card"><div class="eyebrow">--font-body</div>
      <div style="font-family:var(--font-body);font-size:var(--text-h4)">Mitchel</div></div>
    <div class="card"><div class="eyebrow">--font-mono</div>
      <div style="font-family:var(--font-mono);font-size:var(--text-h4)">Mitchel</div></div>
  </div>
</section>

<section>
  <div class="eyebrow">Espaçamento</div>
  <h2>Base 4px</h2>
  <p>Acima dela vivem três tokens semânticos — <code>--section-padding-block</code>,
  <code>--container-gutter</code> e <code>--stack-gap</code> — que definem a densidade da marca.</p>
  <div class="stack-demo">{spaces()}</div>
</section>

<section>
  <div class="eyebrow">Componentes</div>
  <h2>Os tokens em uso</h2>
  <p>Nada aqui tem cor escrita à mão. Dê Tab para ver o anel de foco — o site antigo não tinha nenhum.</p>
  <div class="row">
    <button type="button" class="btn btn-primary">Ação primária</button>
    <button type="button" class="btn btn-secondary">Secundária</button>
    <button type="button" class="btn btn-primary" disabled>Desabilitada</button>
  </div>
  <div class="grid">
    <div class="card"><h3>Card</h3><p>Superfície elevada, contorno sutil, elevação 1.</p></div>
    <div class="card" style="box-shadow:var(--elevation-2)"><h3>Elevação 2</h3>
      <p>Mesma superfície, sombra maior.</p></div>
    <div class="card" style="box-shadow:0 0 34px var(--glow-action)"><h3>Glow</h3>
      <p>Feedback de interação. Não é elevação: papel diferente, token diferente.</p></div>
  </div>
</section>

<section>
  <div class="eyebrow">Marca</div>
  <h2>As logos</h2>
  <p>Nenhuma tem cor embutida: todas herdam <code>currentColor</code>, e é isso que faz a
  logo acompanhar a troca de tema — o PNG antigo não conseguia. A versão de gradiente lê
  <code>--brand-mark-from</code> e <code>--brand-mark-to</code> quando está inline, então
  troca de modo sozinha.</p>
  <p style="color:var(--text-muted)"><strong>Só aqui</strong> cada marca está presa ao próprio
  tema — o seletor lá em cima não as pinta. Seria enganoso: a marca do Lucas sairia verde
  enquanto a empresa estivesse selecionada. O modo claro/escuro continua valendo.</p>
  <div class="logo-row">
    <div class="logo-item" data-theme-pin="mitchel-sistemas" data-theme="mitchel-sistemas" data-mode="dark">{logo("mitchel-sistemas-mark", 64)}
      <span class="eyebrow">mitchel sistemas</span></div>
    <div class="logo-item" data-theme-pin="lucas-mitchel-dev" data-theme="lucas-mitchel-dev" data-mode="dark">{logo("lucas-mitchel-dev-mark-gradient", 64)}
      <span class="eyebrow">lucas mitchel dev · gradiente</span></div>
  </div>
</section>

<section>
  <div class="eyebrow">Marca</div>
  <h2>Peso óptico, não recorte</h2>
  <p>A marca completa tem seis formas: dois chevrons, L, M, a barra e a cauda. Reduzida,
  ela não some por igual — <strong>os chevrons somem primeiro</strong>, porque são os
  traços mais finos. Por isso as variantes não são recortes arbitrários. Fonte tem peso
  óptico e ninguém estranha; logo tem pelo mesmo motivo.</p>
  <div class="logo-row">
    <div class="logo-item" data-theme-pin="lucas-mitchel-dev" data-theme="lucas-mitchel-dev" data-mode="dark">{logo("lucas-mitchel-dev-mark", 72)}
      <span class="eyebrow">completa · acima de 40px</span></div>
    <div class="logo-item" data-theme-pin="lucas-mitchel-dev" data-theme="lucas-mitchel-dev" data-mode="dark">{logo("lucas-mitchel-dev-mark-lockup", 40)}
      <span class="eyebrow">assinatura · 24–40px</span></div>
    <div class="logo-item" data-theme-pin="lucas-mitchel-dev" data-theme="lucas-mitchel-dev" data-mode="dark">{logo("lucas-mitchel-dev-mark-compact", 24)}
      <span class="eyebrow">compacta · abaixo de 24px</span></div>
  </div>
  <div class="scroller"><table><thead><tr><th>Variante</th><th>O que muda</th><th>Por quê</th></tr></thead>
  <tbody>
  <tr><td class="mono">completa</td><td>tudo, no traço do desenho</td>
    <td style="color:var(--text-muted)">a marca como foi desenhada</td></tr>
  <tr><td class="mono">assinatura</td><td>chevrons ~45% mais grossos, sem a cauda</td>
    <td style="color:var(--text-muted)">os chevrons desapareceriam nessa faixa; a cauda desequilibra ao lado do nome</td></tr>
  <tr><td class="mono">compacta</td><td>sem chevrons: L + M + barra</td>
    <td style="color:var(--text-muted)">abaixo de 24px nem engrossados sobrevivem — isto é o que ainda lê a 16px</td></tr>
  </tbody></table></div>
  <p>O nome <strong>não</strong> está dentro do SVG, de propósito: texto em SVG depende da
  fonte carregada, não é selecionável e não é lido direito por leitor de tela. A assinatura
  se monta em HTML — marca ao lado do nome em <code>--font-display</code>.</p>
</section>

</div></div>
"""

JS = """
(function () {
  var app = document.getElementById('app');
  var probe = document.createElement('span');
  probe.style.display = 'none';
  app.appendChild(probe);

  function resolve(token) {
    probe.style.color = '';
    probe.style.color = 'var(' + token + ')';
    var c = getComputedStyle(probe).color;
    return c && c !== 'rgba(0, 0, 0, 0)' ? c : null;
  }
  function rgb(str) {
    var m = str && str.match(/-?[\\d.]+/g);
    return m ? [ +m[0], +m[1], +m[2], m.length > 3 ? +m[3] : 1 ] : null;
  }
  function lum(c) {
    var a = c.slice(0, 3).map(function (v) {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2];
  }
  function hex(c) {
    return '#' + c.slice(0, 3).map(function (v) {
      return ('0' + Math.round(v).toString(16)).slice(-2);
    }).join('');
  }

  function refresh() {
    document.querySelectorAll('[data-swatch]').forEach(function (el) {
      el.style.background = 'var(' + el.getAttribute('data-swatch') + ')';
    });
    document.querySelectorAll('[data-value]').forEach(function (el) {
      var c = rgb(resolve(el.getAttribute('data-value')));
      el.textContent = c ? (c[3] < 1 ? hex(c) + ' · ' + Math.round(c[3] * 100) + '%' : hex(c)) : '—';
    });
    document.querySelectorAll('[data-fg]').forEach(function (el) {
      var f = rgb(resolve(el.getAttribute('data-fg')));
      var b = rgb(resolve(el.getAttribute('data-bg')));
      if (!f || !b) { el.textContent = '—'; return; }
      var l1 = lum(f), l2 = lum(b);
      var r = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
      var min = parseFloat(el.getAttribute('data-min')) || 4.5;
      el.textContent = r.toFixed(2) + ':1';
      el.className = 'ratio ' + (r >= min ? 'pass' : 'fail');
    });
    // Os blocos de logo tem tema proprio. So o MODO acompanha a pagina —
    // e como os dois atributos ficam no MESMO elemento, [data-mode="light"]
    // vence [data-theme] por vir depois no semantic.css.
    var mode = app.getAttribute('data-mode');
    document.querySelectorAll('[data-theme-pin]').forEach(function (el) {
      el.setAttribute('data-mode', el.getAttribute('data-theme-pin') === 'mitchel-sistemas' ? 'dark' : mode);
    });

    var bg = resolve('--surface-1');
    if (bg) { document.body.style.background = bg; }
    var c1 = document.getElementById('chain-1');
    if (c1) {
      var v = rgb(resolve('--ramp-brand-500'));
      c1.textContent = '--ramp-brand-500 ' + (v ? hex(v) : '');
    }
  }

  function press(sel, attr, val) {
    document.querySelectorAll(sel).forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute(attr) === val));
    });
  }

  document.querySelectorAll('[data-theme-btn]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-theme-btn');
      app.setAttribute('data-theme', t);
      press('[data-theme-btn]', 'data-theme-btn', t);
      var light = document.getElementById('m-light');
      var onlyDark = t === 'mitchel-sistemas';
      light.disabled = onlyDark;
      light.title = onlyDark ? 'A marca da empresa é só escura (decisão D10)' : '';
      if (onlyDark) {
        app.setAttribute('data-mode', 'dark');
        press('[data-mode-btn]', 'data-mode-btn', 'dark');
      }
      refresh();
    });
  });
  document.querySelectorAll('[data-mode-btn]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (b.disabled) return;
      var m = b.getAttribute('data-mode-btn');
      app.setAttribute('data-mode', m);
      press('[data-mode-btn]', 'data-mode-btn', m);
      refresh();
    });
  });

  document.getElementById('m-light').disabled = true;
  document.getElementById('m-light').title = 'A marca da empresa é só escura (decisão D10)';
  if (document.fonts && document.fonts.ready) { document.fonts.ready.then(refresh); }
  refresh();
})();
"""

TITLE = "Mitchel Design System"

def inline_css():
    # a doc compara as duas marcas, entao e um dos poucos lugares que
    # legitimamente carrega os dois temas
    order = ["tokens/primitives.css", "tokens/themes/mitchel-sistemas.css",
             "tokens/themes/lucas-mitchel-dev.css", "tokens/semantic.css"]
    return "\n".join((ROOT / f).read_text(encoding="utf-8") for f in order)

# ---- versao do repo: le os CSS de verdade ----
(ROOT / "docs" / "index.html").write_text(
f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
{FONTS}
<link rel="stylesheet" href="../index.css">
<link rel="stylesheet" href="../tokens/themes/mitchel-sistemas.css">
<link rel="stylesheet" href="../tokens/themes/lucas-mitchel-dev.css">
<style>html,body{{margin:0;height:100%}}{PAGE_CSS}</style>
</head>
<body>
{BODY}
<script>{JS}</script>
</body>
</html>
""", encoding="utf-8")

# ---- versao artifact: CSS embutido, sem html/head/body ----
(ROOT / "docs" / "_artifact.html").write_text(
f"""<title>{TITLE}</title>
{FONTS}
<style>
{inline_css()}
{PAGE_CSS}
</style>
{BODY}
<script>{JS}</script>
""", encoding="utf-8")

print("docs/index.html e docs/_artifact.html gerados")
