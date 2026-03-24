# Task 01: Índice de Subtasks - Análise Exploratória de Dados (EDA)

**Projeto:** Flight Delay Prediction - Tech Challenge 3 (FIAP MLOps)  
**Status Geral:** 📋 Planejamento Concluído - Pronto para Execução  
**Data de Criação:** 2026-03-23  

---

## 📊 Visão Geral da Task

| Aspecto | Detalle |
|---------|---------|
| **Objetivo** | Análise exploratória completa do dataset de voos |
| **Datasets** | airlines.csv (~359B), airports.csv (~24KB), flights.csv (~592MB) |
| **Total de Subtasks** | **9 subtasks** em 4 fases |
| **Tempo Estimado** | **15-16 horas** |
| **Saídas Esperadas** | 15-20 visualizações + Relatório + JSON summary |
| **Critério de Sucesso** | Todos os subtasks completados com ✅ status |

---

## 🗂️ Estrutura de Fases

```
FASE 1: SETUP & CARREGAMENTO (1.5h)
├── 1.1: Preparação do Ambiente ......................... 30 min
└── 1.2: Carregamento Otimizado dos dados ........... 60 min

FASE 2: EXPLORAÇÃO & VALIDAÇÃO (5.5h)
├── 2.1: Análise Descritiva Completa .................. 90 min
├── 2.2: Validação de Qualidade dos dados ......... 120 min
└── 2.3: Tratamento & Limpeza de dados ............ 120 min

FASE 3: VISUALIZAÇÕES & INSIGHTS (5.5h)
├── 3.1: Visualizações Univariadas .................... 90 min
├── 3.2: Visualizações Bivariadas & Correlações .. 120 min
└── 3.3: Análise de Padrões & Insights ............ 120 min

FASE 4: VALIDAÇÃO & DOCUMENTAÇÃO (3h)
├── 4.1: Testes & Validação ............................ 60 min
└── 4.2: Relatório Final & Documentação ........... 120 min
```

---

## 📑 Lista de Subtasks

### FASE 1️⃣: SETUP & CARREGAMENTO

| # | Subtask | Status | Tempo | Link |
|---|---------|--------|-------|------|
| 1.1 | Preparação do Ambiente | ❌ Não iniciada | 30min | [task01_subtask_1_1.md](task01_subtask_1_1.md) |
| 1.2 | Carregamento Otimizado dos Dados | ❌ Não iniciada | 60min | [task01_subtask_1_2.md](task01_subtask_1_2.md) |

**Objetivos:**
- ✅ Validar Python/libs instaladas
- ✅ Criar estrutura de diretórios
- ✅ Carregar 3 datasets com otimização

---

### FASE 2️⃣: EXPLORAÇÃO & VALIDAÇÃO

| # | Subtask | Status | Tempo | Link |
|---|---------|--------|-------|------|
| 2.1 | Análise Descritiva Completa | ❌ Não iniciada | 90min | [task01_subtask_2_1.md](task01_subtask_2_1.md) |
| 2.2 | Validação de Qualidade dos Dados | ❌ Não iniciada | 120min | [task01_subtask_2_2.md](task01_subtask_2_2.md) |
| 2.3 | Tratamento & Limpeza de Dados | ❌ Não iniciada | 120min | [task01_subtask_2_3.md](task01_subtask_2_3.md) |

**Objetivos:**
- ✅ Estatísticas descritivas (mean, median, std, etc)
- ✅ Validar qualidade (missing, duplicatas, outliers)
- ✅ Limpar dados e criar variáveis derivadas

---

### FASE 3️⃣: VISUALIZAÇÕES & INSIGHTS

| # | Subtask | Status | Tempo | Link |
|---|---------|--------|-------|------|
| 3.1 | Visualizações Univariadas | ❌ Não iniciada | 90min | [task01_subtask_3_1.md](task01_subtask_3_1.md) |
| 3.2 | Visualizações Bivariadas & Correlações | ❌ Não iniciada | 120min | [task01_subtask_3_2.md](task01_subtask_3_2.md) |
| 3.3 | Análise de Padrões & Insights | ❌ Não iniciada | 120min | [task01_subtask_3_3.md](task01_subtask_3_3.md) |

**Objetivos:**
- ✅ 8-10 histogramas, boxplots, bar charts
- ✅ 8-10 scatter plots, heatmap correlação
- ✅ 5-7 insights acionáveis

---

### FASE 4️⃣: VALIDAÇÃO & DOCUMENTAÇÃO

| # | Subtask | Status | Tempo | Link |
|---|---------|--------|-------|------|
| 4.1 | Testes & Validação | ❌ Não iniciada | 60min | [task01_subtask_4_1.md](task01_subtask_4_1.md) |
| 4.2 | Relatório Final & Documentação | ❌ Não iniciada | 120min | [task01_subtask_4_2.md](task01_subtask_4_2.md) |

**Objetivos:**
- ✅ Validar código fim-a-fim, reproducibilidade
- ✅ Criar relatório markdown (2000+ palavras)
- ✅ JSON summary concentrado

---

## 🚀 Como Usar Este Índice

### 1. **Leitura Sequencial** (Recomendado)
Execute as subtasks **na ordem** listada acima. Cada uma depende da anterior.

### 2. **Rastreamento de Progresso**
Atualize o status de cada subtask:
- ❌ = Não iniciada
- 🔄 = Em progresso
- ✅ = Concluída

Marque a data de conclusão quando terminar cada uma.

### 3. **Acesso Rápido**
Abra diretamente o arquivo da subtask que está trabalhando:
```bash
# Exemplo
cat tasks/task01_subtask_2_3.md
```

---

## ✅ Critérios de Completude

Para considerar **TASK 01 COMPLETA**, todas as subtasks devem ter:

### Por Subtask
- ✅ **Status:** ✅ (Concluída)
- ✅ **Checklist:** 100% items marcados
- ✅ **Critérios de Aceitação:** Todos validados
- ✅ **Changelog:** Atualizado
- ✅ **Outputs:** Salvos no local correto

### No Final (Subtask 4.2)
- ✅ Relatório em `docs/eda_report.md` (2000+ palabras)
- ✅ JSON em `data/processed/eda_summary.json`
- ✅ 20+ visualizações em `docs/eda_plots/`
- ✅ Dados limpos em `data/processed/flights_cleaned.csv`
- ✅ README com instruções

---

## 📈 Métodos de Validação

### Checklist de Outputs
```bash
# Verificar files
ls -lh data/processed/
ls -lh docs/eda_plots/ | wc -l  # Deve ter ~21 arquivos

# Verificar tamanho dos arquivos
du -sh data/processed/
du -sh docs/eda_plots/
```

### Checklist de Reprodutibilidade
```bash
# Executar 2 vezes - deve dar mesmos resultados
python src/01_eda.py > log1.txt
python src/01_eda.py > log2.txt
diff log1.txt log2.txt  # Deve estar vazio ou idêntico
```

### Checklist de Qualidade
- [ ] Código sem erros (executa clean)
- [ ] Variáveis com nomes descritivos
- [ ] Comentários explicam "por quê", não "o quê"
- [ ] Random seed = 42 configurado
- [ ] Tempo de execução < 10 minutos

---

## 🎯 Estimativa de Conclusão

| Fase | Subtasks | Tempo | Data Prevista |
|------|----------|-------|-----------------|
| 1 | 1.1 + 1.2 | 1.5h | 2026-03-23 |
| 2 | 2.1 + 2.2 + 2.3 | 5.5h | 2026-03-24 |
| 3 | 3.1 + 3.2 + 3.3 | 5.5h | 2026-03-25 |
| 4 | 4.1 + 4.2 | 3h | 2026-03-25 |
| **TOTAL** | **9 subtasks** | **15-16h** | **2026-03-25** |

---

## 📚 Instruções Importantes

### ⚠️ ORDEM CRÍTICA
**NÃO PULE SUBTASKS.** Cada fase depende da anterior:
- Não pode fazer Fase 2 sem Fase 1 ✅
- Não pode fazer Fase 3 sem Fase 2 ✅
- Não pode fazer Fase 4 sem Fase 3 ✅

### 💾 SALVAGUARDAR OUTPUTS
Sempre salve outputs no local correto:
```
docs/eda_plots/        ← Visualizações (.png)
data/processed/        ← Dados limpos (.csv, .json)
docs/eda_report.md    ← Relatório final
```

### 📝 DOCUMENTAÇÃO
Cada arquivo de subtask tem:
1. **Checklist**: Items para validar
2. **Critérios de Aceitação**: Quando está pronto
3. **Changelog**: Para rastrear mudanças
4. **Template**: Exemplos de código

---

## 🔧 Comandos Úteis

```bash
# Ver status de uma subtask
cat tasks/task01_subtask_X_Y.md | grep -A 10 "Status"

# Contar arquivos gerados
find docs/eda_plots -name "*.png" | wc -l

# Validar JSON
python -m json.tool data/processed/eda_summary.json

# Ver últimas mudanças (changelog)
git log --oneline tasks/task01_subtask_*
```

---

## 📞 Quando Está Preso?

Cada subtask tem uma seção **"Possíveis Bloqueadores"**:
1. Identifique o bloqueador nessa lista
2. Leia a solução proposta
3. Implemente a solução
4. Documente o que foi corrigido no **Changelog**

Exemplo de documentação:
```
## Changelog

| Data | Versão | Mudança | Autor |
|------|--------|---------|-------|
| 2026-03-23 | v1.0 | Criação inicial | Copilot |
| 2026-03-23 | v1.1 | Bloqueador: Memory overflow - Solução: usar amostra + dtypes otimizados | Hugo |
```

---

## 🎓 Modelo de Progresso

```
[████████░░░░░░░░░░░░░░░░] 33% - Fase 1 & 2 completas
[████████████████████░░░░] 83% - Fase 3 completa
[████████████████████████] 100% - Pronto! ✅
```

Atualize este visual conforme progride.

---

## 🏁 Próximos Passos Após Task 01

Depois de completar esta task, você estará pronto para:
- ✅ **Task 02**: Feature Engineering
- ✅ **Task 03**: Modelagem Supervisionada
- ✅ **Task 04**: Modelagem Não-supervisionada
- ✅ **Task 05**: Relatório Final

---

## 📎 Arquivos Relacionados

- **Original Task**: [task01.md](task01.md)
- **Subtasks Details**: [task01_subtasks.md](task01_subtasks.md)
- **Project Instructions**: [/copilot-instructions.md](../copilot-instructions.md)
- **README**: [../README.md](../README.md)

---

## ✍️ Notas de Rodapé

- **Prioridade**: ALTA - Representa 90% da nota final
- **Trabalho em Equipe**: Delegue subtasks diferentes para membros da equipe
- **Versão deste Índice**: 1.0 (2026-03-23)
- **Última Atualização**: 2026-03-23

---

**Boa sorte! 🚀 Comece pela Subtask 1.1 quando estiver pronto.**

