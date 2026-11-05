import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from plateia import ESPECTADORES, dividir, montar_html, validar  # noqa: E402

BASE = {
    "titulo": "Teste",
    "nicho": "Finanças",
    "frases": [{"n": 1, "inicio": 0, "texto": "Primeira frase."}, {"n": 2, "inicio": 2, "texto": "Segunda frase."}],
    "espectadores": [{"id": i, "saiu_em": None, "motivo": "Ficou.", "comentario": "Ok."} for i in ESPECTADORES],
    "consertos": [{"frase": 1, "problema": "Lento.", "sugestao": "Corte."}],
}


def dados(**mudar):
    d = copy.deepcopy(BASE)
    d.update(mudar)
    return d


class Dividir(unittest.TestCase):
    def test_frases_e_tempo(self):
        f = dividir("Uma frase com cinco palavras. Outra frase aqui!\nTerceira.", ppm=60)
        self.assertEqual([x["n"] for x in f], [1, 2, 3])
        self.assertEqual(f[0]["inicio"], 0)
        self.assertEqual(f[1]["inicio"], 5)

    def test_nao_corta_numero_nem_abreviacao(self):
        f = dividir("Ele pagou R$ 1.200,50 ao Dr. Silva ontem. Fim.")
        self.assertEqual(len(f), 2)
        self.assertIn("Dr. Silva", f[0]["texto"])

    def test_linhas_vazias_e_simbolos(self):
        self.assertEqual(len(dividir("\n\n---\nFrase real.\n\n")), 1)


class Validar(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(validar(dados()), [])

    def test_saida_inexistente(self):
        d = dados()
        d["espectadores"][0]["saiu_em"] = 99
        self.assertTrue(any("saiu_em" in e for e in validar(d)))

    def test_falta_espectador(self):
        d = dados()
        d["espectadores"].pop()
        self.assertTrue(any("Faltam" in e for e in validar(d)))

    def test_espectador_desconhecido_e_repetido(self):
        d = dados()
        d["espectadores"][0]["id"] = "fulano"
        self.assertTrue(any("desconhecido" in e for e in validar(d)))
        d = dados()
        d["espectadores"][1]["id"] = d["espectadores"][0]["id"]
        self.assertTrue(any("repetido" in e for e in validar(d)))

    def test_conserto_invalido(self):
        self.assertTrue(validar(dados(consertos=[{"frase": 9, "problema": "a", "sugestao": "b"}])))

    def test_tipo_errado_nao_quebra(self):
        self.assertTrue(validar([]))
        self.assertTrue(validar({"frases": "x"}))
        self.assertTrue(validar({"frases": [{"n": 1, "texto": "a"}], "espectadores": ["x"]}))


class Html(unittest.TestCase):
    def test_conta_quem_fica(self):
        d = dados()
        d["espectadores"][0]["saiu_em"] = 1
        d["espectadores"][1]["saiu_em"] = 1
        h = montar_html(d)
        self.assertIn("<b>5 de 7</b> ficaram até o fim", h)
        self.assertIn("A frase 1 perdeu mais gente", h)
        self.assertIn("Não são pessoas reais", h)

    def test_todos_ficam(self):
        self.assertIn("<b>7 de 7</b>", montar_html(dados()))

    def test_escapa_html(self):
        d = dados(titulo="<script>alert(1)</script>")
        d["espectadores"][0]["comentario"] = "<img src=x onerror=alert(1)>"
        h = montar_html(d)
        self.assertNotIn("<script>alert", h)
        self.assertNotIn("<img src=x", h)


class Linha(unittest.TestCase):
    def rodar(self, *args):
        return subprocess.run([sys.executable, str(RAIZ / "scripts" / "plateia.py"), *args], capture_output=True, encoding="utf-8")

    def test_relatorio_completo(self):
        with tempfile.TemporaryDirectory() as t:
            j, h = Path(t, "d.json"), Path(t, "m.html")
            j.write_text(json.dumps(BASE, ensure_ascii=False), encoding="utf-8")
            p = self.rodar("relatorio", str(j), str(h))
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertIn("Primeira frase.", h.read_text(encoding="utf-8"))

    def test_erros_sem_traceback(self):
        with tempfile.TemporaryDirectory() as t:
            j = Path(t, "d.json")
            j.write_text("{quebrado", encoding="utf-8")
            for args in (["relatorio", str(j), str(Path(t, "m.html"))], ["dividir", "nao-existe.txt"]):
                p = self.rodar(*args)
                self.assertEqual(p.returncode, 2)
                self.assertNotIn("Traceback", p.stderr)

    def test_todo_id_da_ficha_existe(self):
        ficha = (RAIZ / "espectadores.md").read_text(encoding="utf-8")
        for ident, (nome, _) in ESPECTADORES.items():
            self.assertIn(f"## {ident}: {nome}", ficha)


if __name__ == "__main__":
    unittest.main()
