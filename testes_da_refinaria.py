#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bateria de testes da operação matemática mais auditada do hemisfério sul.

Cobertura: 100% da divisão por dezesseis. Dormimos tranquilos.

Rodar a auditoria externa:
    python3 -m unittest testes_da_refinaria -v
"""

import unittest
from decimal import Decimal

from refinaria_de_pixels import (
    CONSTANTE_UNIVERSAL_DA_TIPOGRAFIA,
    LinhaDeProducao,
    calcular_x_px_dividido_por_16_px,
    polir_para_exibicao,
)


class TestADivisaoMaisImportanteDoMundo(unittest.TestCase):

    def test_dezesseis_dividido_por_dezesseis_continua_sendo_um(self):
        self.assertEqual(calcular_x_px_dividido_por_16_px("16"), Decimal("1"))

    def test_vinte_e_quatro_pixels_viram_exatamente_um_rem_e_meio(self):
        self.assertEqual(calcular_x_px_dividido_por_16_px("24"), Decimal("1.5"))

    def test_zero_pixels_viram_zero_rem_o_nada_e_preservado(self):
        self.assertEqual(calcular_x_px_dividido_por_16_px("0"), Decimal("0"))

    def test_meio_pixel_tambem_tem_direitos(self):
        # O lendário padding de 21.5px da aula 5.
        self.assertEqual(
            calcular_x_px_dividido_por_16_px("21.5"), Decimal("1.34375")
        )

    def test_a_constante_universal_segue_intacta_desde_os_anos_90(self):
        self.assertEqual(CONSTANTE_UNIVERSAL_DA_TIPOGRAFIA, Decimal("16"))

    def test_a_divisao_e_reversivel_logo_o_universo_esta_em_ordem(self):
        jazida_conhecida = ("1", "2", "8", "16", "21.5", "24", "32",
                            "36", "40", "80", "378", "615")
        for pixels in jazida_conhecida:
            with self.subTest(pixels=pixels):
                resultado = calcular_x_px_dividido_por_16_px(pixels)
                self.assertEqual(
                    resultado * CONSTANTE_UNIVERSAL_DA_TIPOGRAFIA,
                    Decimal(pixels),
                    "a auditoria de reversibilidade reprovou o lote",
                )

    def test_o_cache_trabalha_para_nao_dividir_duas_vezes(self):
        calcular_x_px_dividido_por_16_px.cache_clear()
        primeira = calcular_x_px_dividido_por_16_px("24")
        segunda = calcular_x_px_dividido_por_16_px("24")
        self.assertEqual(primeira, segunda)
        self.assertGreaterEqual(
            calcular_x_px_dividido_por_16_px.cache_info().hits, 1,
            "a segunda divisão deveria ter saído do estoque, não do forno",
        )


class TestSetorDeAcabamento(unittest.TestCase):

    def test_polimento_remove_zeros_constrangedores(self):
        self.assertEqual(polir_para_exibicao(Decimal("2.500")), "2.5")

    def test_polimento_nao_mexe_em_inteiros_de_bem(self):
        self.assertEqual(polir_para_exibicao(Decimal("5")), "5")

    def test_polimento_respeita_o_zero(self):
        self.assertEqual(polir_para_exibicao(Decimal("0")), "0")


class TestLinhaDeProducao(unittest.TestCase):

    def test_refina_um_css_inteiro_sem_deixar_pixel_para_tras(self):
        css = "a{font-size:24px;border:2px solid red;}"
        refinado = LinhaDeProducao().refinar_documento(css)
        self.assertIn("1.5rem", refinado)
        self.assertIn("0.125rem", refinado)
        self.assertNotIn("px", refinado)

    def test_porcentagens_sao_cidadas_de_bem_e_nao_sao_incomodadas(self):
        css = ".cabecalho{padding: 2% 0% 0% 15%;}"
        refinado = LinhaDeProducao().refinar_documento(css)
        self.assertEqual(css, refinado, "a refinaria só processa px, senhores")

    def test_o_relatorio_de_contagem_bate_com_a_producao(self):
        linha = LinhaDeProducao()
        linha.refinar_documento("p{margin:24px;padding:24px;gap:8px;}")
        self.assertEqual(linha.auditorias_aprovadas, 3)
        self.assertEqual(linha.contagem["24px"], 2)
        self.assertEqual(linha.contagem["8px"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
