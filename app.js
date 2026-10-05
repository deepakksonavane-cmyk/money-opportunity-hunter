const sampleData = [
  {
    project_client: 'SME Exporter Expansion',
    platform: 'LinkedIn Jobs / Consulting',
    requirement: 'Research 3 export markets, identify buyer segments, assess demand, build a territory map, and prepare feasibility summary for B2B expansion.',
    payment: 45000,
    estimated_days: 7,
    deadline: 'Within 72 hours',
    application_url: 'https://www.linkedin.com/jobs',
    status: 'NEW',
    why_fit: 'Strong in market research, territory mapping, opportunity intelligence, and commercial feasibility.',
  },
  {
    project_client: 'Sponsorship Growth Consultant',
    platform: 'Upwork',
    requirement: 'Create event sponsorship prospect list, draft sponsor deck, identify relevant brands, and estimate outreach strategy for a city event.',
    payment: 28000,
    estimated_days: 5,
    deadline: 'Open now',
    application_url: 'https://www.upwork.com',
    status: 'NEW',
    why_fit: 'Experienced in sponsorship, event development, prospect mapping, and business development outreach.',
  },
  {
    project_client: 'Business Model Validation',
    platform: 'Fiverr / Consulting',
    requirement: 'Review startup idea, identify customer segments, build a business model canvas, assess pricing, competitors, and launch assumptions.',
    payment: 22000,
    estimated_days: 6,
    deadline: 'This week',
    application_url: 'https://www.fiverr.com',
    status: 'BID',
    why_fit: 'Strong at business-model design, customer discovery, competitor research, and turning vague ideas into executable plans.',
  },
  {
    project_client: 'Regional Vendor Research',
    platform: 'Workana',
    requirement: 'Compile vendor shortlist for packaging, print, transport, and local service providers across two cities and compare costs and lead times.',
    payment: 18000,
    estimated_days: 4,
    deadline: 'Open now',
    application_url: 'https://www.workana.com',
    status: 'NEW',
    why_fit: 'Excellent at vendor research, operations planning, SOP design, and commercial evaluation.',
  },
  {
    project_client: 'Territory Expansion Study',
    platform: 'PeoplePerHour',
    requirement: 'Research 5 target territories, find customer density, competitor presence, pricing models, and local partner opportunities for a new service business.',
    payment: 30000,
    estimated_days: 7,
    deadline: 'Open now',
    application_url: 'https://www.peopleperhour.com',
    status: 'NEW',
    why_fit: 'Highly aligned with territory research, market intelligence, forecasting, and feasibility analysis.',
  },
];

const scoreByKeyword = [
  'market', 'research', 'feasibility', 'business model', 'territory', 'vendor', 'sponsorship', 'competitor', 'forecast', 'customer', 'operations', 'sop', 'opportunity', 'commercial', 'analysis'
];

let opportunities = [...sampleData];

function formatCurrency(value) {
  return '₹' + Number(value).toLocaleString('en-IN');
}

function scoreFit(text) {
  const lower = (text || '').toLowerCase();
  let total = 0;
  scoreByKeyword.forEach((keyword) => {
    if (lower.includes(keyword)) total += 8;
  });
  return Math.min(100, total);
}

function scorePay(payment) {
  if (payment < 10000) return 0;
  if (payment < 20000) return 40;
  if (payment < 35000) return 65;
  if (payment < 60000) return 80;
  if (payment < 90000) return 90;
  return 100;
}

function scoreTime(days) {
  if (days <= 3) return 90;
  if (days <= 5) return 80;
  if (days <= 7) return 72;
  if (days <= 10) return 60;
  if (days <= 15) return 45;
  return 15;
}

function scoreCredibility(platform) {
  const lower = (platform || '').toLowerCase();
  if (lower.includes('linkedin')) return 82;
  if (lower.includes('upwork')) return 80;
  if (lower.includes('fiverr')) return 75;
  if (lower.includes('workana')) return 75;
  if (lower.includes('peopleperhour')) return 78;
  if (lower.includes('csr') || lower.includes('ngo')) return 68;
  return 65;
}

function scoreWinProbability(item) {
  let score = 50;
  const text = (item.requirement || '').toLowerCase();
  if (text.includes('market research')) score += 15;
  if (text.includes('territory')) score += 10;
  if (text.includes('vendor')) score += 8;
  if (text.includes('sponsorship')) score += 10;
  if (item.estimated_days <= 7) score += 10;
  if (item.payment >= 25000) score += 10;
  return Math.min(100, score);
}

function buildBid(payment) {
  if (payment < 15000) return payment;
  if (payment < 30000) return Math.round(payment * 0.72);
  if (payment < 60000) return Math.round(payment * 0.68);
  return Math.round(payment * 0.62);
}

function scoreOpportunity(item) {
  const fitScore = scoreFit(item.requirement + ' ' + item.why_fit);
  const payScore = scorePay(item.payment);
  const timeScore = scoreTime(item.estimated_days);
  const credibilityScore = scoreCredibility(item.platform);
  const winScore = scoreWinProbability(item);
  const overall = Math.round(
    0.30 * fitScore +
    0.20 * payScore +
    0.20 * timeScore +
    0.15 * credibilityScore +
    0.15 * winScore
  );

  return {
    ...item,
    fitScore,
    payScore,
    timeScore,
    credibilityScore,
    winScore,
    overall,
    recommendedBid: buildBid(item.payment),
  };
}

function getSortedOpportunities() {
  const filterValue = document.getElementById('statusFilter').value;
  const filtered = filterValue === 'ALL'
    ? opportunities
    : opportunities.filter((item) => item.status === filterValue);

  return [...filtered]
    .map(scoreOpportunity)
    .sort((a, b) => b.overall - a.overall)
    .slice(0, 10);
}

function renderSummary() {
  const scored = opportunities.map(scoreOpportunity);
  const total = scored.length;
  const avgScore = total ? Math.round(scored.reduce((sum, item) => sum + item.overall, 0) / total) : 0;
  const highPriority = scored.filter((item) => item.overall >= 80).length;
  const totalPipeline = scored.reduce((sum, item) => sum + item.payment, 0);

  const cards = [
    { label: 'Total opportunities', value: total },
    { label: 'Average score', value: avgScore },
    { label: 'High fit (>80)', value: highPriority },
    { label: 'Pipeline value', value: formatCurrency(totalPipeline) },
  ];

  document.getElementById('summaryCards').innerHTML = cards.map((card) => `
    <div class="card">
      <div class="label">${card.label}</div>
      <p class="value">${card.value}</p>
    </div>
  `).join('');
}

function renderTable() {
  const topTen = getSortedOpportunities();
  const tbody = document.getElementById('opportunityTable');

  if (!topTen.length) {
    tbody.innerHTML = '<tr><td colspan="9">No opportunities match this status.</td></tr>';
    return;
  }

  tbody.innerHTML = topTen.map((item) => `
    <tr>
      <td>
        <strong>${item.project_client}</strong><br>
        <small>${item.requirement}</small>
      </td>
      <td>${item.platform}</td>
      <td>${formatCurrency(item.payment)}</td>
      <td>${item.estimated_days}</td>
      <td>${item.overall}</td>
      <td><span class="badge ${item.status}">${item.status}</span></td>
      <td>${formatCurrency(item.recommendedBid)}</td>
      <td>${item.deadline}</td>
      <td><a href="${item.application_url || '#'}" target="_blank" rel="noreferrer">Open</a></td>
    </tr>
  `).join('');
}

function handleSubmit(event) {
  event.preventDefault();
  const form = new FormData(event.target);
  const newOpportunity = {
    project_client: form.get('project_client').toString().trim(),
    platform: form.get('platform').toString().trim(),
    requirement: form.get('requirement').toString().trim(),
    payment: Number(form.get('payment')) || 0,
    estimated_days: Number(form.get('estimated_days')) || 0,
    deadline: form.get('deadline').toString().trim() || 'Open now',
    application_url: form.get('application_url').toString().trim() || '#',
    status: form.get('status').toString() || 'NEW',
    why_fit: form.get('why_fit').toString().trim() || 'Relevant market and business opportunity fit.',
  };

  if (!newOpportunity.project_client || !newOpportunity.platform || !newOpportunity.requirement) {
    return;
  }

  opportunities.unshift(newOpportunity);
  event.target.reset();
  renderAll();
}

function resetSampleData() {
  opportunities = [...sampleData];
  renderAll();
}

function renderAll() {
  renderSummary();
  renderTable();
}

document.getElementById('opportunityForm').addEventListener('submit', handleSubmit);
document.getElementById('resetBtn').addEventListener('click', resetSampleData);
document.getElementById('statusFilter').addEventListener('change', renderTable);

renderAll();
