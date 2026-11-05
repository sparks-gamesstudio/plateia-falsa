---
name: plateia-falsa
description: Coloca um roteiro de vídeo curto na frente de 7 espectadores fictícios, que dizem em qual frase iriam embora, por quê e qual comentário deixariam, e gera um mapa em HTML. Use quando pedirem "testa meu roteiro", "plateia falsa", "onde as pessoas iam sair" ou antes de gravar. Não prevê views.
---

# Plateia Falsa

`<skill>` é a pasta desta skill. As fichas dos espectadores estão em `<skill>/espectadores.md`: leia antes de começar.

## 1. Preparar
Você precisa do roteiro e de uma frase sobre o nicho e o público. Se faltar o nicho, deduza do texto e diga o que deduziu. Só pergunte se não houver roteiro.

Salve o roteiro em um arquivo temporário, se ele veio colado, e numere as frases:
```
python <skill>/scripts/plateia.py dividir <roteiro>
```
Use exatamente os números e textos que esse comando devolver.

## 2. Fazer cada espectador assistir
Escreva como cada um dos 7 reage, um de cada vez, seguindo a própria ficha:
- cada um assiste do início e sai na primeira frase em que a ficha mandaria sair. Se ficar até o fim, `saiu_em` é `null`;
- o motivo precisa citar palavras reais da frase. Se não houver motivo concreto, a pessoa fica;
- não force discordância, nem faça todo mundo sair no mesmo lugar para ficar mais dramático;
- não invente dados sobre o canal, o público ou a plataforma.

## 3. Montar o relatório
Grave um JSON neste formato:
```json
{
  "titulo": "nome do roteiro",
  "nicho": "uma frase",
  "frases": [{"n": 1, "inicio": 0, "texto": "..."}],
  "espectadores": [
    {"id": "ze", "saiu_em": 1, "motivo": "...", "comentario": "..."}
  ],
  "consertos": [{"frase": 1, "problema": "...", "sugestao": "..."}]
}
```
- `frases` é copiado do comando `dividir`.
- `espectadores` tem os 7, com os ids da ficha. `comentario` é o que a pessoa escreveria, em uma linha.
- `consertos` tem até 3 itens, do mais importante para o menos importante. Cada `sugestao` é uma frase pronta, que não acrescenta fato novo ao roteiro.

Depois rode:
```
python <skill>/scripts/plateia.py relatorio <dados.json> <mapa.html>
```
Se o comando acusar erro no JSON, corrija e rode de novo.

## 4. Entregar
Diga onde está o mapa e resuma em poucas linhas: em que frase a plateia mais saiu, por quê e os consertos.

Termine deixando claro que é uma simulação feita por IA para revelar pontos fracos. Ela não mede pessoas reais e não prevê views, retenção nem viralização. Não dê nota de potencial viral.
