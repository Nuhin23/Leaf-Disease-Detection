/**
 * LeafAI – script_pages.js
 * Owner: Eva, Nuhin
 *
 * Handles all non-predict page interactions:
 *  1. Tab switching (Upload ↔ Camera)
 *  2. File upload with drag-and-drop support
 *  3. Shared image preview helpers (used by script_predict.js too)
 *
 * Note: showPreview() and clearPreview() are used by
 *       script_predict.js (camera capture), so this file
 *       must be loaded BEFORE script_predict.js in base.html.
 */

"use strict";

// ── Shorthand helpers ──────────────────────────────────────────
const $  = id  => document.getElementById(id);
const qs = sel => document.querySelector(sel);


/* ================================================================
   1. TAB SWITCHING  (Upload / Camera)
   ────────────────────────────────────────────────────────────────
   Toggles between the file-upload panel and the camera panel
   on the predict page. Also stops the camera when switching away.
================================================================ */

/**
 * switchTab(tab)
 * @param {string} tab - 'upload' or 'camera'
 */
function switchTab(tab) {
    const isUpload = tab === 'upload';

    $('uploadPanel').style.display = isUpload ? 'block' : 'none';
    $('cameraPanel').style.display = isUpload ? 'none'  : 'block';

    $('tabUpload').classList.toggle('active',  isUpload);
    $('tabCamera').classList.toggle('active', !isUpload);

    // Release the camera when switching to upload tab
    if (isUpload && typeof stopCamera === 'function') stopCamera();
}


/* ================================================================
   2. FILE UPLOAD  — file picker + drag-and-drop
   ────────────────────────────────────────────────────────────────
   Listens for file selection via in the <input type="file"> or
   a drag-and-drop onto the upload zone. Reads the file and
   calls showPreview() to display it.
================================================================ */

const imageInput = $('imageInput');
const uploadZone = $('uploadZone');

// File picker: shows preview when a file is selected
if (imageInput) {
    imageInput.addEventListener('change', () => {
        const file = imageInput.files[0];
        if (file) showFilePreview(file);
    });
}

// Drag-and-drop onto the upload  zone
if (uploadZone) {
    // Highlight zone on drag-over
    uploadZone.addEventListener('dragover', e => {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
    });
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-over');
    });

    // Drop: assign file to the input and show previews
    uploadZone.addEventListener('drop', e => {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            // Assign dropped file to the actual file input
            // so the form sends it correctly on submit
            const dt = new DataTransfer();
            dt.items.add(file);
            imageInput.files = dt.files;
            showFilePreview(file);
        }
    });
}

/**
 * showFilePreview(file)
 * Reads a File object with FileReader and displays it.
 * Also clears any previously captured camera data so the
 * form submits the file, not the base64 camera capture.
 * @param {File} file
 */
function showFilePreview(file) {
    const reader = new FileReader();
    reader.onload = e => showPreview(e.target.result);
    reader.readAsDataURL(file);
    $('capturedImageData').value = '';  // clear camera data
}


/* ================================================================
   3. SHARED PREVIEW HELPERS
   ────────────────────────────────────────────────────────────────
   showPreview()  — used by both file upload (above) and
                    camera capture (script_predict.js)
   clearPreview() — called by the ✕ Clear button in predict.html
================================================================ */

/**
 * showPreview(src)
 * Displays the image in the preview area and enables the submit button.
 * @param {string} src - data URL or image URL
 */
function showPreview(src) {
    $('previewImage').src          = src;
    $('previewWrap').style.display = 'block';
    const btn = $('submitBtn');
    if (btn) btn.disabled = false;
}


/**
 * clearPreview()
 * Hides the preview, clears all image data, disables submit button.
 * Called by the ✕ Clear button in predict.html.
 */
function clearPreview() {
    $('previewImage').src          = '';
    $('capturedImageData').value   = '';
    $('previewWrap').style.display = 'none';
    if (imageInput) imageInput.value = '';
    const btn = $('submitBtn');
    if (btn) btn.disabled = true;
}