/**
 * Flight Delay EDA Dashboard — App Logic
 * Loads JSON data and renders interactive Chart.js charts
 */

const DATA_BASE = '../data/processed/dashboard';

// ===== Chart.js Global Config =====
Chart.defaults.color = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255,255,255,0.06)';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.pointStyle = 'circle';
Chart.defaults.plugins.legend.labels.padding = 16;
Chart.defaults.animation.duration = 800;

// Color palette
const COLORS = {
    blue: '#3b82f6',
    cyan: '#06b6d4',
    purple: '#8b5cf6',
    pink: '#ec4899',
    orange: '#f97316',
    green: '#10b981',
    red: '#ef4444',
    yellow: '#eab308',
    teal: '#14b8a6',
    indigo: '#6366f1',
    rose: '#f43f5e',
    amber: '#f59e0b',
    lime: '#84cc16',
    sky: '#0ea5e9',
};

const PALETTE = [
    COLORS.blue, COLORS.cyan, COLORS.purple, COLORS.pink,
    COLORS.orange, COLORS.green, COLORS.red, COLORS.yellow,
    COLORS.teal, COLORS.indigo, COLORS.rose, COLORS.amber,
    COLORS.lime, COLORS.sky,
];

const CATEGORY_COLORS = {
    'On Time': '#10b981',
    'Minor Delay': '#eab308',
    'Moderate Delay': '#f97316',
    'Major Delay': '#ef4444',
    'Unknown': '#64748b',
};

// ===== Utility Functions =====
function formatNumber(n) {
    if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
    if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
    return n.toLocaleString('pt-BR');
}

async function loadJSON(filename) {
    const res = await fetch(`${DATA_BASE}/${filename}`);
    if (!res.ok) throw new Error(`Failed to load ${filename}`);
    return res.json();
}

function alpha(hex, a) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r},${g},${b},${a})`;
}

function createGradient(ctx, color1, color2, vertical = true) {
    const gradient = vertical
        ? ctx.createLinearGradient(0, 0, 0, ctx.canvas.height)
        : ctx.createLinearGradient(0, 0, ctx.canvas.width, 0);
    gradient.addColorStop(0, alpha(color1, 0.8));
    gradient.addColorStop(1, alpha(color2, 0.1));
    return gradient;
}

// ===== KPI Cards =====
async function renderKPIs() {
    const data = await loadJSON('dashboard_kpis.json');
    const grid = document.getElementById('kpi-grid');

    const kpis = [
        { icon: '✈️', value: formatNumber(data.total_flights), label: 'Total de Voos' },
        { icon: '⏱️', value: data.delay_rate + '%', label: 'Taxa de Atraso' },
        { icon: '🕐', value: data.avg_delay_minutes + ' min', label: 'Atraso Médio' },
        { icon: '❌', value: data.cancellation_rate + '%', label: 'Cancelamentos' },
        { icon: '↪️', value: data.diversion_rate + '%', label: 'Desvios' },
        { icon: '🏢', value: data.total_airlines, label: 'Companhias' },
        { icon: '🛫', value: formatNumber(data.total_airports), label: 'Aeroportos' },
        { icon: '📏', value: formatNumber(data.avg_distance) + ' mi', label: 'Distância Média' },
        { icon: '📊', value: data.median_delay + ' min', label: 'Mediana do Atraso' },
    ];

    grid.innerHTML = kpis.map((kpi, i) => `
        <div class="kpi-card" style="animation-delay: ${i * 0.05}s">
            <div class="kpi-icon">${kpi.icon}</div>
            <div class="kpi-value">${kpi.value}</div>
            <div class="kpi-label">${kpi.label}</div>
        </div>
    `).join('');
}

// ===== Delay Distribution =====
async function renderDelayDistribution() {
    const data = await loadJSON('dashboard_delay_distribution.json');

    // Histogram
    const histCtx = document.getElementById('histogram-chart').getContext('2d');
    const gradient = createGradient(histCtx, COLORS.blue, COLORS.cyan);

    new Chart(histCtx, {
        type: 'bar',
        data: {
            labels: data.histogram.bin_edges.slice(0, -1).map(v => v + ''),
            datasets: [{
                label: 'Frequência',
                data: data.histogram.values,
                backgroundColor: gradient,
                borderColor: COLORS.blue,
                borderWidth: 0,
                borderRadius: 2,
                barPercentage: 1.0,
                categoryPercentage: 1.0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        title: (items) => {
                            const idx = items[0].dataIndex;
                            return `${data.histogram.bin_edges[idx]} a ${data.histogram.bin_edges[idx + 1]} min`;
                        },
                        label: (item) => `${item.raw.toLocaleString('pt-BR')} voos`
                    }
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Atraso (minutos)' },
                    ticks: { maxTicksLimit: 12 }
                },
                y: {
                    title: { display: true, text: 'Frequência' },
                    ticks: { callback: v => formatNumber(v) }
                }
            }
        }
    });

    // Categories Pie
    const catCtx = document.getElementById('categories-chart').getContext('2d');
    const catColors = data.categories.labels.map(l => CATEGORY_COLORS[l] || '#64748b');

    new Chart(catCtx, {
        type: 'doughnut',
        data: {
            labels: data.categories.labels,
            datasets: [{
                data: data.categories.values,
                backgroundColor: catColors.map(c => alpha(c, 0.85)),
                borderColor: catColors,
                borderWidth: 2,
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '55%',
            plugins: {
                legend: { position: 'bottom', labels: { font: { size: 11 } } },
                tooltip: {
                    callbacks: {
                        label: (item) => {
                            const total = item.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = ((item.raw / total) * 100).toFixed(1);
                            return ` ${item.label}: ${item.raw.toLocaleString('pt-BR')} (${pct}%)`;
                        }
                    }
                }
            }
        }
    });

    // Stats below pie
    const statsGrid = document.getElementById('delay-stats');
    const s = data.stats;
    const stats = [
        { label: 'Média', value: s.mean + ' min' },
        { label: 'Mediana', value: s.median + ' min' },
        { label: 'Desvio Padrão', value: s.std + ' min' },
        { label: 'Q25–Q75', value: `${s.q25} — ${s.q75}` },
    ];
    statsGrid.innerHTML = stats.map(st => `
        <div class="stat-item">
            <span class="stat-label">${st.label}</span>
            <span class="stat-value">${st.value}</span>
        </div>
    `).join('');
}

// ===== Temporal Analysis =====
async function renderTemporal() {
    const data = await loadJSON('dashboard_temporal.json');

    // Monthly Delay
    const monthlyCtx = document.getElementById('monthly-delay-chart').getContext('2d');
    const monthlyGrad = createGradient(monthlyCtx, COLORS.blue, COLORS.blue);

    new Chart(monthlyCtx, {
        type: 'line',
        data: {
            labels: data.monthly.labels,
            datasets: [{
                label: 'Atraso Médio (min)',
                data: data.monthly.avg_delay,
                borderColor: COLORS.blue,
                backgroundColor: monthlyGrad,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: COLORS.blue,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { title: { display: true, text: 'Atraso (min)' } }
            }
        }
    });

    // Monthly Rate
    const rateCtx = document.getElementById('monthly-rate-chart').getContext('2d');
    const rateGrad = createGradient(rateCtx, COLORS.red, COLORS.red);

    new Chart(rateCtx, {
        type: 'line',
        data: {
            labels: data.monthly.labels,
            datasets: [{
                label: 'Taxa de Atraso (%)',
                data: data.monthly.delay_rate,
                borderColor: COLORS.red,
                backgroundColor: rateGrad,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: COLORS.red,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { title: { display: true, text: 'Taxa (%)' } }
            }
        }
    });

    // Day of Week
    const dowCtx = document.getElementById('dow-chart').getContext('2d');
    new Chart(dowCtx, {
        type: 'bar',
        data: {
            labels: data.day_of_week.labels,
            datasets: [{
                label: 'Atraso Médio (min)',
                data: data.day_of_week.avg_delay,
                backgroundColor: data.day_of_week.avg_delay.map((v, i) =>
                    alpha(PALETTE[i % PALETTE.length], 0.75)
                ),
                borderColor: data.day_of_week.avg_delay.map((v, i) =>
                    PALETTE[i % PALETTE.length]
                ),
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { title: { display: true, text: 'Atraso (min)' }, beginAtZero: true }
            }
        }
    });

    // Period
    const periodCtx = document.getElementById('period-chart').getContext('2d');
    const periodColors = {
        'Morning': COLORS.yellow,
        'Afternoon': COLORS.orange,
        'Evening': COLORS.purple,
        'Night': COLORS.indigo,
        'Unknown': COLORS.teal,
    };

    new Chart(periodCtx, {
        type: 'bar',
        data: {
            labels: data.period.labels,
            datasets: [{
                label: 'Atraso Médio (min)',
                data: data.period.avg_delay,
                backgroundColor: data.period.labels.map(l => alpha(periodColors[l] || COLORS.blue, 0.75)),
                borderColor: data.period.labels.map(l => periodColors[l] || COLORS.blue),
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { title: { display: true, text: 'Atraso (min)' }, beginAtZero: true }
            }
        }
    });
}

// ===== Airlines =====
async function renderAirlines() {
    const data = await loadJSON('dashboard_airlines.json');

    // By Delay
    const delayCtx = document.getElementById('airlines-delay-chart').getContext('2d');
    new Chart(delayCtx, {
        type: 'bar',
        data: {
            labels: data.by_delay.labels,
            datasets: [{
                label: 'Atraso Médio (min)',
                data: data.by_delay.avg_delay,
                backgroundColor: data.by_delay.avg_delay.map((v, i) =>
                    alpha(PALETTE[i % PALETTE.length], 0.75)
                ),
                borderColor: data.by_delay.avg_delay.map((v, i) =>
                    PALETTE[i % PALETTE.length]
                ),
                borderWidth: 2,
                borderRadius: 6,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        afterLabel: (item) => {
                            const idx = item.dataIndex;
                            return `${data.by_delay.names[idx]}\nVoos: ${formatNumber(data.by_delay.flight_count[idx])}`;
                        }
                    }
                }
            },
            scales: {
                x: { title: { display: true, text: 'Atraso Médio (min)' }, beginAtZero: true }
            }
        }
    });

    // By Volume
    const volCtx = document.getElementById('airlines-volume-chart').getContext('2d');
    new Chart(volCtx, {
        type: 'bar',
        data: {
            labels: data.by_volume.labels,
            datasets: [
                {
                    label: 'Número de Voos',
                    data: data.by_volume.flight_count,
                    backgroundColor: alpha(COLORS.blue, 0.7),
                    borderColor: COLORS.blue,
                    borderWidth: 2,
                    borderRadius: 6,
                    yAxisID: 'y',
                },
                {
                    label: 'Taxa de Atraso (%)',
                    data: data.by_volume.delay_rate,
                    type: 'line',
                    borderColor: COLORS.red,
                    backgroundColor: alpha(COLORS.red, 0.1),
                    pointBackgroundColor: COLORS.red,
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    tension: 0.4,
                    yAxisID: 'y1',
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                tooltip: {
                    callbacks: {
                        afterLabel: (item) => {
                            const idx = item.dataIndex;
                            return data.by_volume.names[idx];
                        }
                    }
                }
            },
            scales: {
                y: {
                    title: { display: true, text: 'Voos' },
                    ticks: { callback: v => formatNumber(v) },
                    position: 'left',
                },
                y1: {
                    title: { display: true, text: 'Taxa (%)' },
                    position: 'right',
                    grid: { drawOnChartArea: false },
                }
            }
        }
    });
}

// ===== Airports =====
async function renderAirports() {
    const data = await loadJSON('dashboard_airports.json');

    // Origin
    const originCtx = document.getElementById('airports-origin-chart').getContext('2d');
    new Chart(originCtx, {
        type: 'bar',
        data: {
            labels: data.top_origin_delay.labels,
            datasets: [{
                label: 'Atraso Partida (min)',
                data: data.top_origin_delay.avg_delay,
                backgroundColor: data.top_origin_delay.avg_delay.map((_, i) =>
                    alpha(COLORS.orange, 0.6 + (i / 20))
                ),
                borderColor: COLORS.orange,
                borderWidth: 1,
                borderRadius: 6,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        afterLabel: (item) => {
                            const idx = item.dataIndex;
                            return `${data.top_origin_delay.names[idx]}\nVoos: ${formatNumber(data.top_origin_delay.flight_count[idx])}`;
                        }
                    }
                }
            },
            scales: {
                x: { title: { display: true, text: 'Atraso Médio (min)' }, beginAtZero: true }
            }
        }
    });

    // Destination
    const destCtx = document.getElementById('airports-dest-chart').getContext('2d');
    new Chart(destCtx, {
        type: 'bar',
        data: {
            labels: data.top_dest_delay.labels,
            datasets: [{
                label: 'Atraso Chegada (min)',
                data: data.top_dest_delay.avg_delay,
                backgroundColor: data.top_dest_delay.avg_delay.map((_, i) =>
                    alpha(COLORS.purple, 0.6 + (i / 20))
                ),
                borderColor: COLORS.purple,
                borderWidth: 1,
                borderRadius: 6,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        afterLabel: (item) => {
                            const idx = item.dataIndex;
                            return `${data.top_dest_delay.names[idx]}\nVoos: ${formatNumber(data.top_dest_delay.flight_count[idx])}`;
                        }
                    }
                }
            },
            scales: {
                x: { title: { display: true, text: 'Atraso Médio (min)' }, beginAtZero: true }
            }
        }
    });
}

// ===== Correlation Heatmap =====
async function renderCorrelation() {
    const data = await loadJSON('dashboard_correlation.json');
    const container = document.getElementById('heatmap-container');

    // Short labels
    const shortLabels = {
        'DEPARTURE_DELAY': 'Dep. Delay',
        'ARRIVAL_DELAY': 'Arr. Delay',
        'AIR_TIME': 'Air Time',
        'DISTANCE': 'Distance',
        'TAXI_OUT': 'Taxi Out',
        'TAXI_IN': 'Taxi In',
        'ELAPSED_TIME': 'Elapsed',
    };

    function getHeatmapColor(val) {
        // Blue (negative) -> Gray (zero) -> Red (positive)
        const absVal = Math.abs(val);
        if (val >= 0) {
            const r = Math.round(239 * absVal + 30 * (1 - absVal));
            const g = Math.round(68 * absVal + 41 * (1 - absVal));
            const b = Math.round(68 * absVal + 55 * (1 - absVal));
            return `rgb(${r},${g},${b})`;
        } else {
            const r = Math.round(59 * absVal + 30 * (1 - absVal));
            const g = Math.round(130 * absVal + 41 * (1 - absVal));
            const b = Math.round(246 * absVal + 55 * (1 - absVal));
            return `rgb(${r},${g},${b})`;
        }
    }

    function getTextColor(val) {
        return Math.abs(val) > 0.5 ? '#fff' : '#94a3b8';
    }

    let html = '<table class="heatmap-table"><thead><tr><th></th>';
    data.labels.forEach(l => {
        html += `<th>${shortLabels[l] || l}</th>`;
    });
    html += '</tr></thead><tbody>';

    data.matrix.forEach((row, i) => {
        html += `<tr><td class="row-header">${shortLabels[data.labels[i]] || data.labels[i]}</td>`;
        row.forEach((val, j) => {
            const bg = getHeatmapColor(val);
            const color = getTextColor(val);
            html += `<td style="background:${bg};color:${color}" title="${data.labels[i]} × ${data.labels[j]}: ${val}">${val.toFixed(2)}</td>`;
        });
        html += '</tr>';
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

// ===== Cancellations =====
async function renderCancellations() {
    const data = await loadJSON('dashboard_cancellations.json');

    // Reasons Pie
    const reasonsCtx = document.getElementById('cancel-reasons-chart').getContext('2d');
    const reasonColors = {
        'Weather': COLORS.blue,
        'Airline/Carrier': COLORS.orange,
        'NAS': COLORS.purple,
        'Security': COLORS.red,
        'No data': COLORS.teal,
    };

    new Chart(reasonsCtx, {
        type: 'doughnut',
        data: {
            labels: data.reasons.labels,
            datasets: [{
                data: data.reasons.values,
                backgroundColor: data.reasons.labels.map(l => alpha(reasonColors[l] || COLORS.teal, 0.8)),
                borderColor: data.reasons.labels.map(l => reasonColors[l] || COLORS.teal),
                borderWidth: 2,
                hoverOffset: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '50%',
            plugins: {
                legend: { position: 'bottom', labels: { font: { size: 11 } } },
                tooltip: {
                    callbacks: {
                        label: (item) => {
                            const total = item.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = ((item.raw / total) * 100).toFixed(1);
                            return ` ${item.label}: ${item.raw.toLocaleString('pt-BR')} (${pct}%)`;
                        }
                    }
                }
            }
        }
    });

    // Monthly cancel rate
    const monthlyCtx = document.getElementById('cancel-monthly-chart').getContext('2d');
    const monthlyGrad = createGradient(monthlyCtx, COLORS.red, COLORS.red);

    new Chart(monthlyCtx, {
        type: 'bar',
        data: {
            labels: data.monthly_cancel_rate.labels,
            datasets: [{
                label: 'Taxa Cancel. (%)',
                data: data.monthly_cancel_rate.values,
                backgroundColor: monthlyGrad,
                borderColor: COLORS.red,
                borderWidth: 1,
                borderRadius: 6,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { title: { display: true, text: 'Taxa (%)' }, beginAtZero: true }
            }
        }
    });

    // Delay types
    const typesCtx = document.getElementById('delay-types-chart').getContext('2d');
    const typeColors = [COLORS.blue, COLORS.red, COLORS.orange, COLORS.purple, COLORS.cyan];

    new Chart(typesCtx, {
        type: 'polarArea',
        data: {
            labels: data.delay_types.labels,
            datasets: [{
                data: data.delay_types.values,
                backgroundColor: typeColors.map(c => alpha(c, 0.6)),
                borderColor: typeColors,
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom', labels: { font: { size: 10 } } },
                tooltip: {
                    callbacks: {
                        label: (item) => ` ${item.label}: ${formatNumber(item.raw)} min acumulados`
                    }
                }
            },
            scales: {
                r: {
                    ticks: { display: false },
                    grid: { color: 'rgba(255,255,255,0.05)' }
                }
            }
        }
    });
}

// ===== Tab Logic =====
function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-target');
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(target).classList.add('active');
            
            if (target === 'ml-content' && !window.mlLoaded) {
                renderMachineLearning();
                window.mlLoaded = true;
            }
            if (target === 'story-content' && !window.storyLoaded) {
                renderStorytelling();
                window.storyLoaded = true;
            }
        });
    });
}

// ===== Machine Learning Rendering =====
let mlDataRoc = null;
let mlDataPr = null;

async function renderMachineLearning() {
    try {
        await Promise.all([
            renderModelComparison(),
            renderFeatureImportance(),
            renderConfusionMatrix(),
            loadRocPrData(),
            renderElbowMethod(),
            renderPcaVariance(),
            renderClusterProfiles(),
            renderPcaScatter()
        ]);
        console.log('✅ ML Dashboard loaded successfully');
    } catch (err) {
        console.error('❌ Error loading ML dashboard:', err);
    }
}

async function renderModelComparison() {
    const data = await loadJSON('ml_model_comparison.json');
    const ctx = document.getElementById('model-comparison-chart').getContext('2d');
    
    const datasets = [
        { label: 'Accuracy', data: data.metrics.accuracy, backgroundColor: alpha(COLORS.blue, 0.8) },
        { label: 'F1 Score', data: data.metrics.f1_weighted, backgroundColor: alpha(COLORS.purple, 0.8) },
        { label: 'ROC AUC', data: data.metrics.roc_auc, backgroundColor: alpha(COLORS.orange, 0.8) }
    ];

    new Chart(ctx, {
        type: 'bar',
        data: { labels: data.models, datasets: datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true, max: 1 } }
        }
    });
}

async function renderFeatureImportance() {
    const data = await loadJSON('ml_feature_importance.json');
    const ctx = document.getElementById('feature-importance-chart').getContext('2d');
    
    // Top 10 features
    const topFeatures = data.features.slice(0, 10);
    const labels = topFeatures.map(f => f.name);
    const values = topFeatures.map(f => f.importance);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Importância',
                data: values,
                backgroundColor: alpha(COLORS.teal, 0.8),
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { x: { beginAtZero: true } }
        }
    });
}

async function renderConfusionMatrix() {
    const data = await loadJSON('ml_confusion_matrices.json');
    const container = document.getElementById('cm-heatmap-container');
    
    // Show Random Forest by default if exists, else first model
    const modelName = data['Random Forest'] ? 'Random Forest' : Object.keys(data)[0];
    const cm = data[modelName];
    
    const tn = cm.TN || cm.matrix[0][0];
    const fp = cm.FP || cm.matrix[0][1];
    const fn = cm.FN || cm.matrix[1][0];
    const tp = cm.TP || cm.matrix[1][1];
    const total = tn + fp + fn + tp;
    
    // Build a simple 2x2 grid table
    const html = `
        <table class="heatmap-table" style="transform: scale(1.1);">
            <thead>
                <tr>
                    <th></th>
                    <th>Predito: No Prazo</th>
                    <th>Predito: Atrasado</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="row-header">Real: No Prazo</td>
                    <td style="background: rgba(16, 185, 129, 0.2); color: #fff;">
                        <div>Verdadeiro Negativo</div>
                        <div style="font-size: 1.2rem;">${formatNumber(tn)}</div>
                        <div style="font-size: 0.7rem; opacity: 0.7;">${((tn/total)*100).toFixed(1)}%</div>
                    </td>
                    <td style="background: rgba(239, 68, 68, 0.2); color: #fff;">
                        <div>Falso Positivo</div>
                        <div style="font-size: 1.2rem;">${formatNumber(fp)}</div>
                        <div style="font-size: 0.7rem; opacity: 0.7;">${((fp/total)*100).toFixed(1)}%</div>
                    </td>
                </tr>
                <tr>
                    <td class="row-header">Real: Atrasado</td>
                    <td style="background: rgba(249, 115, 22, 0.2); color: #fff;">
                        <div>Falso Negativo</div>
                        <div style="font-size: 1.2rem;">${formatNumber(fn)}</div>
                        <div style="font-size: 0.7rem; opacity: 0.7;">${((fn/total)*100).toFixed(1)}%</div>
                    </td>
                    <td style="background: rgba(59, 130, 246, 0.2); color: #fff;">
                        <div>Verdadeiro Positivo</div>
                        <div style="font-size: 1.2rem;">${formatNumber(tp)}</div>
                        <div style="font-size: 0.7rem; opacity: 0.7;">${((tp/total)*100).toFixed(1)}%</div>
                    </td>
                </tr>
            </tbody>
        </table>
    `;
    container.innerHTML = html;
}

async function loadRocPrData() {
    mlDataRoc = await loadJSON('ml_roc_curves.json');
    mlDataPr = await loadJSON('ml_pr_curves.json');
    renderRocPrChart('roc'); // Render default
}

window.switchInnerTab = function(type) {
    const btns = document.querySelectorAll('.tab-inner-btn');
    btns.forEach(b => b.classList.remove('active'));
    
    if (type === 'roc') {
        document.querySelector('[data-target="roc-chart"]').classList.add('active');
        renderRocPrChart('roc');
    } else {
        document.querySelector('[data-target="pr-chart"]').classList.add('active');
        renderRocPrChart('pr');
    }
}

function renderRocPrChart(type) {
    const ctx = document.getElementById('roc-pr-chart').getContext('2d');
    const chartId = 'roc-pr-chart-instance';
    
    // Destroy previous Chart instance
    if (window[chartId]) {
        window[chartId].destroy();
    }
    
    const data = type === 'roc' ? mlDataRoc : mlDataPr;
    if (!data) return;

    const datasets = [];
    const models = Object.keys(data);
    const colors = [COLORS.blue, COLORS.purple, COLORS.orange];

    models.forEach((model, idx) => {
        const modelData = data[model];
        // Downsample slightly if curve has too many points
        const step = Math.ceil((modelData.fpr || modelData.recall).length / 100);
        const xData = (type === 'roc' ? modelData.fpr : modelData.recall).filter((_, i) => i % step === 0);
        const yData = (type === 'roc' ? modelData.tpr : modelData.precision).filter((_, i) => i % step === 0);
        
        datasets.push({
            label: `${model} (AUC = ${modelData.auc.toFixed(3)})`,
            data: xData.map((x, i) => ({ x: x, y: yData[i] })),
            borderColor: colors[idx % colors.length],
            backgroundColor: 'transparent',
            pointRadius: 0,
            pointHoverRadius: 4,
            tension: 0.2
        });
    });

    // Baseline
    if (type === 'roc') {
        datasets.push({
            label: 'Aleatório',
            data: [{x: 0, y: 0}, {x: 1, y: 1}],
            borderColor: 'rgba(255,255,255,0.2)',
            borderDash: [5, 5],
            pointRadius: 0
        });
    }

    window[chartId] = new Chart(ctx, {
        type: 'line',
        data: { datasets: datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { title: { display: true, text: type === 'roc' ? 'Falso Positivo Rate' : 'Recall' }, type: 'linear', min: 0, max: 1 },
                y: { title: { display: true, text: type === 'roc' ? 'Verdadeiro Positivo Rate' : 'Precision' }, type: 'linear', min: 0, max: 1 }
            }
        }
    });
}

// === Unsupervised ===

async function renderElbowMethod() {
    const data = await loadJSON('ml_kmeans_elbow.json');
    const ctx = document.getElementById('elbow-chart').getContext('2d');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.k_values,
            datasets: [{
                label: 'Inércia',
                data: data.inertia,
                borderColor: COLORS.pink,
                backgroundColor: alpha(COLORS.pink, 0.1),
                fill: true,
                pointBackgroundColor: COLORS.pink,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { x: { title: { display: true, text: 'Número de Clusters (K)' } } }
        }
    });
}

async function renderPcaVariance() {
    const data = await loadJSON('ml_pca_variance.json');
    const ctx = document.getElementById('pca-variance-chart').getContext('2d');
    
    // Show only first 15 if there are too many
    const labels = Array.from({length: data.n_components}, (_, i) => `PC${i+1}`).slice(0, 15);
    const varRatio = data.explained_variance_ratio.slice(0, 15).map(v => v * 100);
    const cumVarRatio = data.cumulative_variance.slice(0, 15).map(v => v * 100);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    type: 'line',
                    label: 'Variância Acumulada (%)',
                    data: cumVarRatio,
                    borderColor: COLORS.red,
                    backgroundColor: 'transparent',
                    pointBackgroundColor: COLORS.red,
                    tension: 0.2,
                    yAxisID: 'y'
                },
                {
                    type: 'bar',
                    label: 'Variância Explicada (%)',
                    data: varRatio,
                    backgroundColor: alpha(COLORS.cyan, 0.7),
                    borderRadius: 4,
                    yAxisID: 'y'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { min: 0 } }
        }
    });
}

async function renderClusterProfiles() {
    const data = await loadJSON('ml_cluster_profiles.json');
    const ctx = document.getElementById('cluster-profiles-chart').getContext('2d');
    
    // Normalize data for radar chart so they fit nicely
    // For simplicity, we just use raw delay & rate values if comparable, but standardizing is better
    // Since radar charts are tricky with unscaled data, let's just make a grouped bar chart
    
    const clusters = data.clusters;
    const labels = clusters.map(c => `Cluster ${c.id}: ${c.label}`);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Taxa de Atraso Média (%)',
                    data: clusters.map(c => c.avg_delay_rate * 100),
                    backgroundColor: alpha(COLORS.red, 0.7),
                },
                {
                    label: 'Distância Média (/10)',
                    data: clusters.map(c => c.avg_distance / 10), // scaled down to compare visually
                    backgroundColor: alpha(COLORS.blue, 0.7),
                },
                {
                    label: 'Voos Médios',
                    data: clusters.map(c => c.avg_flight_count),
                    backgroundColor: alpha(COLORS.green, 0.7),
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true } }
        }
    });
}

async function renderPcaScatter() {
    const data = await loadJSON('ml_pca_scatter.json');
    const ctx = document.getElementById('pca-scatter-chart').getContext('2d');
    
    // data.PC1, data.PC2, data.cluster
    // We group points by cluster
    const clusterMap = {};
    const clusterLabels = data.cluster || new Array(data.PC1.length).fill(0); // fallback
    
    for (let i = 0; i < data.PC1.length; i++) {
        const cId = clusterLabels[i];
        if (!clusterMap[cId]) clusterMap[cId] = [];
        clusterMap[cId].push({ x: data.PC1[i], y: data.PC2[i] });
    }
    
    const datasets = Object.keys(clusterMap).map((cId, idx) => ({
        label: `Cluster ${cId}`,
        data: clusterMap[cId],
        backgroundColor: alpha(PALETTE[idx % PALETTE.length], 0.6),
        borderColor: PALETTE[idx % PALETTE.length],
        borderWidth: 1,
        pointRadius: 3,
        pointHoverRadius: 6
    }));

    new Chart(ctx, {
        type: 'scatter',
        data: { datasets: datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: (item) => `PC1: ${item.raw.x.toFixed(2)}, PC2: ${item.raw.y.toFixed(2)}`
                    }
                }
            },
            scales: {
                x: { title: { display: true, text: 'Componente Principal 1' } },
                y: { title: { display: true, text: 'Componente Principal 2' } }
            }
        }
    });
}

// ===== Storytelling Rendering =====
async function renderStorytelling() {
    try {
        await renderStoryFeatureChart();
        console.log('✅ Storytelling tab loaded successfully');
    } catch (err) {
        console.error('❌ Error loading storytelling tab:', err);
    }
}

async function renderStoryFeatureChart() {
    const data = await loadJSON('ml_feature_importance.json');
    const ctx = document.getElementById('story-feature-chart').getContext('2d');
    
    const targetFeatures = ['SCHEDULED_TIME', 'MONTH', 'AIRLINE', 'DISTANCE'];
    const friendlyNames = {
        'SCHEDULED_TIME': 'Horário Programado',
        'MONTH': 'Mês do Ano',
        'AIRLINE': 'Companhia Aérea',
        'DISTANCE': 'Distância do Voo'
    };
    
    const filteredFeatures = data.features.filter(f => targetFeatures.includes(f.name));
    filteredFeatures.sort((a,b) => b.importance - a.importance);
    
    const labels = filteredFeatures.map(f => friendlyNames[f.name]);
    const values = filteredFeatures.map(f => f.importance);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Relevância no Atraso',
                data: values,
                backgroundColor: alpha(COLORS.blue, 0.8),
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: () => ' Alto Impacto no Atraso'
                    }
                }
            },
            scales: {
                x: { display: false },
                y: {
                    ticks: {
                        font: { size: 13, weight: '600' },
                        color: '#f1f5f9'
                    }
                }
            }
        }
    });
}

// ===== Initialize =====
async function init() {
    setupTabs();
    try {
        await Promise.all([
            renderKPIs(),
            renderDelayDistribution(),
            renderTemporal(),
            renderAirlines(),
            renderAirports(),
            renderCorrelation(),
            renderCancellations(),
        ]);
        console.log('✅ Dashboard loaded successfully');
    } catch (err) {
        console.error('❌ Error loading dashboard:', err);
    }
}

document.addEventListener('DOMContentLoaded', init);
