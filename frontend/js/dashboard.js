document.addEventListener('DOMContentLoaded', async () => {
    console.log('Dashboard loaded');
    
    // Load templates
    const templatesGrid = document.getElementById('templates-grid');
    if (templatesGrid) {
        try {
            const templates = await api.get('/templates');
            const displayTemplates = templates.slice(0, 3); // Show first 3
            
            templatesGrid.innerHTML = displayTemplates.map((template, index) => `
                <div class="bg-white border border-slate-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow group ${index === 1 ? 'border-primary/20 shadow-sm' : ''}">
                    <div class="h-56 bg-slate-100 overflow-hidden relative">
                        <img src="${template.linkImage || 'https://via.placeholder.com/400x300?text=No+Preview'}" 
                             class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                             alt="${template.name}">
                    </div>
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div>
                                <h4 class="font-bold text-slate-900 text-body-lg">${template.name}</h4>
                                <p class="text-slate-500 text-body-sm">${template.type === 'A4' ? 'Hoàn hảo cho các bài kiểm tra' : 'Dung lượng cao'}</p>
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
                        <a href="http://localhost:3000/api/templates/${template.id_template}/download" 
                           target="_blank"
                           class="w-full flex items-center justify-center gap-2 ${index === 1 ? 'bg-primary text-white shadow-md' : 'bg-white border-2 border-primary text-primary'} font-bold py-2.5 rounded-lg hover:bg-primary hover:text-white transition-all">
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
});
