# Portfólio HTML & CSS — agora com Refinaria de Pixels S.A.™

`[ build: passing ]` `[ divisões por 16: 21/21 ]` `[ pixels feridos: 0 ]` `[ over-engineering: 100% ]`

> A aula 5 pedia: *"troque as medidas de `px` para `rem`"*.
> Qualquer pessoa faria isso com uma calculadora. Ou de cabeça. Ou com Ctrl+H.
>
> Nós construímos uma refinaria.

## O problema (que não existia)

Converter `px` para `rem` é dividir por 16. Só isso. Mas fazer isso à mão expõe o projeto a riscos **inaceitáveis**:

- Errar uma vírgula e entregar um `padding` de `13.4375rem` em vez de `1.34375rem`;
- Ter que calcular `21.5 ÷ 16` de cabeça na frente dos outros;
- Precisar refazer tudo se os navegadores mudarem o font-size padrão de 16px (não muda desde os anos 90 — **mas E SE?**).

## A solução (que ninguém pediu)

Este repositório trata `px` como **minério bruto** e `rem` como **produto refinado**. O CSS deste site não é mais editado: é **compilado**. Sim, uma página estática de portfólio agora tem etapa de build. De nada.

```
styles/style.px.css  ──▶  [ NÚCLEO MATEMÁTICO ÷16 ]  ──▶  styles/style.css
   (minério bruto)         refinaria_de_pixels.py         (rems refinados)
                                     │
                                     └─ auditoria: rem × 16 == px (sempre)
```

## A função que sustenta esta empresa

```python
resultado = Decimal(x_px) / CONSTANTE_UNIVERSAL_DA_TIPOGRAFIA   # ou seja: x ÷ 16
```

É isso. **Uma divisão.** As outras ~250 linhas existem para dar a ela a dignidade que merece:

| Infraestrutura | Justificativa do conselho diretor |
|---|---|
| `Decimal` com 28 casas de precisão | Precisão bancária para o seu `padding`. Float erra lá na 15ª casa decimal; nosso cliente não tolera. |
| Cache LRU de 4096 entradas | O valor `24px` aparece **6 vezes** neste projeto. Dividir 24 por 16 seis vezes? Não nesta empresa. Calcula-se UMA vez; as outras cinco saem do estoque. |
| Auditoria de reversibilidade | Toda divisão é conferida na saída: se `resultado × 16 ≠ original`, a produção **para** e dispara `PixelInimaginavelError`. Nunca disparou. Nunca vai. A gente confere mesmo assim. |
| Logging com carimbo de hora | Rastreabilidade total. Sabemos *exatamente* quando o `21.5px` virou `1.34375rem`. (Foi às 18:40:22. Momento lindo.) |
| Modo `--dramatico` | Narra cada divisão como um lançamento de foguete, com pausa dramática de 0,45s por pixel. |
| Suíte com 17 testes | Cobertura de 100% na operação de dividir por dezesseis, incluindo o teste `test_zero_pixels_viram_zero_rem_o_nada_e_preservado`. Dormimos tranquilos. |

## Como operar a planta

```bash
python3 refinaria_de_pixels.py               # turno normal de refino
python3 refinaria_de_pixels.py --dramatico   # turno com narração épica
python3 -m unittest testes_da_refinaria -v   # auditoria externa independente
```

## Mapa da planta

```
.
├── index.html / about.html ........ o site (intocado e feliz)
├── assets/ ........................ imagens
├── styles/
│   ├── style.px.css ............... minério bruto — fonte da verdade, em px
│   └── style.css .................. produto refinado — GERADO, não editar
├── refinaria_de_pixels.py ......... a planta industrial inteira
└── testes_da_refinaria.py ......... auditoria externa (17 testes)
```

## Regras de segurança da planta industrial

1. **NUNCA edite `styles/style.css` à mão.** Ele é um artefato gerado, carimbado com selo de qualidade ISO-0625. Editar à mão é contrabando de unidades.
2. Quer mudar uma medida? Edite o minério (`styles/style.px.css`) **em px, como a natureza os criou**, e recompile.
3. Se o W3C um dia mudar o font-size padrão dos navegadores, altere a `CONSTANTE_UNIVERSAL_DA_TIPOGRAFIA` e recompile o império. Uma linha. É por isso que tudo isto existe. *É. Por. Isso.*
4. Capacete é obrigatório ao ler o regex `(\d*\.?\d+)px\b`.

## Números do último lote (nº 0001)

- **21 medidas refinadas** — que, passadas pela própria refinaria, dão **`1.3125rem` de medidas**. No lote de 16 deu `1rem` cravado e o universo piscou pra gente; aí veio o PR de acessibilidade com mais 5 medidas e a coincidência cósmica foi rebaixada a número quebrado. Faltam 11 para a próxima piscadela (32 medidas, `2rem` redondos).
- Funcionário do mês: **`24px`**, com 6 aparições (será homenageado virando `1.5rem` em todas elas).
- Maior pixel já minerado: **`1000px`** (o breakpoint do mobile), refinado em `62.5rem` sem rachaduras. O antigo recordista, `615px` (largura do conteúdo), segue em `38.4375rem` com honra.
- Caso mais delicado: **`21.5px`** de padding → `1.34375rem`. Cinco casas decimais. A plateia foi ao delírio.
- Tempo total de refino: **0,71 ms**. Idas à calculadora poupadas: 21. Pixels feridos: **0**.

## FAQ

**Não era mais fácil um buscar-e-substituir?**
Era.

**Isso é over-engineering?**
Isso é uma *homenagem* ao over-engineering. Há uma diferença, e ela está documentada em 28 casas decimais.

**Por que Python e não `calc()` do CSS?**
Porque `calc(24px / 16 * 1rem)` resolveria em uma linha, e piadas de uma linha não sustentam uma refinaria.

**O site mudou alguma coisa?**
Visualmente, nada — `24px` e `1.5rem` rendem idêntico com a fonte padrão. Mas agora, se o usuário aumentar o tamanho de fonte do navegador, o layout inteiro acompanha. A piada é o caminho; a acessibilidade é o destino.

**Quantos pixels foram feridos no processo?**
Zero. Todos foram refinados com dignidade e seguem vivos no `style.px.css`, que funciona como museu.

## Roadmap

- [x] v1.0 — Aprender a dividir por 16 *(marco histórico)*
- [ ] v2.0 — Microsserviço REST: `POST /dividir-por-16` com rate limiting
- [ ] v3.0 — Fila Kafka para lotes de pixels em alta demanda
- [ ] v4.0 — Modelo de IA treinado exclusivamente em divisões por dezesseis
- [ ] v5.0 — RemChain™: cada conversão registrada em blockchain
- [ ] v6.0 — IPO na bolsa de valores tipográficos

## Ata de entrega da obra (resumo executivo da diretoria)

> Pronto — a tarefa da aula 5 foi concluída pelo caminho mais longo fisicamente possível. Nasceu a **Refinaria de Pixels S.A.™**: em vez de trocar px por rem na mão, este portfólio agora tem uma *etapa de build industrial* em Python cuja única responsabilidade matemática é dividir por 16.
>
> **Como a piada funciona:** o CSS original virou minério bruto (`styles/style.px.css`, em px, intocado como museu). Rodar `python3 refinaria_de_pixels.py` refina cada medida no Núcleo Matemático — a função `calcular_x_px_dividido_por_16_px()` — e gera o `styles/style.css` final em rem, carimbado com selo de qualidade ISO-0625 e aviso de NÃO EDITE À MÃO. O HTML continua apontando pro mesmo arquivo, então o site renderiza idêntico (e de quebra ficou acessível de verdade, que era o objetivo real da aula).
>
> **O exagero deliberado em volta da divisão:**
> - `Decimal` com 28 casas de precisão ("precisão bancária para o seu `padding`");
> - Cache LRU, porque `24px` aparece 6 vezes e dividir 24 por 16 seis vezes "seria um desperdício imperdoável";
> - Auditoria de reversibilidade em toda conversão (`resultado × 16 == original`, senão dispara `PixelInimaginavelError` e evacua a planta);
> - Relatório de produção com funcionário do mês (`24px`), maior pixel já minerado (`615px → 38.4375rem`) e contagem de pixels feridos (zero);
> - Modo `--dramatico`, que narra cada divisão com 0,45s de pausa e frases tipo "a NASA ligou perguntando como conseguimos";
> - 13 testes unitários (todos passando), incluindo `test_meio_pixel_tambem_tem_direitos` (o lendário `21.5px → 1.34375rem`) e `test_dezesseis_dividido_por_dezesseis_continua_sendo_um`.
>
> **O presente do destino:** o CSS tinha exatamente **16 medidas em px para dividir por 16** — isso virou easter egg no relatório de produção ("o universo piscou pra gente").
>
> Tudo rodado e verificado: 16/16 conversões exatas, zero px sobrando no produto final. Para a experiência completa: `python3 refinaria_de_pixels.py --dramatico`.
>
> — *ata lavrada pelo engenheiro-chefe da planta em 10/06/2026, às 18h40, no exato momento em que o `21.5px` virou `1.34375rem`*
>
> **Adendo de 16/10/2026:** a auditoria de acessibilidade elevou a jazida para **21 medidas** (21/21 conversões exatas, zero px sobrando). O presente do destino foi devolvido: o easter egg agora divide a própria contagem por 16 e só diz que o universo piscou quando o resultado sai redondo. Hoje sai `1.3125rem`. A suíte também cresceu para 17 testes, três deles só para vigiar a piscadela.

## A parte séria (juro que existe)

Este é o portfólio do curso 3 de HTML/CSS (aula 5), cujo exercício real é trocar unidades absolutas (`px`) por relativas (`rem`). A regra é simples: **1rem = font-size do elemento raiz**, que por padrão é 16px em todos os navegadores — logo, `rem = px ÷ 16`. Usar `rem` torna o site acessível: quem aumenta a fonte no navegador vê todo o layout escalar junto, em vez de textos espremidos em caixas fixas.

O script faz exatamente o que a aula pede, em todas as 21 medidas do CSS, com resultado matematicamente exato — ele só escolheu, deliberadamente, o caminho mais longo possível até lá.

## Estado, estrutura e como usar (sem piada)

- **O que é:** portfólio fictício ("Joana Santos") do curso de HTML/CSS da Alura, aula 5 (px → rem),
  mais o script Python que gera o CSS em `rem`.
- **Estado:** completo para o que a aula pede. `styles/style.css` está em sincronia com
  `styles/style.px.css` (conferido em 08/10/2026 regerando e comparando).
- **Ver o site:** abra `index.html` no navegador. **Regerar o CSS:** `python3 refinaria_de_pixels.py`
  (Python 3.7+, só biblioteca padrão). **Testes:** `python3 -m unittest testes_da_refinaria -v`.
- **Tecnologias:** HTML5, CSS3 (custom properties, flexbox, BEM), Python (`re`, `decimal`,
  `functools.lru_cache`, `argparse`, `logging`, `unittest`).

### Revisão de 08/10/2026

- Regex não pegava `.5px` (sem zero na frente): gerava `.0.3125rem`, CSS inválido. Corrigido + teste novo.
- No Windows, com a saída redirecionada (`> log.txt` ou pipe), a moldura `╔═╗` derrubava o script com
  `UnicodeEncodeError` antes de gerar o CSS. Agora caracteres que o console não suporta viram `?`.

### Auditoria de acessibilidade/mobile de 16/10/2026

- Defeito 1: rolagem horizontal em telas ≤ 1000px (larguras fixas de 615px/378px; `scrollWidth` 920 em viewport de 320px).
  Corrigido com `@media (max-width: 1000px)` (coluna única, larguras fluidas) e `img { max-width: 100% }`.
- Defeito 2: anel de foco do teclado quase invisível sobre o fundo preto (computava `rgb(16,16,16)`).
  Corrigido com `a:focus-visible` em 3px na cor terciária. As correções estão em `style.px.css`; `style.css` foi regerado.
- Smoke test headless (sem janela): `NODE_PATH=<node_modules com playwright> node smoke_acessibilidade.js`.
- Limites: não medi contraste de todas as combinações nem usei leitor de tela; as fontes do Google não carregam offline
  (usa fonte de fallback); links sociais continuam do template (ver pendências).

### Pendências

- Os links de redes sociais em `index.html` ainda apontam para os perfis dos instrutores do curso
  (template da Alura), não para os seus.
- O regex também converteria `px` dentro de nomes, como `icone-24px.png` → `icone-1.5rem.png`. Não ocorre
  neste CSS; se ocorrer, exigir que antes do número não haja letra/hífen.

### Para estudar

1. **`rem` x `px` e acessibilidade** — compare `styles/style.px.css` com `styles/style.css`; depois mude o
   tamanho de fonte padrão do navegador (não o zoom) e veja qual dos dois escala.
2. **Expressões regulares com grupo de captura** — `GARIMPO_DE_PIXEL` (`refinaria_de_pixels.py`, linha 54) e
   `re.sub` com função em `refinar_documento()` (linha 122): a função recebe cada `Match` e devolve o texto novo.
3. **`Decimal` x `float`** — `calcular_x_px_dividido_por_16_px()` (linha 78). Rode `0.1 + 0.2` e
   `Decimal("0.1") + Decimal("0.2")` no Python para ver por que existe.
4. **Memoização com `lru_cache`** — decorador na linha 77 e o teste `test_o_cache_trabalha_para_nao_dividir_duas_vezes`.

---

*Refinaria de Pixels S.A. — divisão por dezesseis com rigor industrial desde 2026.*
