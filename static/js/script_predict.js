/**
 * LeafAI – script_predict.js
 * Owner: YOUR NAME
 *
 * Handles everything related to the predict page:
 *  1. Camera stream, frame capture, canvas preprocessing
 *  2. Loading spinner + animated step sequencer on form submit
 *  3. Staggered result reveal animation on page load
 *  4. Confidence bar + counter animation
 *  5. Confidence tier label (High / Moderate / Low)
 *
 * Depends on: script_pages.js (for showPreview, switchTab helpers)
 */

"use strict";


/* ================================================================
   1. CAMERA  — open stream, capture frame, preprocess
   ────────────────────────────────────────────────────────────────
   Uses the browser MediaDevices API to access the device camera.
   On capture, draws the frame to a hidden <canvas> at 160×160px
   (matching the model's expected input size), converts to base64
   JPEG, and stores it in the hidden form field for Flask to read.
================================================================ */

let mediaStream = null;   // holds the active MediaStream object

/**
 * startCamera()
 * Requests camera permission and starts the live video stream.
 * Prefers the rear-facing camera on mobile (facingMode: environment).
 */
async function startCamera() {
    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment' }
        });
        document.getElementById('video').srcObject = mediaStream;
        document.getElementById('startCameraBtn').style.display = 'none';
        document.getElementById('captureBtn').style.display     = 'block';
    } catch (err) {
        alert('Camera access denied or not available: ' + err.message);
    }
}

/**
 * stopCamera()
 * Stops all camera tracks to release the device
 * (prevents the "camera in use" indicator from staying on).
 */
function stopCamera() {
    if (mediaStream) {
        mediaStream.getTracks().forEach(t => t.stop());
        mediaStream = null;
    }
    const video = document.getElementById('video');
    if (video) video.srcObject = null;

    const s = document.getElementById('startCameraBtn');
    const c = document.getElementById('captureBtn');
    if (s) s.style.display = 'block';
    if (c) c.style.display = 'none';
}

/**
 * captureFrame()
 * Grabs the current video frame, resizes it to 160×160 on a canvas,
 * converts it to a base64 JPEG string, stores it in the hidden input,
 * then stops the camera.
 *
 * The 160×160 resize matches the model's expected input dimensions.
 * Pixel normalisation (÷255 or backbone preprocess) happens server-side.
 */
function captureFrame() {
    const video  = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const SIZE   = 160;

    canvas.width = canvas.height = SIZE;
    canvas.getContext('2d').drawImage(video, 0, 0, SIZE, SIZE);

    // Convert to base64 JPEG — Flask decodes this in the predict route
    const dataUrl = canvas.toDataURL('image/jpeg', 0.95);
    document.getElementById('capturedImageData').value = dataUrl;

    showPreview(dataUrl);   // defined in script_pages.js
    stopCamera();
}


/* ================================================================
   2. LOADING SPINNER + ANIMATED STEP SEQUENCER
   ────────────────────────────────────────────────────────────────
   When the form submits:
     a) Submit button becomes a spinner ("Analyzing...")
     b) The right result panel shows the loading overlay
     c) Step labels light up one-by-one to signal progress stages
================================================================ */

const predictForm = document.getElementById('predictForm');

if (predictForm) {
    predictForm.addEventListener('submit', () => {
        const imageInput = document.getElementById('imageInput');
        const hasFile    = imageInput && imageInput.files.length > 0;
        const hasCapture = document.getElementById('capturedImageData').value.length > 0;
        if (!hasFile && !hasCapture) return;

        // a) Transform submit button
        const label   = document.getElementById('submitLabel');
        const arrow   = document.getElementById('submitArrow');
        const spinner = document.getElementById('submitSpinner');
        const btn     = document.getElementById('submitBtn');

        if (label)   label.textContent       = 'Analyzing...';
        if (arrow)   arrow.style.display     = 'none';
        if (spinner) spinner.style.display   = 'inline-block';
        if (btn)     btn.disabled            = true;

        // b) Show loading overlay on result panel
        const resultPanel = document.getElementById('resultPanel');
        if (resultPanel) resultPanel.classList.add('is-loading');

        // c) Light up step labels sequentially
        //    Timings are cosmetic — they make the wait feel purposeful
        const stepDelays = [0, 600, 1300, 2100];
        ['step1', 'step2', 'step3', 'step4'].forEach((id, i) => {
            setTimeout(() => {
                const el = document.getElementById(id);
                if (el) el.classList.add('step-active');
            }, stepDelays[i]);
        });

        // Form submits normally — Flask handles the response
    });
}


/* ================================================================
   3. RESULT REVEAL — staggered fade-in on page load
   ────────────────────────────────────────────────────────────────
   When Flask returns results, each .reveal-item fades+slides in
   one by one with a 120ms gap, avoiding the "everything at once" look.
================================================================ */

window.addEventListener('DOMContentLoaded', () => {

    // Stagger each .reveal-item with incremental animation-delay
    document.querySelectorAll('.reveal-item').forEach((el, i) => {
        el.style.animationDelay = `${i * 120}ms`;
        el.classList.add('reveal-animate');
    });


    /* ============================================================
       4. CONFIDENCE BAR + COUNTER ANIMATION
       ──────────────────────────────────────────────────────────
       Animates:
         - The fill bar width (via CSS transition)
         - A counting number from 0.0% up to the real value
       Both finish at exactly the same time (1200ms).
    ============================================================ */

    const fill = document.getElementById('confidenceFill');
    const text = document.getElementById('confidenceText');
    const tier = document.getElementById('confidenceTier');

    if (!fill) return;

    const targetPct = Math.min(parseFloat(fill.dataset.confidence) || 0, 100);

    // Small delay so the page paints before the animation starts
    setTimeout(() => {

        // Trigger bar fill (CSS transition does the easing)
        fill.style.width = targetPct + '%';

        // Animate the counter number in sync (1200ms, ease-out cubic)
        const duration  = 1200;
        const startTime = performance.now();

        function countUp(now) {
            const elapsed  = now - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const eased    = 1 - Math.pow(1 - progress, 3);  // ease-out cubic
            const current  = Math.round(eased * targetPct * 10) / 10;

            if (text) text.textContent = current.toFixed(1) + '%';

            if (progress < 1) {
                requestAnimationFrame(countUp);
            } else {
                // Lock to exact final value
                if (text) text.textContent = targetPct.toFixed(1) + '%';

                /* ================================================
                   5. CONFIDENCE TIER LABEL
                   ────────────────────────────────────────────────
                   Appears after counting finishes.
                   Color-coded: green / gold / red
                ================================================ */
                if (tier) {
                    if (targetPct >= 80) {
                        tier.textContent = '✔ High confidence';
                        tier.className   = 'confidence-tier tier-high';
                    } else if (targetPct >= 50) {
                        tier.textContent = '◈ Moderate confidence — consider a second check';
                        tier.className   = 'confidence-tier tier-mid';
                    } else {
                        tier.textContent = '⚠ Low confidence — result may be inaccurate';
                        tier.className   = 'confidence-tier tier-low';
                    }
                    tier.classList.add('tier-visible');
                }
            }
        }

        requestAnimationFrame(countUp);

    }, 300);  // 300ms initial delay after page load

});
