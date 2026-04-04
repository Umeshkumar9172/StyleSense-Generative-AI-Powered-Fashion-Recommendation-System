document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analyzeForm');
    const photoInput = document.getElementById('photoInput');
    const preview = document.getElementById('preview');
    const previewContainer = document.getElementById('previewContainer');
    const submitBtn = document.getElementById('submitBtn');
    const spinner = document.getElementById('spinner');
    const btnText = document.getElementById('btnText');
    const alertContainer = document.getElementById('alertContainer');
    const resultsContainer = document.getElementById('resultsContainer');
    const placeholderContainer = document.getElementById('placeholderContainer');
    const loadingContainer = document.getElementById('loadingContainer');
    const loadingPreview = document.getElementById('loadingPreview');

    // Camera Elements
    const uploadTab = document.getElementById('uploadTab');
    const cameraTab = document.getElementById('cameraTab');
    const uploadMode = document.getElementById('uploadMode');
    const cameraMode = document.getElementById('cameraMode');
    const cameraFeed = document.getElementById('cameraFeed');
    const captureCanvas = document.getElementById('captureCanvas');
    const startCameraBtn = document.getElementById('startCameraBtn');
    const captureBtn = document.getElementById('captureBtn');
    const stopCameraBtn = document.getElementById('stopCameraBtn');
    const cameraPreview = document.getElementById('cameraPreview');
    const cameraPreviewContainer = document.getElementById('cameraPreviewContainer');
    const zoomControls = document.getElementById('zoomControls');
    const zoomSlider = document.getElementById('zoomSlider');
    const zoomOutBtn = document.getElementById('zoomOutBtn');
    const zoomInBtn = document.getElementById('zoomInBtn');
    const zoomLevel = document.getElementById('zoomLevel');
    const cameraLoading = document.getElementById('cameraLoading');
    
    let currentMode = 'upload';
    let mediaStream = null;
    let capturedImageData = null;
    let currentZoom = 1;

    // Initialize tab styles
    uploadTab.classList.add('active');
    uploadTab.classList.add('btn-secondary');
    uploadTab.classList.remove('btn-outline-secondary');
    cameraTab.classList.add('btn-outline-secondary');

    // Tab Switching
    uploadTab.addEventListener('click', function() {
        currentMode = 'upload';
        uploadTab.classList.add('active');
        uploadTab.classList.remove('btn-outline-secondary');
        uploadTab.classList.add('btn-secondary');
        cameraTab.classList.remove('active');
        cameraTab.classList.add('btn-outline-secondary');
        cameraTab.classList.remove('btn-secondary');
        uploadMode.style.display = 'block';
        cameraMode.style.display = 'none';
        stopCamera();
    });

    cameraTab.addEventListener('click', function() {
        currentMode = 'camera';
        cameraTab.classList.add('active');
        cameraTab.classList.remove('btn-outline-secondary');
        cameraTab.classList.add('btn-secondary');
        uploadTab.classList.remove('active');
        uploadTab.classList.add('btn-outline-secondary');
        uploadTab.classList.remove('btn-secondary');
        uploadMode.style.display = 'none';
        cameraMode.style.display = 'block';
    });

    // Camera Functions
    function startCamera() {
        console.log('🎥 Starting camera...');
        cameraLoading.style.display = 'block';
        cameraFeed.style.display = 'none';
        
        // Request camera with zoom capability
        const constraints = {
            video: {
                facingMode: 'user',
                width: { ideal: 1280 },
                height: { ideal: 720 },
                aspectRatio: { ideal: 16 / 9 }
            },
            audio: false
        };
        
        console.log('📹 Requesting camera with constraints:', constraints);
        
        navigator.mediaDevices.getUserMedia(constraints)
            .then(stream => {
                console.log('✅ Camera stream obtained:', stream);
                mediaStream = stream;
                
                // Assign stream to video element
                cameraFeed.srcObject = stream;
                
                // Wait for video to load
                cameraFeed.onloadedmetadata = function() {
                    console.log('✅ Video metadata loaded');
                    cameraFeed.play().catch(err => {
                        console.error('❌ Play error:', err);
                        showAlert('Could not start camera playback: ' + err.message, 'danger');
                    });
                };
                
                // Show camera after a brief delay
                setTimeout(() => {
                    cameraLoading.style.display = 'none';
                    cameraFeed.style.display = 'block';
                    startCameraBtn.style.display = 'none';
                    captureBtn.style.display = 'block';
                    stopCameraBtn.style.display = 'block';
                    zoomControls.style.display = 'block';
                    currentZoom = 1;
                    zoomSlider.value = 1;
                    updateZoomLevel();
                    console.log('✅ Camera UI updated');
                }, 100);
            })
            .catch(error => {
                console.error('❌ Camera error:', error);
                cameraLoading.style.display = 'none';
                
                let errorMsg = 'Camera access denied. ';
                if (error.name === 'NotAllowedError') {
                    errorMsg += 'Please allow camera permission in browser settings.';
                } else if (error.name === 'NotFoundError') {
                    errorMsg += 'No camera device found.';
                } else if (error.name === 'NotReadableError') {
                    errorMsg += 'Camera is currently unavailable or in use.';
                } else {
                    errorMsg += error.message;
                }
                
                showAlert(errorMsg, 'danger');
            });
    }

    function stopCamera() {
        console.log('🛑 Stopping camera...');
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => {
                console.log('Stopping track:', track.kind);
                track.stop();
            });
            mediaStream = null;
        }
        cameraFeed.style.display = 'none';
        cameraLoading.style.display = 'none';
        captureBtn.style.display = 'none';
        stopCameraBtn.style.display = 'none';
        zoomControls.style.display = 'none';
        startCameraBtn.style.display = 'block';
        currentZoom = 1;
        console.log('✅ Camera stopped');
    }
    
    function updateZoomLevel() {
        currentZoom = parseFloat(zoomSlider.value);
        cameraFeed.style.transform = `scaleX(-1) scale(${currentZoom})`;
        cameraFeed.style.transformOrigin = 'center';
        zoomLevel.textContent = currentZoom.toFixed(1) + 'x';
    }
    
    function capturePhotoWithZoom() {
        const context = captureCanvas.getContext('2d');
        const width = cameraFeed.videoWidth;
        const height = cameraFeed.videoHeight;
        
        captureCanvas.width = width;
        captureCanvas.height = height;
        
        // Draw the video frame
        context.save();
        context.scale(-1, 1);
        context.drawImage(cameraFeed, -width, 0, width, height);
        context.restore();
        
        // Convert to blob with quality compression for face detection
        captureCanvas.toBlob(blob => {
            capturedImageData = blob;
            
            // Create preview
            const reader = new FileReader();
            reader.onload = function(e) {
                cameraPreview.src = e.target.result;
                cameraPreview.style.display = 'block';
                cameraPreviewContainer.classList.add('show');
            };
            reader.readAsDataURL(blob);
            
            stopCamera();
            showAlert('✅ Photo captured! Ready to analyze.', 'success');
        }, 'image/jpeg', 0.95);
    }

    startCameraBtn.addEventListener('click', startCamera);
    stopCameraBtn.addEventListener('click', stopCamera);
    captureBtn.addEventListener('click', capturePhotoWithZoom);
    
    // Zoom Controls
    zoomSlider.addEventListener('input', updateZoomLevel);
    
    zoomOutBtn.addEventListener('click', function() {
        let newZoom = parseFloat(zoomSlider.value) - 0.5;
        if (newZoom < 1) newZoom = 1;
        zoomSlider.value = newZoom;
        updateZoomLevel();
    });
    
    zoomInBtn.addEventListener('click', function() {
        let newZoom = parseFloat(zoomSlider.value) + 0.5;
        if (newZoom > 5) newZoom = 5;
        zoomSlider.value = newZoom;
        updateZoomLevel();
    });

    // Image Preview for File Upload
    photoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                preview.src = event.target.result;
                previewContainer.classList.add('show');
            };
            reader.readAsDataURL(file);
        }
    });

    // Form Submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const gender = document.getElementById('gender').value;
        
        let fileToAnalyze = null;
        let previewSource = null;
        
        if (currentMode === 'upload') {
            fileToAnalyze = photoInput.files[0];
            previewSource = preview.src;
            
            if (!fileToAnalyze) {
                showAlert('Please select a photo', 'danger');
                return;
            }
        } else if (currentMode === 'camera') {
            if (!capturedImageData) {
                showAlert('Please capture a photo from camera', 'danger');
                return;
            }
            fileToAnalyze = capturedImageData;
            previewSource = cameraPreview.src;
        }

        // Disable submit button and show loader
        submitBtn.disabled = true;
        spinner.classList.add('show');
        btnText.textContent = 'Analyzing...';
        alertContainer.innerHTML = '';

        // Show loading animation
        loadingContainer.classList.add('show');
        loadingContainer.style.display = 'flex';
        loadingPreview.src = previewSource;
        resultsContainer.classList.remove('show');
        resultsContainer.style.display = 'none';
        placeholderContainer.style.display = 'none';

        const formData = new FormData();
        
        // Handle both File objects and Blob objects
        if (fileToAnalyze instanceof Blob) {
            formData.append('file', fileToAnalyze, 'camera_capture.jpg');
        } else {
            formData.append('file', fileToAnalyze);
        }
        
        formData.append('gender', gender);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                // displayResults handles hiding loading and showing results
                displayResults(data);
                showAlert('Analysis complete! Check your personalized style guide below.', 'success');
            } else {
                showAlert(data.message || 'An error occurred during analysis.', 'danger');
                placeholderContainer.style.display = 'block';
                resultsContainer.style.display = 'none';
                resultsContainer.classList.remove('show');
                loadingContainer.classList.remove('show');
            }
        } catch (error) {
            const errorMsg = error.message || 'Server error. Please try again.';
            showAlert(errorMsg, 'danger');
            console.error('Error:', error);
            loadingContainer.classList.remove('show');
            placeholderContainer.style.display = 'block';
            resultsContainer.style.display = 'none';
            resultsContainer.classList.remove('show');
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            spinner.classList.remove('show');
            btnText.textContent = 'Analyze & Style Me!';
        }
    });

    function showAlert(message, type) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        alertContainer.innerHTML = '';
        alertContainer.appendChild(alert);
    }

    function displayResults(data) {
        console.log('Displaying results...', data);
        
        // Hide placeholder and loading
        placeholderContainer.style.display = 'none';
        if (loadingContainer) {
            loadingContainer.classList.remove('show');
            loadingContainer.style.display = 'none';
        }
        
        // Show results container explicitly
        resultsContainer.style.display = 'block';
        resultsContainer.style.opacity = '1';
        resultsContainer.classList.add('show');

        // Update skin tone detection
        const skintoneEl = document.getElementById('skintoneText');
        const colorBoxEl = document.getElementById('colorBox');
        const faceshapeEl = document.getElementById('faceshapeText');

        if (skintoneEl) skintoneEl.textContent = data.skin_tone || 'Unknown';
        if (colorBoxEl) colorBoxEl.style.backgroundColor = data.average_color || '#eee';
        if (faceshapeEl) faceshapeEl.textContent = data.face_shape || 'Oval';

        const recs = data.recommendations;
        console.log('Recommendations object:', recs);
        
        if (!recs || Object.keys(recs).length === 0) {
            console.error('Empty or invalid recommendation data found');
            const recContent = document.getElementById('recommendationsContent');
            if (recContent) {
                recContent.innerHTML = `<div class="alert alert-danger">
                    <h6 class="fw-bold">No results found</h6>
                    <p class="small mb-0">The AI didn't provide any specific styling data. Please try again with a clearer photo.</p>
                </div>`;
            }
            return;
        }
        
        // Render Analysis Summary & Color Guide
        let recommendationsHtml = '';
        
        // Ensure recs.analysis exists or provide a default structure
        const analysis = recs.analysis || recs.style_analysis || recs.summary || {};
        if (analysis.style_summary || analysis.color_recommendation || analysis.avoid_colors) {
            recommendationsHtml += `
                <div class="analysis-section mb-4">
                    <div class="style-summary mb-3">
                        <p class="lead" style="font-size: 1.1rem; border-left: 4px solid #E85B89; padding-left: 15px;">${analysis.style_summary || analysis.summary || 'Your personalized style analysis.'}</p>
                    </div>
                    
                    <div class="row g-3">
                        <div class="col-md-6">
                            <div class="color-guide p-3 rounded-3 bg-light">
                                <h6 class="small fw-bold text-success mb-2">Recommended Colors</h6>
                                <div class="d-flex flex-wrap gap-2">
                                    ${(analysis.color_recommendation || analysis.recommended_colors || []).length > 0 ? (analysis.color_recommendation || analysis.recommended_colors || []).map(color => `
                                        <span class="badge rounded-pill bg-white text-dark border">${color}</span>
                                    `).join('') : '<span class="text-muted small">Colors matching your skin tone</span>'}
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="color-guide p-3 rounded-3 bg-light">
                                <h6 class="small fw-bold text-danger mb-2">Colors to Avoid</h6>
                                <div class="d-flex flex-wrap gap-2">
                                    ${(analysis.avoid_colors || analysis.colors_to_avoid || []).length > 0 ? (analysis.avoid_colors || analysis.colors_to_avoid || []).map(color => `
                                        <span class="badge rounded-pill bg-white text-muted border">${color}</span>
                                    `).join('') : '<span class="text-muted small">Colors that may not complement you</span>'}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`;
        }

        // Render Outfits by Occasion
        const outfits = recs.outfits || recs.outfit_recommendations || recs.recommendations || [];
        if (Array.isArray(outfits) && outfits.length > 0) {
            recommendationsHtml += `<div class="outfits-section">
                <h5 class="fw-bold mb-3 d-flex align-items-center">
                    <span class="me-2">👔</span> Outfit Recommendations
                </h5>`;
            
            outfits.forEach(outfit => {
                const items = outfit.items || outfit.products || [];
                if (Array.isArray(items) && items.length > 0) {
                    recommendationsHtml += `<div class="occasion-block mb-4">
                        <h6 class="text-primary border-bottom pb-2 d-flex justify-content-between">
                            <span>${outfit.occasion || 'Style Look'}</span>
                            <span class="badge bg-primary rounded-pill" style="font-size: 0.6rem;">${items.length} Items</span>
                        </h6>
                        <div class="row g-3">`;
                    
                    items.forEach(item => {
                        recommendationsHtml += `
                            <div class="col-md-6">
                                <div class="item-card p-3 border rounded-3 bg-light h-100 d-flex flex-column">
                                    <div class="d-flex justify-content-between align-items-start mb-2">
                                        <span class="badge bg-secondary" style="font-size: 0.7rem;">${item.category || 'Apparel'}</span>
                                        <img src="https://www.google.com/s2/favicons?domain=${(item.platform || 'amazon').toLowerCase()}.com" alt="" class="me-1" style="width:14px;">
                                    </div>
                                    <h6 class="mb-1" style="font-size: 0.95rem;">${item.item_name || item.name}</h6>
                                    <p class="small text-muted mb-2">Color: ${item.color || 'Matching'}</p>
                                    <p class="small mb-3 flex-grow-1">${item.reason || item.description || 'Perfect for your style'}</p>
                                    <a href="${item.search_link || item.link || '#'}" target="_blank" class="btn btn-sm btn-gradient w-100 mt-auto">
                                        Shop on ${item.platform || 'Platform'}
                                    </a>
                                </div>
                            </div>`;
                    });
                    
                    recommendationsHtml += `</div></div>`;
                }
            });
            recommendationsHtml += `</div>`;
        }

        // Render Accessories
        const accessories = recs.accessories || recs.accessory_recommendations || [];
        if (Array.isArray(accessories) && accessories.length > 0) {
            recommendationsHtml += `
                <div class="accessories-section mt-4">
                    <h5 class="fw-bold mb-3 d-flex align-items-center">
                        <span class="me-2">⌚</span> Accessories
                    </h5>
                    <div class="row g-3">
                        ${accessories.map(acc => `
                            <div class="col-md-6">
                                <div class="item-card p-3 border rounded-3 bg-white h-100 shadow-sm">
                                    <h6 class="mb-1" style="font-size: 0.9rem;">${acc.item_name || acc.name}</h6>
                                    <p class="small mb-2">${acc.reason || acc.description || 'Complements your look'}</p>
                                    <a href="${acc.search_link || acc.link || '#'}" target="_blank" class="btn btn-sm btn-link p-0 text-decoration-none" style="color: #E85B89;">
                                        Shop on ${acc.platform || 'Platform'} →
                                    </a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>`;
        }

        // Render Styling Tips
        const styling_tips = recs.styling_tips || recs.tips || recs.advice || [];
        if (Array.isArray(styling_tips) && styling_tips.length > 0) {
            recommendationsHtml += `<div class="tips-section mt-4 pt-3 border-top">
                <h6 class="fw-bold mb-3">Professional Styling Tips</h6>
                <div class="d-flex flex-column gap-2">`;
            styling_tips.forEach(tip => {
                recommendationsHtml += `
                    <div class="d-flex align-items-start gap-2 small">
                        <span class="text-primary">✦</span>
                        <span>${tip}</span>
                    </div>`;
            });
            recommendationsHtml += `</div></div>`;
        }

        if (!recommendationsHtml) {
            console.warn('recommendationsHtml is empty, but recs was not null. Recs content:', JSON.stringify(recs));
            recommendationsHtml = `
                <div class="alert alert-warning">
                    <h6 class="fw-bold">Partial Results Received</h6>
                    <p class="small mb-0">I received some data from the stylist but it wasn't formatted correctly. Please try one more time or refresh the page.</p>
                </div>`;
        }

        document.getElementById('recommendationsContent').innerHTML = recommendationsHtml;

        // Clear the old shopping guide
        const shoppingGrid = document.getElementById('shoppingGuide');
        if (shoppingGrid) {
            shoppingGrid.innerHTML = '<p class="text-muted small text-center">Your personalized shopping experience is integrated above.</p>';
        }

        // Scroll to results
        setTimeout(() => {
            resultsContainer.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }

    function markdownToHtml(markdown) {
        let html = markdown;

        // Headers
        html = html.replace(/^### (.*?)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.*?)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.*?)$/gm, '<h1>$1</h1>');

        // Bold and italic
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
        html = html.replace(/_(.*?)_/g, '<em>$1</em>');

        // Links
        html = html.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Lists
        html = html.replace(/^- (.*?)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>.*?<\/li>)/s, function(match) {
            return '<ul>' + match + '</ul>';
        });

        // Line breaks
        html = html.replace(/\n\n/g, '</p><p>');
        html = '<p>' + html + '</p>';

        // Clean up multiple <p> tags
        html = html.replace(/<\/p><p>/g, '</p><p>');

        return html;
    }

    // Smooth scroll to sections
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // StyleBot Logic
    const stylebotWidget = document.getElementById('stylebot-widget');
    const stylebotTrigger = document.getElementById('stylebot-trigger');
    const stylebotBubble = document.getElementById('stylebot-bubble');
    const stylebotClose = document.getElementById('stylebot-close');
    const stylebotChatContainer = document.getElementById('stylebot-chat-container');
    const stylebotMessages = document.getElementById('stylebot-messages');
    const stylebotInput = document.getElementById('stylebot-input');
    const stylebotSend = document.getElementById('stylebot-send');

    let chatHistory = [];

    // Toggle Chat
    stylebotTrigger.addEventListener('click', openChat);
    stylebotClose.addEventListener('click', closeChat);

    function openChat() {
        stylebotChatContainer.style.display = 'flex';
        stylebotBubble.style.display = 'none';
        stylebotTrigger.style.display = 'none';
        stylebotInput.focus();
    }

    function closeChat() {
        stylebotChatContainer.style.display = 'none';
        stylebotBubble.style.display = 'block';
        stylebotTrigger.style.display = 'flex';
    }

    stylebotSend.addEventListener('click', sendMessage);
    stylebotInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    async function sendMessage() {
        const message = stylebotInput.value.trim();
        if (!message) return;

        // Add user message to UI
        appendMessage('user', message);
        stylebotInput.value = '';

        // Show typing indicator
        const typingId = appendMessage('bot', '...', true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    history: chatHistory
                })
            });

            const data = await response.json();

            // Remove typing indicator
            removeMessage(typingId);

            if (data.success) {
                appendMessage('bot', data.response);
                chatHistory.push({ role: 'user', content: message });
                chatHistory.push({ role: 'assistant', content: data.response });
                // Keep history manageable
                if (chatHistory.length > 10) chatHistory = chatHistory.slice(-10);
            } else {
                appendMessage('bot', 'Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            console.error('Chat error:', error);
            removeMessage(typingId);
            appendMessage('bot', "Sorry, I'm having trouble connecting right now.");
        }
    }

    function appendMessage(role, text, isTyping = false) {
        if (role === 'bot') {
            const wrapper = document.createElement('div');
            wrapper.className = 'bot-message-wrapper';
            if (isTyping) wrapper.id = 'typing-indicator-wrapper';
            
            const icon = document.createElement('img');
            icon.src = '/static/bot-icon.svg';
            icon.className = 'bot-msg-icon';
            icon.alt = 'Bot Icon';
            
            const messageDiv = document.createElement('div');
            messageDiv.className = 'bot-message';
            if (isTyping) messageDiv.id = 'typing-indicator';
            messageDiv.textContent = text;
            
            wrapper.appendChild(icon);
            wrapper.appendChild(messageDiv);
            stylebotMessages.appendChild(wrapper);
            stylebotMessages.scrollTop = stylebotMessages.scrollHeight;
            return wrapper.id;
        } else {
            const messageDiv = document.createElement('div');
            messageDiv.className = `${role}-message`;
            messageDiv.textContent = text;
            stylebotMessages.appendChild(messageDiv);
            stylebotMessages.scrollTop = stylebotMessages.scrollHeight;
            return null;
        }
    }

    function removeMessage(id) {
        if (id) {
            const el = document.getElementById(id);
            if (el) el.remove();
        }
    }
});
