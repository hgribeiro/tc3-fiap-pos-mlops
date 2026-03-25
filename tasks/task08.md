# Task 08: Adicionar Aba de Storytelling Executivo ao Dashboard

## Objetivo
Criar uma nova aba de **Storytelling** no dashboard, voltada para uma apresentação executiva aos nossos clientes (ex: gestão de uma companhia aérea ou diretoria de um aeroporto). O objetivo é traduzir as análises de Exploratory Data Analysis, Modelagem Supervisionada e Não Supervisionada em insights de negócio claros, acionáveis e diretos.

## Contexto
O cliente nos contratou para entender:
1. Quais são as causas raiz dos atrasos de voos?
2. Existem padrões geográficos ou temporais claros?
3. É possível antecipar/prever os atrasos com base nos dados que eles possuem hoje?

A aba não deve apenas listar gráficos técnicos (como ROC ou Elbow Method), mas deve ter **textos explicativos, conclusões e visualizações amigáveis** baseadas no documento `docs/model_report.md`.

---

## Etapas de Implementação

### 1. Atualizar a Estrutura e Estilo (`dashboard/index.html` e `style.css`)
- [x] Criar um novo link de navegação para a aba "Storytelling" (ou "Insights Executivos").
- [x] Estruturar a página em um formato de "Narrativa" (leitura de cima para baixo), dividindo as conclusões em blocos ou "Cards de Insight".
- [x] Aplicar um design limpo, priorizando a legibilidade de textos e destacando os números e KPIs mais importantes (ex: *Highlights* ou *Big Numbers*).

### 2. Seção Visual: "O Mapa do Atraso" (Características e Temporalidade)
- [x] **Insight de Negócio (Texto):** Explicar como características da própria malha aérea e sazonalidades influenciam a probabilidade de atraso. Destacar que voos programados para o final da tarde e noite têm grande probabilidade de atraso (efeito cascata).
- [x] **Apoio Visual:** Gráficos que resumam a *Feature Importance* (exibindo apenas o impacto prático de variáveis como Horário, Mês e Companhia Aérea, sem o jargão matemático).

### 3. Seção Visual: "Perfis de Malha" (Clusters de Rotas)
- [x] **Insight de Negócio (Texto):** Mostrar a descoberta dos 2 perfis distintos de rotas:
  - **Rotas Curtas Pontuais (Hubs):** Rotas de ~600 milhas, com alta frequência, passando por megahubs (ATL, ORD, DFW) e com uma taxa de atraso alarmante de 34%. O gargalo está na curta distância com alta saturação.
  - **Rotas Longas Pontuais:** Voos cross-country (~1900 milhas), com margem maior de recuperação em voo e por isso com impacto menor em minutos absolutos de atraso no pouso final.
- [x] **Apoio Visual:** Gráficos comparativos lado a lado resumindo os top aeroportos, métricas absolutas de atraso e o percentual de atraso em cada cluster.

### 4. Seção Visual: "Prevenção e Visão de Futuro" (Modelagem Preditiva)
- [x] **Insight de Negócio (Texto):** Explicar a capacidade preditiva do sistema. Explicitar que, usando nossos modelos de IA (ex. o modelo de Gradient Boosting), conseguimos priorizar os alertas focando na otimização da métrica principal (capturar os atrasos mantendo os falsos alarmes sob controle).
- [x] **Conclusão para o Cliente:** Citar que com o histórico puro há um teto de acerto metodológico e fazer a chamada para os **Próximos Passos** (Integração de dados meteorológicos para prever atrasos massivos no dia).

### 5. Integração e Textos
- [x] Transformar os achados da Seção 8 do `docs/model_report.md` (Perguntas Norteadoras) em uma área de Perguntas e Respostas Executivas ou "Takeaways" na parte inferior do dashboard.
- [x] Garantir que o JS carregue os dados estáticos ou componentes de UI de forma leve e responsiva.

---

## Dependências
- Informações consolidadas em `docs/model_report.md`.
- Estrutura base do Dashboard implementada (`index.html`, `style.css`).
- Geração dos JSONs caso a aba utilize gráficos dinâmicos extraídos dos notebooks (opicional dependendo se a narrativa usará imagens estáticas exportadas ou Chart.js dinâmico).

## Critérios de Sucesso

| Requisito | Entregável | Status |
|---|---|---|
| Aba "Storytelling/Insights" acessível no menu | `dashboard/index.html` atualizado | ✅ |
| Conteúdo textual redigido para público não-técnico | Textos baseados no `model_report.md` | ✅ |
| Pelo menos 3 blocos de narrativa (Tempo, Clusters, Modelos)| Elementos visuais bem estruturados | ✅ |
| Funcionalidade e design responsivos | Visualização validada em tela web e mobile | ✅ |
