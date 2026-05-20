document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('templates-container');
    const paginationContainer = document.getElementById('templates-pagination');
    if (!container || !paginationContainer) return;

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
            return `http://localhost:3000/api/templates/${template.id_template}/download`;
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

        if (!Array.isArray(templates) || templates.length === 0) {
            container.innerHTML = '<p class="col-span-full text-center text-slate-500 py-12">Chưa có mẫu phiếu nào.</p>';
            paginationContainer.innerHTML = '';
            return;
        }

        const pageSize = 4;
        let currentPage = 1;
        const totalPages = Math.max(1, Math.ceil(templates.length / pageSize));

        const renderPage = (page) => {
            currentPage = Math.max(1, Math.min(page, totalPages));
            const startIndex = (currentPage - 1) * pageSize;
            const pageTemplates = templates.slice(startIndex, startIndex + pageSize);

            container.innerHTML = pageTemplates.map((template, index) => `
                <div class="bg-white border border-slate-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow group flex flex-col h-full">
                    <div class="h-56 bg-slate-100 overflow-hidden relative">
                        <img src="${getTemplatePreview(template)}" 
                             class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                             alt="${template.name}">
                    </div>
                    <div class="p-6 flex flex-col flex-grow">
                        <div class="flex items-start justify-between mb-4">
                            <div>
                                <h4 class="font-bold text-slate-900 text-body-lg">${template.name}</h4>
                                <p class="text-slate-500 text-body-sm">${getTemplateDescription(template)}</p>
                            </div>
                        </div>
                        <div class="flex items-center gap-4 mb-6 text-slate-500 text-body-sm mt-auto">
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
                           class="w-full flex items-center justify-center gap-2 bg-white border-2 border-primary text-primary font-bold py-2.5 rounded-lg hover:bg-primary hover:text-white transition-all text-sm">
                            <span class="material-symbols-outlined">download</span>
                            <span>Tải xuống PDF</span>
                        </a>
                    </div>
                </div>
            `).join('');

            renderPagination();
        };

        const renderPagination = () => {
            const pages = [];
            pages.push(`
                <button class="w-8 h-8 flex items-center justify-center border border-slate-200 rounded hover:bg-slate-50 transition-colors ${currentPage === 1 ? 'opacity-40 cursor-not-allowed' : ''}" ${currentPage === 1 ? 'disabled' : ''} data-page="prev">
                    <span class="material-symbols-outlined text-sm">chevron_left</span>
                </button>
            `);

            for (let i = 1; i <= totalPages; i += 1) {
                pages.push(`
                    <button class="w-8 h-8 flex items-center justify-center rounded font-bold text-xs transition-colors ${currentPage === i ? 'bg-primary text-white' : 'border border-slate-200 bg-white hover:bg-slate-50 text-slate-700'}" data-page="${i}">
                        ${i}
                    </button>
                `);
            }

            pages.push(`
                <button class="w-8 h-8 flex items-center justify-center border border-slate-200 rounded hover:bg-slate-50 transition-colors ${currentPage === totalPages ? 'opacity-40 cursor-not-allowed' : ''}" ${currentPage === totalPages ? 'disabled' : ''} data-page="next">
                    <span class="material-symbols-outlined text-sm">chevron_right</span>
                </button>
            `);

            paginationContainer.innerHTML = pages.join('');
            paginationContainer.querySelectorAll('button[data-page]').forEach(button => {
                button.addEventListener('click', () => {
                    const pageValue = button.getAttribute('data-page');
                    if (pageValue === 'prev') {
                        renderPage(currentPage - 1);
                    } else if (pageValue === 'next') {
                        renderPage(currentPage + 1);
                    } else {
                        renderPage(Number(pageValue));
                    }
                });
            });
        };

        renderPage(1);
    } catch (error) {
        console.error('Failed to fetch templates:', error);
        container.innerHTML = '<p class="col-span-full text-center text-red-500 py-12">Lỗi khi tải danh sách mẫu phiếu.</p>';
    }
});
