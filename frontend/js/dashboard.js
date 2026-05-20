document.addEventListener('DOMContentLoaded', async () => {
    console.log('Dashboard loaded');
    
    // Wire up quick navigation cards (Registered synchronously to prevent async blocking)
    const navBatchBtn = document.getElementById('nav-batch');
    const navInstantBtn = document.getElementById('nav-instant');

    if (navBatchBtn) {
        navBatchBtn.addEventListener('click', () => {
            window.location.href = 'batch.html';
        });
    }

    if (navInstantBtn) {
        navInstantBtn.addEventListener('click', () => {
            window.location.href = 'instant.html';
        });
    }
    
    // Load templates
    const templatesGrid = document.getElementById('templates-grid');
    if (templatesGrid) {
        try {
            const templates = await api.get('/templates');
            const getTemplatePreview = (template) => {
                if (!template) return 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="300"><rect width="100%" height="100%" fill="%23f1f5f9"/></svg>';
                const questions = template.totalQuestions || 20;
                const svg = `
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
                    <defs>
                        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" style="stop-color:#f8fafc;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#e2e8f0;stop-opacity:1" />
                        </linearGradient>
                        <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" style="stop-color:#1e3a8a;stop-opacity:1" />
                            <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
                        </linearGradient>
                    </defs>
                    <rect width="400" height="300" fill="url(#grad)" />
                    
                    <!-- Document Sheet -->
                    <rect x="80" y="30" width="240" height="240" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1"/>
                    
                    <!-- Header area inside sheet -->
                    <rect x="100" y="50" width="120" height="12" rx="3" fill="url(#accentGrad)" />
                    <rect x="100" y="70" width="200" height="6" rx="2" fill="#e2e8f0" />
                    <rect x="100" y="82" width="150" height="6" rx="2" fill="#e2e8f0" />
                    
                    <!-- OMR Grid Representation -->
                    <g transform="translate(100, 105)">
                        <!-- Question 1 -->
                        <text x="0" y="8" font-family="'Inter', sans-serif" font-size="8" font-weight="600" fill="#64748b">01</text>
                        <circle cx="20" cy="5" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="32" cy="5" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="44" cy="5" r="4" fill="#3b82f6" />
                        <circle cx="56" cy="5" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        
                        <!-- Question 2 -->
                        <text x="0" y="22" font-family="'Inter', sans-serif" font-size="8" font-weight="600" fill="#64748b">02</text>
                        <circle cx="20" cy="19" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="32" cy="19" r="4" fill="#3b82f6" />
                        <circle cx="44" cy="19" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="56" cy="19" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>

                        <!-- Question 3 -->
                        <text x="0" y="36" font-family="'Inter', sans-serif" font-size="8" font-weight="600" fill="#64748b">03</text>
                        <circle cx="20" cy="33" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="32" cy="33" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="44" cy="33" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="56" cy="33" r="4" fill="#3b82f6" />

                        <!-- Question 4 -->
                        <text x="0" y="50" font-family="'Inter', sans-serif" font-size="8" font-weight="600" fill="#64748b">04</text>
                        <circle cx="20" cy="47" r="4" fill="#3b82f6" />
                        <circle cx="32" cy="47" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="44" cy="47" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="56" cy="47" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                    </g>
                    
                    <!-- Right column of OMR Grid -->
                    <g transform="translate(200, 105)">
                        <!-- Question 5 -->
                        <text x="0" y="8" font-family="'Inter', sans-serif" font-size="8" font-weight="600" fill="#64748b">05</text>
                        <circle cx="20" cy="5" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="32" cy="5" r="4" fill="#3b82f6" />
                        <circle cx="44" cy="5" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="56" cy="5" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        
                        <!-- Question 6 -->
                        <text x="0" y="22" font-family="'Inter', sans-serif" font-size="8" font-weight="600" fill="#64748b">06</text>
                        <circle cx="20" cy="19" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="32" cy="19" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="44" cy="19" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="56" cy="19" r="4" fill="#3b82f6" />

                        <!-- Question 7 -->
                        <text x="0" y="36" font-family="'Inter', sans-serif" font-size="8" font-weight="600" fill="#64748b">07</text>
                        <circle cx="20" cy="33" r="4" fill="#3b82f6" />
                        <circle cx="32" cy="33" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="44" cy="33" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="56" cy="33" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>

                        <!-- Question 8 -->
                        <text x="0" y="50" font-family="'Inter', sans-serif" font-size="8" font-weight="600" fill="#64748b">08</text>
                        <circle cx="20" cy="47" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="32" cy="47" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                        <circle cx="44" cy="47" r="4" fill="#3b82f6" />
                        <circle cx="56" cy="47" r="4" fill="none" stroke="#94a3b8" stroke-width="1"/>
                    </g>

                    <!-- Footer OMR markers -->
                    <rect x="90" y="245" width="8" height="8" fill="#000000" />
                    <rect x="302" y="245" width="8" height="8" fill="#000000" />
                    <rect x="90" y="40" width="8" height="8" fill="#000000" />
                    <rect x="302" y="40" width="8" height="8" fill="#000000" />
                    
                    <!-- Dynamic Text Badge for questions -->
                    <g transform="translate(200, 205)">
                        <rect x="-45" y="0" width="90" height="18" rx="9" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1" />
                        <text x="0" y="12" text-anchor="middle" font-family="'Inter', sans-serif" font-size="8" font-weight="700" fill="#2563eb">${questions} CÂU HỎI</text>
                    </g>
                </svg>`;
                return 'data:image/svg+xml;utf8,' + encodeURIComponent(svg.trim());
            };
            const getTemplateDownloadUrl = (template) => {
                if (!template || !template.id_template) return '#';
                return `${window.api.BASE_URL}/templates/${template.id_template}/download`;
            };
            const getTemplateDescription = (template) => {
                if (!template) return 'Dung lượng cao';
                
                // Match descriptions based on totalQuestions and type
                if (template.totalQuestions === 20 && template.type === 'A4') {
                    return 'Hoàn hảo cho các bài kiểm tra ngắn';
                } else if (template.totalQuestions === 50 && template.type === 'A4') {
                    return 'Các kỳ thi giữa kỳ và cuối kỳ';
                } else if (template.totalQuestions === 120 && template.type !== 'A4') {
                    return 'Dung lượng cao tiêu chuẩn doanh nghiệp';
                }
                
                // Fallback for other templates
                return template.type === 'A4' ? 'Hoàn hảo cho các bài kiểm tra' : 'Dung lượng cao';
            };
            const displayTemplates = templates.slice(0, 3); // Show first 3
            
            templatesGrid.innerHTML = displayTemplates.map((template, index) => `
                <div class="bg-white border border-slate-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow group">
                    <div class="h-56 bg-slate-100 overflow-hidden relative">
                        <img src="${getTemplatePreview(template)}" 
                             class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                             alt="${template.name}">
                    </div>
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div>
                                <h4 class="font-bold text-slate-900 text-body-lg">${template.name}</h4>
                                <p class="text-slate-500 text-body-sm">${getTemplateDescription(template)}</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-4 mb-6 text-slate-500 text-body-sm">
                            <div class="flex items-center gap-1">
                                <span class="material-symbols-outlined text-sm">format_list_numbered</span>
                                <span>${template.totalQuestions} Câu hỏi</span>
                            </div>
                            <div class="flex items-center gap-1">
                                <span class="material-symbols-outlined text-sm">description</span>
                                <span>${template.type}</span>
                            </div>
                        </div>
                        <a href="${getTemplateDownloadUrl(template)}" 
                           download
                           class="w-full flex items-center justify-center gap-2 bg-white border-2 border-primary text-primary font-bold py-2.5 rounded-lg hover:bg-primary hover:text-white transition-all">
                            <span class="material-symbols-outlined">download</span>
                            <span>Tải xuống PDF</span>
                        </a>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Failed to load templates:', error);
            templatesGrid.innerHTML = '<p class="col-span-full text-center text-red-500 py-12">Lỗi khi tải mẫu phiếu.</p>';
        }
    }
    
    // Navigation and stats logic would go here
    
    // Load batches
    const batchesTableBody = document.getElementById('batches-table-body');
    const modal = document.getElementById('batch-details-modal');
    const modalBatchName = document.getElementById('modal-batch-name');
    const modalBatchMeta = document.getElementById('modal-batch-meta');
    const modalTableBody = document.getElementById('batch-details-table-body');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const closeModalFooterBtn = document.getElementById('close-modal-footer-btn');

    const currentUser = JSON.parse(localStorage.getItem('user') || 'null');
    if (!currentUser) {
        window.location.href = 'login.html';
        return;
    }

    let allBatches = [];

    const loadBatches = async () => {
        if (!batchesTableBody) return;
        try {
            const fetchedBatches = await api.get('/batches');
            allBatches = Array.isArray(fetchedBatches)
                ? fetchedBatches.filter(batch => {
                    return batch.id_user === currentUser.id_user || (batch.user && batch.user.id_user === currentUser.id_user);
                })
                : [];

            const userInfoElement = document.getElementById('dashboard-current-user');
            if (userInfoElement) {
                userInfoElement.textContent = `Đang hiển thị lịch sử chấm bài của: ${currentUser.fullName || currentUser.username}`;
            }
            console.log('Dashboard batches for user', currentUser.username, allBatches);

            if (allBatches.length === 0) {
                batchesTableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="px-6 py-8 text-center text-slate-400 italic">Chưa có đợt chấm nào cho người dùng hiện tại.</td>
                    </tr>
                `;
                return;
            }

            batchesTableBody.innerHTML = allBatches.map((batch, index) => {
                const dateStr = new Date(batch.time).toLocaleString('vi-VN');
                const resultName = batch.result ? batch.result.name : '<span class="text-slate-400 italic">Không có bộ đáp án</span>';
                return `
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-slate-800">${batch.name}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">${resultName}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-600">${batch.total_tests} bài thi</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">${dateStr}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                            <button class="view-detail-btn px-3 py-1.5 bg-blue-50 text-blue-700 hover:bg-blue-100 font-bold rounded-lg text-xs transition-colors" data-index="${index}">
                                Xem chi tiết
                            </button>
                        </td>
                    </tr>
                `;
            }).join('');

            // Add click listeners to buttons
            document.querySelectorAll('.view-detail-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const idx = e.currentTarget.getAttribute('data-index');
                    showBatchDetails(allBatches[idx]);
                });
            });

        } catch (error) {
            console.error('Failed to load batches:', error);
            batchesTableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="px-6 py-8 text-center text-red-500 font-semibold">Lỗi khi tải lịch sử chấm bài.</td>
                </tr>
            `;
        }
    };

    const showBatchDetails = (batch) => {
        if (!modal) return;
        
        modalBatchName.textContent = batch.name;
        const dateStr = new Date(batch.time).toLocaleString('vi-VN');
        const userFullName = batch.user ? batch.user.fullName || batch.user.username : 'Ẩn danh';
        const resultInfo = batch.result ? `${batch.result.name} (${batch.result.totalQuestions} câu)` : 'Không có';
        modalBatchMeta.innerHTML = `Người chấm: <strong>${userFullName}</strong> | Bộ đáp án: <strong>${resultInfo}</strong> | Thời gian: <strong>${dateStr}</strong>`;

        if (!batch.details || batch.details.length === 0) {
            modalTableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="px-6 py-6 text-center text-slate-400 italic">Không có chi tiết bài chấm nào trong đợt này.</td>
                </tr>
            `;
        } else {
            modalTableBody.innerHTML = batch.details.map(detail => `
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="px-6 py-3.5 whitespace-nowrap text-sm text-slate-700">${detail.file_name}</td>
                    <td class="px-6 py-3.5 whitespace-nowrap text-sm text-slate-800 font-medium">${detail.student_id || '<span class="text-slate-400 italic">Không nhận diện được</span>'}</td>
                    <td class="px-6 py-3.5 whitespace-nowrap text-sm text-slate-600">${detail.test_code || '---'}</td>
                    <td class="px-6 py-3.5 whitespace-nowrap text-sm font-bold ${detail.score >= 5 ? 'text-emerald-600' : 'text-red-500'}">${detail.score.toFixed(1)} / 10.0</td>
                </tr>
            `).join('');
        }

        modal.classList.remove('hidden');
    };

    const hideModal = () => {
        if (modal) modal.classList.add('hidden');
    };

    if (closeModalBtn) closeModalBtn.addEventListener('click', hideModal);
    if (closeModalFooterBtn) closeModalFooterBtn.addEventListener('click', hideModal);
    
    // Close modal on click outside content
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) hideModal();
        });
    }

    // Load initial batches
    loadBatches();
});
