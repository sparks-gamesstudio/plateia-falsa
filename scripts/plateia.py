#!/usr/bin/env python3
"""Divide um roteiro em frases numeradas e monta o mapa da Plateia Falsa em HTML.

python plateia.py dividir roteiro.txt [--ppm 150]
python plateia.py relatorio dados.json mapa.html
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ESPECTADORES = {
    "ze": ("Zé do Feed", "#D97757"),
    "marina": ("Marina Sem Som", "#7FB3D5"),
    "tiago": ("Tiago Cético", "#C39BD3"),
    "lurdes": ("Dona Lurdes", "#F7DC6F"),
    "renata": ("Renata do Nicho", "#76D7C4"),
    "bruno": ("Bruno da Treta", "#EC7063"),
    "carla": ("Carla Compartilha", "#F5B7B1"),
}
PALAVRA = re.compile(r"[^\W_]+(?:-[^\W_]+)*")


class DadosInvalidos(ValueError):
    pass


def dividir(texto: str, ppm: int = 150) -> list[dict]:
    frases: list[dict] = []
    decorrido = 0.0
    for bloco in texto.splitlines():
        # Não corta em "3,5", "R$ 1.200" nem em abreviações como "Dr."
        partes = re.split(r"(?<=[.!?…])[\"”']?\s+(?=[\"“'A-ZÀ-Ú0-9])", bloco.strip())
        unidas: list[str] = []
        for p in partes:
            if unidas and re.search(r"\b(?:Dr|Dra|Sr|Sra|Prof|Profa|Av|Ex)\.$", unidas[-1]):
                unidas[-1] += " " + p
            else:
                unidas.append(p)
        for p in unidas:
            if not PALAVRA.search(p):
                continue
            frases.append({"n": len(frases) + 1, "inicio": round(decorrido, 1), "texto": p})
            decorrido += len(PALAVRA.findall(p)) / ppm * 60
    return frases


def validar(d: object) -> list[str]:
    if not isinstance(d, dict):
        return ["O arquivo precisa ser um objeto JSON."]
    erros: list[str] = []
    frases = d.get("frases")
    if not isinstance(frases, list) or not frases:
        return ['"frases" precisa ser uma lista com pelo menos uma frase.']
    numeros: set[int] = set()
    for i, f in enumerate(frases, 1):
        if not isinstance(f, dict) or not isinstance(f.get("n"), int) or not isinstance(f.get("texto"), str):
            erros.append(f'A frase {i} precisa de "n" (inteiro) e "texto".')
        else:
            numeros.add(f["n"])

    esp = d.get("espectadores")
    if not isinstance(esp, list):
        return erros + ['"espectadores" precisa ser uma lista.']
    vistos: set[str] = set()
    for e in esp:
        if not isinstance(e, dict):
            erros.append("Cada espectador precisa ser um objeto.")
            continue
        ident = e.get("id")
        if ident not in ESPECTADORES:
            erros.append(f'Espectador desconhecido: {ident!r}. Use: {", ".join(ESPECTADORES)}.')
            continue
        if ident in vistos:
            erros.append(f"Espectador repetido: {ident}.")
        vistos.add(ident)
        saiu = e.get("saiu_em")
        if saiu is not None and saiu not in numeros:
            erros.append(f'{ident}: "saiu_em" = {saiu!r} não é o número de uma frase (use null se ficou até o fim).')
        if not isinstance(e.get("motivo"), str) or not e["motivo"].strip():
            erros.append(f'{ident}: falta "motivo".')
        if not isinstance(e.get("comentario"), str) or not e["comentario"].strip():
            erros.append(f'{ident}: falta "comentario".')
    faltando = set(ESPECTADORES) - vistos
    if faltando:
        erros.append(f'Faltam espectadores: {", ".join(sorted(faltando))}.')

    consertos = d.get("consertos", [])
    if not isinstance(consertos, list):
        erros.append('"consertos" precisa ser uma lista.')
    else:
        for c in consertos:
            if not isinstance(c, dict) or c.get("frase") not in numeros or not c.get("problema") or not c.get("sugestao"):
                erros.append('Cada conserto precisa de "frase" (um número de frase), "problema" e "sugestao".')
    return erros


def _tempo(segundos: object) -> str:
    if not isinstance(segundos, (int, float)):
        return ""
    return f"{int(segundos) // 60}:{int(segundos) % 60:02d}"


CSS = """
:root{color-scheme:dark}*{box-sizing:border-box}
body{margin:0;background:#0B0A09;color:#F3EDE6;font:16px/1.5 system-ui,'Segoe UI',sans-serif}
main{max-width:920px;margin:auto;padding:32px 20px 60px}
h1{font-size:30px;margin:0 0 4px}h2{font-size:20px;margin:36px 0 12px}
.nicho,.aviso,.tempo,.cont{color:#A99F94}.aviso{border:1px solid #3a322b;border-radius:10px;padding:10px 14px;font-size:14px;margin:18px 0}
.resumo{font-size:18px;margin:14px 0}.resumo b{color:#D97757}
.linha{display:grid;grid-template-columns:44px 1fr 72px;gap:12px;padding:10px 12px;border-radius:10px;margin-bottom:6px;background:linear-gradient(90deg,rgba(217,119,87,var(--calor)),rgba(217,119,87,0) 85%),#171411}
.tempo{font-size:13px;padding-top:2px}.cont{font-size:13px;text-align:right;padding-top:2px;white-space:nowrap}
.saidas{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}.saida{border-radius:99px;padding:1px 10px;font-size:13px;color:#0B0A09;font-weight:600}
.cartoes{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}
.cartao{background:#171411;border-radius:12px;padding:14px;border-top:3px solid var(--cor)}.cartao h3{margin:0 0 2px;font-size:16px}
.onde{font-size:13px;color:#A99F94;margin-bottom:8px}.cartao p{margin:6px 0;font-size:15px}.coment{font-style:italic;color:#D9CFC4}
.conserto{background:#171411;border-radius:12px;padding:14px;margin-bottom:10px}.conserto b{color:#D97757}.conserto p{margin:6px 0}
"""


def montar_html(d: dict) -> str:
    e = html.escape
    frases = d["frases"]
    total = len(d["espectadores"])
    por_id = {x["id"]: x for x in d["espectadores"]}
    saidas: dict[int, list[str]] = {}
    for x in d["espectadores"]:
        if x.get("saiu_em") is not None:
            saidas.setdefault(x["saiu_em"], []).append(x["id"])

    linhas = []
    presentes = total
    for f in frases:
        saindo = saidas.get(f["n"], [])
        calor = round(len(saindo) / max(total, 1) * 1.6, 2)
        presentes -= len(saindo)
        selos = "".join(
            f'<span class="saida" style="background:{ESPECTADORES[i][1]}">{e(ESPECTADORES[i][0])} saiu</span>' for i in saindo
        )
        linhas.append(
            f'<div class="linha" style="--calor:{calor}"><div class="tempo">{e(_tempo(f.get("inicio")))}</div>'
            f'<div>{e(f["texto"])}{f"<div class=saidas>{selos}</div>" if selos else ""}</div>'
            f'<div class="cont">{presentes} de {total}</div></div>'
        )

    cartoes = []
    for ident, (nome, cor) in ESPECTADORES.items():
        x = por_id[ident]
        onde = f'Saiu na frase {x["saiu_em"]}' if x.get("saiu_em") is not None else "Ficou até o fim"
        cartoes.append(
            f'<div class="cartao" style="--cor:{cor}"><h3>{e(nome)}</h3><div class="onde">{onde}</div>'
            f'<p>{e(x["motivo"])}</p><p class="coment">“{e(x["comentario"])}”</p></div>'
        )

    consertos = "".join(
        f'<div class="conserto"><b>Frase {c["frase"]}:</b> {e(c["problema"])}<p>{e(c["sugestao"])}</p></div>'
        for c in d.get("consertos", [])
    )
    pior = max(saidas, key=lambda n: len(saidas[n]), default=None)
    resumo = f"<b>{presentes} de {total}</b> ficaram até o fim."
    if pior is not None:
        resumo += f" A frase {pior} perdeu mais gente: <b>{len(saidas[pior])}</b>."

    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Plateia Falsa: {e(str(d.get("titulo", "roteiro")))}</title><style>{CSS}</style></head><body><main>
<h1>{e(str(d.get("titulo", "Roteiro")))}</h1><div class="nicho">{e(str(d.get("nicho", "")))}</div>
<p class="resumo">{resumo}</p>
<div class="aviso">Simulação feita por IA com 7 personagens fictícios. Não são pessoas reais e não prevê views nem retenção.</div>
<h2>O roteiro, frase por frase</h2>{"".join(linhas)}
<h2>Os espectadores</h2><div class="cartoes">{"".join(cartoes)}</div>
{f"<h2>O que consertar primeiro</h2>{consertos}" if consertos else ""}
</main></body></html>
"""


def ler(caminho: str) -> str:
    dados = Path(caminho).read_bytes()
    try:
        return dados.decode("utf-8-sig")
    except UnicodeDecodeError:
        return dados.decode("cp1252")


def main(argv: list[str] | None = None) -> int:
    for fluxo in (sys.stdout, sys.stderr):
        if hasattr(fluxo, "reconfigure"):
            fluxo.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Plateia Falsa")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("dividir", help="numera as frases do roteiro")
    a.add_argument("roteiro")
    a.add_argument("--ppm", type=int, default=150)
    b = sub.add_parser("relatorio", help="gera o mapa em HTML")
    b.add_argument("dados")
    b.add_argument("saida")
    args = p.parse_args(argv)

    try:
        if args.cmd == "dividir":
            if args.ppm <= 0:
                p.error("--ppm precisa ser maior que zero")
            print(json.dumps(dividir(ler(args.roteiro), args.ppm), ensure_ascii=False, indent=2))
            return 0
        try:
            dados = json.loads(ler(args.dados))
        except json.JSONDecodeError as erro:
            print(f"JSON inválido na linha {erro.lineno}: {erro.msg}", file=sys.stderr)
            return 2
        erros = validar(dados)
        if erros:
            print("\n".join(erros), file=sys.stderr)
            return 2
        Path(args.saida).write_text(montar_html(dados), encoding="utf-8")
        print(f"Mapa salvo em {args.saida}")
        return 0
    except OSError as erro:
        print(f"Erro ao abrir o arquivo: {erro.strerror} ({erro.filename})", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
