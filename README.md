<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0B0A09,100:D97757&height=170&section=header&text=Plateia%20Falsa&fontSize=50&fontColor=F3EDE6&fontAlignY=36&desc=Teste%20o%20roteiro%20antes%20de%20gravar%20%C2%B7%20gr%C3%A1tis%20da%20F%C3%A1brica%20de%20Canais&descAlignY=58&descSize=16" width="100%" alt="Plateia Falsa" />

<a href="https://sparks-gamesstudio.github.io/fabrica-de-canais/"><img src="https://sparks-gamesstudio.github.io/fabrica-de-canais/marca/simbolo-1024.png" width="84" alt="Fábrica de Canais" /></a>

**Sete espectadores fictícios leem o seu roteiro e dizem em qual frase iriam embora, por quê e o que comentariam.**

<p>
  <img src="https://img.shields.io/badge/roda%20no%20Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Roda no Claude Code" />
  <img src="https://img.shields.io/badge/gr%C3%A1tis-0B0A09?style=for-the-badge" alt="Grátis" />
  <img src="https://img.shields.io/badge/em%20portugu%C3%AAs-F3EDE6?style=for-the-badge" alt="Em português" />
  <img src="https://img.shields.io/badge/sem%20chave%20de%20API-0B0A09?style=for-the-badge" alt="Sem chave de API" />
</p>

<p>
  <a href="#instalacao"><img src="https://img.shields.io/badge/%E2%AC%87%EF%B8%8F%20Como%20instalar-D97757?style=for-the-badge" alt="Como instalar" /></a>
  <a href="https://sparks-gamesstudio.github.io/fabrica-de-canais/github.html"><img src="https://img.shields.io/badge/Mais%20projetos%20gr%C3%A1tis-0B0A09?style=for-the-badge&logo=github&logoColor=D97757" alt="Mais projetos grátis" /></a>
  <img src="https://img.shields.io/github/stars/sparks-gamesstudio/plateia-falsa?style=for-the-badge&color=D97757&label=%E2%AD%90" alt="Estrelas" />
</p>

</div>

## 👋 O Rebite explica

<img align="right" src="https://raw.githubusercontent.com/sparks-gamesstudio/sparks-gamesstudio/main/assets/rebite/acenar.jpg" width="170" alt="Rebite, o mascote da Fábrica de Canais" />

> Depois de escrever um roteiro, você já não consegue enxergar os defeitos dele. Eu chamo uma plateia inventada para reclamar por você, ainda antes de gravar. Ela não prevê o sucesso do vídeo, mas aponta frases para você olhar de novo.

<br clear="right" />

## 🍿 A plateia

| Espectador | Vai embora quando |
|---|---|
| **Zé do Feed** | A abertura enrola |
| **Marina Sem Som** | A frase depende do áudio ou não cabe em uma legenda |
| **Tiago Cético** | Aparece número sem origem ou promessa exagerada |
| **Dona Lurdes** | Surge um termo técnico sem explicação |
| **Renata do Nicho** | O vídeo repete o básico ou erra um detalhe |
| **Bruno da Treta** | O vídeo fica morno, e o comentário dele mostra a frase mais fácil de atacar |
| **Carla Compartilha** | Ela não imagina para quem enviaria |

Quer outro perfil? As fichas ficam em `espectadores.md`, e os nomes e cores em `scripts/plateia.py`.

## 🗺️ O que você recebe

<img src="docs/mapa.png" width="100%" alt="Mapa da Plateia Falsa, com o roteiro frase por frase e os espectadores que saíram em cada ponto" />

Um mapa em HTML ([exemplo](exemplos/mapa-exemplo.html)) que abre no navegador, com:

- o roteiro frase por frase, mais quente onde a plateia saiu;
- quantos espectadores ainda estão presentes em cada ponto;
- o motivo e o comentário de cada espectador;
- até 3 consertos, do mais importante para o menos importante.

<a id="instalacao"></a>

## ⬇️ Como instalar

Precisa do [Claude Code](https://claude.com/claude-code) e do Python 3.10 ou mais novo. Não há pacotes para instalar.

```bash
git clone https://github.com/sparks-gamesstudio/plateia-falsa.git $HOME/.claude/skills/plateia-falsa
```

Depois, em uma sessão nova do Claude Code, peça:

```text
/plateia-falsa testa o roteiro do arquivo meu-roteiro.txt
```

Para testar sem um roteiro seu, use o `exemplos/roteiro.txt`, que tem defeitos de propósito.

<table>
<tr>
<td width="110"><img src="https://raw.githubusercontent.com/sparks-gamesstudio/sparks-gamesstudio/main/assets/rebite/pensar.jpg" width="90" alt="Rebite pensando" /></td>
<td>

**Aviso honesto:** é uma simulação feita por IA, com personagens inventados. Não são pessoas reais, não mede retenção e não prevê views. Duas rodadas podem dar respostas diferentes. Use para achar frases fracas e decida com a sua cabeça.

</td>
</tr>
</table>

## 🔒 Seus dados

O mapa é gerado no seu computador e não usa rede. O roteiro passa pelo Claude Code, como qualquer texto que você envia a ele.

## 🧪 Para quem quer mexer

```bash
python -m unittest discover -s tests -v
```

---

<div align="center">

<a href="https://sparks-gamesstudio.github.io/fabrica-de-canais/"><img src="https://sparks-gamesstudio.github.io/fabrica-de-canais/marca/simbolo-1024.png" width="56" alt="Fábrica de Canais" /></a>

Feito pela **[Fábrica de Canais](https://sparks-gamesstudio.github.io/fabrica-de-canais/)**, skills de Claude Code para canais de vídeo no piloto automático.

<a href="https://instagram.com/afabricadecanais"><img src="https://img.shields.io/badge/@afabricadecanais-E4405F?style=flat-square&logo=instagram&logoColor=white" alt="Instagram" /></a>
<a href="https://github.com/sparks-gamesstudio"><img src="https://img.shields.io/badge/mais%20projetos-0B0A09?style=flat-square&logo=github&logoColor=D97757" alt="Mais projetos" /></a>

<sub>Licença MIT · use, modifique e compartilhe. Se ajudou, deixa uma ⭐</sub>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:D97757,100:0B0A09&height=90&section=footer" width="100%" alt="" />

</div>
