---
name: frontend-dashboard
description: "Use quando alterar o dashboard web estático (app.js, index.html, style.css) para manter escopo, contratos de dados e consistência visual."
applyTo: "dashboard/{app.js,index.html,style.css}"
---

# Frontend Dashboard (TC3)

## Escopo

- Limite alterações aos arquivos `dashboard/app.js`, `dashboard/index.html` e `dashboard/style.css`.
- Evite criar páginas/rotas/frameworks/build step; só faça isso quando houver solicitação explícita ou necessidade técnica clara.
- Manter o dashboard estático servido por `npx -y serve . -l 3847`.

## Contrato de dados

- Consumir apenas JSONs em `data/processed/dashboard/`.
- Não renomear chaves JSON já usadas sem atualizar todos os pontos de consumo em `app.js`.
- Tratar ausência de arquivo/chave com fallback visual simples (mensagem curta no card/gráfico), sem quebrar a página.

## JavaScript (`app.js`)

- Preferir funções pequenas e puras para transformação de dados.
- Evitar duplicação: extrair utilitários para formatação de número, percentual e labels temporais.
- Evitar dependências externas novas quando JavaScript nativo resolver bem; se necessário, manter a escolha mínima e justificada.
- Preservar ordem de inicialização: carregar dados, validar, renderizar KPIs e gráficos.

## HTML (`index.html`)

- Manter semântica básica (`header`, `main`, `section`) e hierarquia de títulos consistente.
- Priorizar o escopo solicitado; componentes extras (ex.: filtros, modais, abas) só quando agregarem valor direto à demanda atual.
- Garantir que IDs/classes usados pelo `app.js` permaneçam estáveis após mudanças estruturais.

## CSS (`style.css`)

- Reaproveitar tokens/variáveis e padrões já existentes antes de criar novos estilos.
- Evitar hardcode de cores arbitrárias quando já houver variáveis equivalentes.
- Preservar responsividade existente; alterações de layout devem funcionar em desktop e mobile.
- Manter estilos simples por padrão; animações/efeitos são permitidos quando forem discretos e alinhados ao objetivo da tarefa.

## Qualidade e validação

- Após alterações de frontend, validar carregamento local em `http://localhost:3847/dashboard/`.
- Se houver quebra de renderização por dados, corrigir no `app.js` sem alterar contrato dos artefatos gerados pelos scripts `src/`.
- Manter mudanças mínimas e focadas na demanda do usuário.