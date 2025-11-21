// scanner.js - uses ZXing BrowserMultiFormatReader

const codeReader = new ZXing.BrowserMultiFormatReader();
const videoElem = document.getElementById('video');
const resultDiv = document.getElementById('result');
const cameraSelect = document.getElementById('cameraSelect');
const uploadBtn = document.getElementById('uploadBtn');
const uploadInput = document.getElementById('uploadInput');
const diagnosticDiv = document.getElementById('diagnostic');
let currentDeviceId = null;
const ngrokUrlInput = document.getElementById('ngrokUrl');
const renderQrBtn = document.getElementById('renderQrBtn');
const qrCanvas = document.getElementById('qrCanvas');
const copyBtn = document.getElementById('copyBtn');

function getCSRF() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        const [k, v] = c.trim().split('=');
        if (k === name) return decodeURIComponent(v);
    }
    return '';
}

function showCameraMessage(html) {
    resultDiv.innerHTML = html;
}

async function listCameras() {
    try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
            throw new Error('navigator.mediaDevices not supported');
        }
        const devices = await codeReader.listVideoInputDevices();
        cameraSelect.innerHTML = '';
        devices.forEach((device, idx) => {
            const opt = document.createElement('option');
            opt.value = device.deviceId;
            opt.text = device.label || `Camera ${idx+1}`;
            cameraSelect.appendChild(opt);
        });
        if (devices.length) {
            currentDeviceId = devices[0].deviceId;
            cameraSelect.value = currentDeviceId;
        }
        return devices;
    } catch (e) {
        console.warn('Device listing failed', e);
        return [];
    }
}

async function startScanner(deviceId) {
    stopScanner();
    // Feature-detect getUserMedia
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showCameraMessage(
            `<div class="alert alert-warning">Camera not available in this browser. 
             For mobile devices open via HTTPS (eg. ngrok) or open the site directly on the device. 
             You can also upload a QR image below.</div>`
        );
        // show upload fallback
        uploadBtn.style.display = 'inline-block';
        return;
    }

    try {
        showCameraMessage('<div class="alert alert-info">Starting camera...</div>');
        await codeReader.decodeFromVideoDevice(deviceId || undefined, videoElem, (result, err) => {
            if (result) {
                handleResult(result.text);
            }
            if (err && !(err instanceof ZXing.NotFoundException)) {
                // NotFoundException is normal while scanning; log others
                console.error(err);
            }
        });
    } catch (e) {
        console.error('Camera start error', e);
        let friendly = `<div class="alert alert-danger">Camera error: ${e.message || e}. `;
        friendly += `For mobile devices, open via HTTPS (ngrok) or open the site on the device itself.</div>`;
        showCameraMessage(friendly);
        uploadBtn.style.display = 'inline-block';
    }
}

function stopScanner() {
    try { codeReader.reset(); } catch(e){ }
}

let lastQR = null;
let cooldown = false;

function handleResult(qrText) {
    if (cooldown || qrText === lastQR) return;
    lastQR = qrText;
    cooldown = true;
    fetch('/adminpanel/save-attendance/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRF(),
        },
        body: JSON.stringify({ qr: qrText })
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                  <h5>${data.student_name}</h5>
                  <p>${data.class} — ${data.time}</p>
                  ${data.photo_url ? `<img src="${data.photo_url}" style="max-width:120px; border-radius:8px;">` : ''}
                </div>`;
        } else {
            resultDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        }
    })
    .catch(err => {
        console.error('Network error', err);
        resultDiv.innerHTML = `<div class="alert alert-danger">Network error</div>`;
    })
    .finally(() => {
        setTimeout(() => { cooldown = false; }, 2000);
    });
}

// file-upload fallback decode
uploadInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    uploadBtn.style.display = 'none';
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    img.onload = async () => {
        try {
            // try decode from image element
            const result = await codeReader.decodeFromImageElement(img);
            handleResult(result.text);
        } catch (err) {
            console.error('Image decode failed', err);
            showCameraMessage('<div class="alert alert-danger">Could not decode QR from the uploaded image.</div>');
        } finally {
            URL.revokeObjectURL(img.src);
        }
    };
});

// UI events
if (cameraSelect) {
    cameraSelect.addEventListener('change', (e) => {
        currentDeviceId = e.target.value;
        stopScanner();
        startScanner(currentDeviceId);
    });
}

document.getElementById('switchBtn').addEventListener('click', async () => {
    const opts = Array.from(cameraSelect.options).map(o => o.value);
    if (!opts.length) return;
    const idx = opts.indexOf(currentDeviceId);
    const next = opts[(idx + 1) % opts.length];
    cameraSelect.value = next;
    currentDeviceId = next;
    stopScanner();
    startScanner(currentDeviceId);
});

document.getElementById('useLaptopToggle').addEventListener('change', (e) => {
    if (e.target.checked) {
        cameraSelect.disabled = true;
        stopScanner();
        startScanner(undefined); // default camera
    } else {
        cameraSelect.disabled = false;
        stopScanner();
        startScanner(currentDeviceId);
    }
});

uploadBtn.addEventListener('click', () => uploadInput.click());

// QR generator helper functions
function renderQr(url) {
    qrCanvas.innerHTML = '';
    if (!url) return;
    // use qrcode lib if available
    if (window.QRCode) {
        try {
            new QRCode(qrCanvas, { text: url, width: 180, height: 180 });
        } catch (e) {
            qrCanvas.textContent = url;
        }
    } else if (window.QRCodeGenerator) {
        qrCanvas.textContent = url;
    } else {
        // fallback: use Google Chart API (simple)
        const img = document.createElement('img');
        img.src = `https://chart.googleapis.com/chart?cht=qr&chs=180x180&chl=${encodeURIComponent(url)}`;
        img.alt = 'QR';
        qrCanvas.appendChild(img);
    }
}

renderQrBtn?.addEventListener('click', () => {
    const url = ngrokUrlInput.value?.trim();
    if (!url) return alert('Paste your ngrok HTTPS URL first');
    renderQr(url);
});

copyBtn?.addEventListener('click', async () => {
    const url = ngrokUrlInput.value?.trim();
    if (!url) return alert('Paste your ngrok HTTPS URL first');
    try { await navigator.clipboard.writeText(url); alert('Copied to clipboard'); } catch(e) { alert('Copy failed'); }
});

// Initialize with diagnostics and start
(async () => {
    // diagnostics: enumerate devices if possible
    diagnosticDiv.innerHTML = '<small>Detecting cameras...</small>';
    const devices = await listCameras();
    if (!devices.length) {
        diagnosticDiv.innerHTML = `<div class="alert alert-info">No video devices found or permission not yet granted.
            If on mobile, open via HTTPS (eg. ngrok) or load the site on the device. You can upload a QR image below.</div>`;
    } else {
        diagnosticDiv.innerHTML = `<div class="text-muted">Found ${devices.length} video device(s).</div>`;
    }
    uploadBtn.style.display = 'none';
    if (currentDeviceId) startScanner(currentDeviceId);
    else startScanner(undefined);
})();
