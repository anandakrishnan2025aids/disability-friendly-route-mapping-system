let reportMap, reportMarker;
let selectedLat = null, selectedLng = null;
let currentStep = 1;
let uploadedImageB64 = null;
let uploadedFilename = '';

// ── Image Upload + Auto Detection ────────────────────────────
const uploadZone = document.getElementById('uploadZone');

uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('drag-over'); });
uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('drag-over'));
uploadZone.addEventListener('drop', e => {
    e.preventDefault();
    uploadZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) handleImageFile(file);
});

document.getElementById('imageInput').addEventListener('change', e => {
    if (e.target.files[0]) handleImageFile(e.target.files[0]);
});

function handleImageFile(file) {
    if (!file.type.startsWith('image/')) return;
    uploadedFilename = file.name;
    const reader = new FileReader();
    reader.onload = async ev => {
        const b64 = ev.target.result.split(',')[1];
        uploadedImageB64 = b64;
        document.getElementById('previewImg').src = ev.target.result;
        document.getElementById('uploadPlaceholder').classList.add('hidden');
        document.getElementById('uploadPreview').classList.remove('hidden');
        await runAutoDetection(b64, file.name);
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    uploadedImageB64 = null;
    uploadedFilename = '';
    document.getElementById('imageInput').value = '';
    document.getElementById('uploadPlaceholder').classList.remove('hidden');
    document.getElementById('uploadPreview').classList.add('hidden');
    document.getElementById('detectionResult').classList.add('hidden');
    document.getElementById('detectionResult').innerHTML = '';
}

async function runAutoDetection(b64, filename) {
    const resultEl = document.getElementById('detectionResult');
    resultEl.className = 'detection-result detection-loading';
    resultEl.innerHTML = '<span class="det-spinner"></span> Analysing image…';

    try {
        const res  = await fetch('/api/analyze-image', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename, image_b64: b64 }),
        });
        const data = await res.json();

        if (data.detected) {
            // Auto-fill issue type
            const radio = document.querySelector('input[name="issue_type"][value="' + data.issue_type + '"]');
            if (radio) {
                radio.checked = true;
                radio.closest('.issue-type-card').classList.add('ai-selected');
            }
            // Auto-fill title if empty
            const titleEl = document.getElementById('title');
            if (!titleEl.value.trim()) titleEl.value = data.title;
            // Auto-fill description if empty
            const descEl = document.getElementById('description');
            if (!descEl.value.trim()) descEl.value = data.description;
            // Auto-select severity
            const sevRadio = document.querySelector('input[name="severity"][value="' + data.severity + '"]');
            if (sevRadio) sevRadio.checked = true;

            const confColor = data.confidence >= 80 ? '#10e8b8' : data.confidence >= 60 ? '#ffc35a' : '#ff5c7a';
            resultEl.className = 'detection-result detection-success';
            resultEl.innerHTML =
                '<div class="det-header"><span class="det-icon">🤖</span><strong>AI Detection Complete</strong>' +
                '<span class="det-conf" style="color:' + confColor + '">' + data.confidence + '% confidence</span></div>' +
                '<div class="det-rows">' +
                '<div class="det-row"><span class="det-label">Issue Type</span><span class="det-val">' + data.issue_type.replace(/_/g, ' ') + '</span></div>' +
                '<div class="det-row"><span class="det-label">Severity</span><span class="det-val det-sev det-sev-' + data.severity + '">' + data.severity.toUpperCase() + '</span></div>' +
                '</div>' +
                '<div class="det-note">Fields have been auto-filled. You can edit them before submitting.</div>';
        }
    } catch {
        resultEl.className = 'detection-result detection-error';
        resultEl.innerHTML = '⚠️ Could not analyse image. Please fill in the details manually.';
    }
}

function goToStep(n) {
    if (n === 2 && !validateStep1()) return;
    if (n === 3 && !validateStep2()) return;
    currentStep = n;
    document.querySelectorAll('.form-step').forEach((s, i) => { s.classList.toggle('hidden', i + 1 !== n); });
    document.querySelectorAll('.step').forEach((s, i) => { s.classList.toggle('active', i + 1 === n); s.classList.toggle('done', i + 1 < n); });
    if (n === 2 && !reportMap) initReportMap();
    if (n === 3) buildReview();
}

function validateStep1() {
    let ok = true;
    const issueType = document.querySelector('input[name="issue_type"]:checked');
    const title = document.getElementById('title').value.trim();
    const desc = document.getElementById('description').value.trim();
    setError('issueTypeError', !issueType, 'Please select an issue type.');
    setError('titleError', !title, 'Please enter a title.');
    setError('descriptionError', !desc, 'Please describe the issue.');
    if (!issueType || !title || !desc) ok = false;
    return ok;
}

function validateStep2() {
    const loc = document.getElementById('location').value.trim();
    setError('locationError', !loc, 'Please enter a location.');
    return !!loc;
}

function setError(id, show, msg) {
    const el = document.getElementById(id);
    if (el) el.textContent = show ? msg : '';
}

function initReportMap() {
    reportMap = L.map('reportMap').setView([11.0168, 76.9558], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap contributors' }).addTo(reportMap);
    reportMap.on('click', e => {
        selectedLat = e.latlng.lat.toFixed(5);
        selectedLng = e.latlng.lng.toFixed(5);
        document.getElementById('coordsDisplay').textContent = '📍 ' + selectedLat + ', ' + selectedLng;
        if (reportMarker) reportMap.removeLayer(reportMarker);
        reportMarker = L.marker(e.latlng).addTo(reportMap);
    });
}

function buildReview() {
    const issueType = document.querySelector('input[name="issue_type"]:checked')?.value || '';
    const title = document.getElementById('title').value.trim();
    const desc = document.getElementById('description').value.trim();
    const severity = document.querySelector('input[name="severity"]:checked')?.value || 'medium';
    const location = document.getElementById('location').value.trim();
    document.getElementById('reviewBox').innerHTML = '<div class="review-row"><span class="review-label">Issue Type</span><span class="review-value">' + issueType.replace(/_/g, ' ') + '</span></div><div class="review-row"><span class="review-label">Title</span><span class="review-value">' + title + '</span></div><div class="review-row"><span class="review-label">Description</span><span class="review-value">' + desc + '</span></div><div class="review-row"><span class="review-label">Severity</span><span class="review-value">' + severity.toUpperCase() + '</span></div><div class="review-row"><span class="review-label">Location</span><span class="review-value">' + location + '</span></div>' + (selectedLat ? '<div class="review-row"><span class="review-label">Coordinates</span><span class="review-value" style="font-family:monospace;">' + selectedLat + ', ' + selectedLng + '</span></div>' : '');
}

document.getElementById('reportForm').addEventListener('submit', async e => {
    e.preventDefault();
    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    const payload = {
        issue_type: document.querySelector('input[name="issue_type"]:checked')?.value,
        title: document.getElementById('title').value.trim(),
        description: document.getElementById('description').value.trim(),
        severity: document.querySelector('input[name="severity"]:checked')?.value || 'medium',
        location: document.getElementById('location').value.trim(),
        lat: selectedLat ? parseFloat(selectedLat) : null,
        lng: selectedLng ? parseFloat(selectedLng) : null,
    };
    try {
        const res = await fetch('/api/reports', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
        if (res.ok) {
            document.getElementById('reportFormCard').classList.add('hidden');
            document.getElementById('successCard').classList.remove('hidden');
            loadRecentReports();
        } else { alert('Submission failed. Please try again.'); }
    } catch { alert('Network error. Please try again.'); }
    btn.disabled = false;
});

function resetForm() {
    document.getElementById('reportFormCard').classList.remove('hidden');
    document.getElementById('successCard').classList.add('hidden');
    document.getElementById('reportForm').reset();
    goToStep(1);
    selectedLat = null; selectedLng = null;
    document.getElementById('coordsDisplay').textContent = '';
    if (reportMarker && reportMap) { reportMap.removeLayer(reportMarker); reportMarker = null; }
}

async function loadRecentReports() {
    const res = await fetch('/api/reports');
    const data = await res.json();
    const container = document.getElementById('recentReports');
    if (!data.reports.length) { container.innerHTML = '<p class="no-reports">No reports yet. Be the first!</p>'; return; }
    const sorted = [...data.reports].reverse().slice(0, 8);
    container.innerHTML = sorted.map(r => '<div class="report-card"><div class="report-card-title">' + r.title + '</div><div class="report-card-meta"><span class="report-type-badge">' + r.issue_type.replace(/_/g, ' ') + '</span><span class="report-time">' + timeAgo(r.submitted_at) + '</span><button class="upvote-btn" onclick="upvote(' + r.id + ', this)">▲ ' + r.upvotes + '</button></div></div>').join('');
}

async function upvote(id, btn) {
    const res = await fetch('/api/reports/' + id + '/upvote', { method: 'POST' });
    const data = await res.json();
    if (data.success) btn.textContent = '▲ ' + data.upvotes;
}

function timeAgo(iso) {
    const diff = Date.now() - new Date(iso).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return mins + 'm ago';
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return hrs + 'h ago';
    return Math.floor(hrs / 24) + 'd ago';
}

loadRecentReports();
