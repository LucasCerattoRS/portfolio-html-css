#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════
                      REFINARIA DE PIXELS S.A.
        "Transformando pixels brutos em rems refinados, com a
                  seriedade que ninguém pediu."
═══════════════════════════════════════════════════════════════════════

A aula 5 pedia uma coisa: trocar as medidas de px para rem.
Tecnicamente, isso é dividir por 16. Uma calculadora resolvia.
Uma pessoa com paciência resolvia. Até de cabeça dava.

Nós, porém, construímos uma refinaria.

Fluxo industrial da planta:

    styles/style.px.css ──▶ [ NÚCLEO MATEMÁTICO ÷16 ] ──▶ styles/style.css
        (minério bruto)        (a função. A função.)       (produto final)

Uso:
    python3 refinaria_de_pixels.py               # turno normal de refino
    python3 refinaria_de_pixels.py --dramatico   # narração épica por divisão
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal, getcontext
from functools import lru_cache
from pathlib import Path

# ────────────────────────── CONSTANTES DA EMPRESA ──────────────────────────

# Precisão bancária de 28 casas decimais. Estamos dividindo por 16:
# não é hora de arriscar.
getcontext().prec = 28

# A constante mais importante da tipografia ocidental: o font-size padrão
# dos navegadores. Não muda desde os anos 90. Mas E SE mudar? Aí trocamos
# UMA linha aqui e recompilamos o império. É por isso que este arquivo
# existe. É. Por. Isso.
CONSTANTE_UNIVERSAL_DA_TIPOGRAFIA = Decimal("16")

# Detector de pixels brutos na natureza: "24px", "21.5px", "615px"...
# (\d*\.?\d+) também aceita ".5px": com \d+ na frente o ponto ficava de fora
# e ".5px" virava ".0.3125rem" (CSS inválido).
GARIMPO_DE_PIXEL = re.compile(r"(\d*\.?\d+)px\b")

# Número de vezes que tudo isto poderia ter sido um Ctrl+H:
OPORTUNIDADES_IGNORADAS = float("inf")

LOG = logging.getLogger("refinaria")

FRASES_DE_EFEITO = (
    "a plateia vai ao delírio.",
    "nenhum algarismo foi ferido.",
    "a NASA ligou perguntando como conseguimos.",
    "dezesseis avos de pura engenharia.",
    "auditoria aprovou em primeira instância.",
    "o estagiário chorou de emoção.",
)


class PixelInimaginavelError(ArithmeticError):
    """Lançado se a matemática quebrar. (Spoiler: ela não quebra.)"""


# ────────────────────────── O NÚCLEO MATEMÁTICO ──────────────────────────

@lru_cache(maxsize=4096)
def calcular_x_px_dividido_por_16_px(x_px: str) -> Decimal:
    """A função. A razão de esta empresa existir.

    Recebe X pixels e executa a operação mais sofisticada de todo o
    repositório: X ÷ 16. Com cache LRU, porque dividir 24 por 16 SEIS
    vezes seria um desperdício imperdoável de recursos computacionais.

    Inclui auditoria de reversibilidade: se (resultado × 16) não devolver
    o pixel original, o universo está com defeito de fabricação e esta
    empresa se recusa a continuar operando nele.
    """
    pixels = Decimal(x_px)
    resultado = pixels / CONSTANTE_UNIVERSAL_DA_TIPOGRAFIA

    if resultado * CONSTANTE_UNIVERSAL_DA_TIPOGRAFIA != pixels:
        raise PixelInimaginavelError(
            f"{x_px}px entrou na divisão e não voltou inteiro. "
            "Evacuar a planta. Acionar o matemático de plantão."
        )

    return resultado


def polir_para_exibicao(valor: Decimal) -> str:
    """Setor de acabamento: remove zeros constrangedores à direita.

    Ninguém merece entregar um '1.5000000' para o cliente.
    """
    texto = format(valor, "f")
    if "." in texto:
        texto = texto.rstrip("0").rstrip(".")
    return texto or "0"


# ────────────────────────── A LINHA DE PRODUÇÃO ──────────────────────────

@dataclass
class LinhaDeProducao:
    """Percorre o CSS, minera cada px e o encaminha ao Núcleo Matemático."""

    dramatico: bool = False
    contagem: Counter = field(default_factory=Counter)
    auditorias_aprovadas: int = 0

    def refinar_documento(self, css_bruto: str) -> str:
        saida = []
        for numero, linha in enumerate(css_bruto.splitlines(keepends=True), start=1):
            saida.append(
                GARIMPO_DE_PIXEL.sub(lambda m: self._refinar(m, numero), linha)
            )
        return "".join(saida)

    def _refinar(self, achado: re.Match, numero_da_linha: int) -> str:
        bruto = achado.group(1)
        refinado = calcular_x_px_dividido_por_16_px(bruto)
        rotulo = polir_para_exibicao(refinado) + "rem"

        self.contagem[bruto + "px"] += 1
        self.auditorias_aprovadas += 1

        if self.dramatico:
            time.sleep(0.45)
            frase = FRASES_DE_EFEITO[(self.auditorias_aprovadas - 1) % len(FRASES_DE_EFEITO)]
            LOG.info(
                "⛏️  linha %02d: %spx entra no forno... ÷16... sai %s — %s",
                numero_da_linha, bruto, rotulo, frase,
            )
        else:
            LOG.info(
                "linha %02d: %6spx ──▶ %10s · auditoria ok",
                numero_da_linha, bruto, rotulo,
            )
        return rotulo


# ──────────────────────── DEPARTAMENTOS DE APOIO ────────────────────────

def moldura_corporativa(*linhas: str) -> str:
    """Departamento de Identidade Visual. Verba anual: uma função."""
    largura = max(len(linha) for linha in linhas) + 4
    topo = "╔" + "═" * largura + "╗"
    base = "╚" + "═" * largura + "╝"
    meio = [f"║  {linha.ljust(largura - 2)}║" for linha in linhas]
    return "\n".join([topo, *meio, base])


def carimbo_de_qualidade(total: int) -> str:
    """Selo impresso no produto final. Exigência da ISO-0625."""
    agora = time.strftime("%d/%m/%Y %H:%M:%S")
    return (
        "/* ════════════════════════════════════════════════════════════════\n"
        "   ARQUIVO GERADO PELA REFINARIA DE PIXELS S.A. — NÃO EDITE À MÃO.\n"
        "   Fonte da verdade: styles/style.px.css (o minério bruto).\n"
        "   Para recompilar:  python3 refinaria_de_pixels.py\n"
        f"   Lote nº 0001 · {agora} · {total} medidas divididas por 16\n"
        "   Auditoria de reversibilidade: 100% aprovada · pixels feridos: 0\n"
        "   ════════════════════════════════════════════════════════════════ */\n\n"
    )


def relatorio_de_producao(linha: LinhaDeProducao, duracao: float, saida: Path) -> None:
    total = linha.auditorias_aprovadas
    LOG.info("─" * 58)
    LOG.info("RELATÓRIO DE PRODUÇÃO DO LOTE Nº 0001")
    LOG.info("medidas refinadas ............. %d", total)
    LOG.info("auditorias aprovadas .......... %d de %d (100%%)", total, total)

    if linha.contagem:
        campeao, aparicoes = linha.contagem.most_common(1)[0]
        LOG.info("funcionário do mês ............ %s (%d aparições)", campeao, aparicoes)

        maior = max(linha.contagem, key=lambda chave: Decimal(chave[:-2]))
        maior_rem = polir_para_exibicao(calcular_x_px_dividido_por_16_px(maior[:-2]))
        LOG.info("maior pixel já minerado ....... %s (virou %srem)", maior, maior_rem)

    LOG.info("pixels feridos no processo .... 0")
    LOG.info("tempo de refino ............... %.2f ms", duracao * 1000)
    LOG.info("idas à calculadora poupadas ... %d", total)
    LOG.info("produto entregue em ........... %s", saida)

    if total == 16:
        LOG.info("nota do turno: 16 medidas divididas por 16. "
                 "O universo piscou pra gente.")

    LOG.info("─" * 58)
    LOG.info("a refinaria agradece. Volte sempre que o navegador "
             "mudar a fonte padrão.")


# ─────────────────────────── TURNO PRINCIPAL ───────────────────────────

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="refinaria_de_pixels",
        description=(
            "Converte um CSS de px para rem dividindo cada medida por 16 — "
            "com toda a infraestrutura que essa operação NÃO precisava."
        ),
    )
    raiz = Path(__file__).resolve().parent
    parser.add_argument(
        "--fonte", type=Path, default=raiz / "styles" / "style.px.css",
        help="o minério bruto (CSS em px)",
    )
    parser.add_argument(
        "--saida", type=Path, default=raiz / "styles" / "style.css",
        help="o produto refinado (CSS em rem)",
    )
    parser.add_argument(
        "--dramatico", action="store_true",
        help="narra cada divisão como um lançamento de foguete",
    )
    args = parser.parse_args(argv)

    # No Windows com saída redirecionada (pipe/arquivo) o console é cp1252 e a
    # moldura ╔═╗ derrubava o script com UnicodeEncodeError ANTES de refinar.
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(errors="replace")

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [REFINARIA] %(message)s",
        datefmt="%H:%M:%S",
    )

    print(moldura_corporativa(
        "REFINARIA DE PIXELS S.A.",
        "divisão por dezesseis com rigor industrial",
        'certificação ISO-0625 · "um px vale 0.0625rem"',
    ), flush=True)  # a fachada da empresa aparece ANTES do turno começar

    if not args.fonte.exists():
        LOG.error("matéria-prima não encontrada em %s — sem minério não há refino.",
                  args.fonte)
        return 1

    css_bruto = args.fonte.read_text(encoding="utf-8")
    jazida = len(GARIMPO_DE_PIXEL.findall(css_bruto))
    LOG.info("jazida localizada: %d medidas em px aguardando refino.", jazida)

    if args.dramatico:
        LOG.info("🚨 modo dramático ativado. Sirene acionada. Turno iniciado.")
        time.sleep(1.0)

    inicio = time.perf_counter()
    linha = LinhaDeProducao(dramatico=args.dramatico)
    css_refinado = linha.refinar_documento(css_bruto)
    duracao = time.perf_counter() - inicio

    args.saida.write_text(
        carimbo_de_qualidade(linha.auditorias_aprovadas) + css_refinado,
        encoding="utf-8",
    )

    relatorio_de_producao(linha, duracao, args.saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
