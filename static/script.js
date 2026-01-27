document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-upload');
    const form = document.querySelector('form');
    const loader = document.getElementById('loader-overlay');

    // Drag and Drop Visual Effects
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-active');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-active');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length) {
            fileInput.files = files;
            triggerUpload();
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length) {
            triggerUpload();
        }
    });

    function triggerUpload() {
        // Show loading animation
        loader.classList.add('active');
        // Submit the form after a tiny delay for visual smoothness
        setTimeout(() => form.submit(), 500);
    }

    // Animate elements on entry
    const cards = document.querySelectorAll('.fade-in-up');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    cards.forEach(card => observer.observe(card));
});