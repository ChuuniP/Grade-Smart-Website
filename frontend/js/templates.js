document.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('templates-container');
    if (!container) return;

    try {
        const templates = await api.get('/templates');
        
        if (templates.length === 0) {
            container.innerHTML = '<p class="col-span-full text-center text-slate-500 py-12">Chưa có mẫu phiếu nào.</p>';
            return;
        }

        container.innerHTML = templates.map(template => `
            <div class="bg-white border border-slate-200 rounded-xl overflow-hidden hover:shadow-md transition-shadow group">
                <div class="h-56 bg-slate-100 overflow-hidden relative">
                    <img src="${template.link_image || 'https://via.placeholder.com/400x300?text=No+Preview'}" 
                         class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                         alt="${template.name}">
                </div>
                <div class="p-5">
                    <div class="flex items-start justify-between mb-3">
                        <h3 class="font-bold text-slate-900 text-body-md line-clamp-1">${template.name}</h3>
                    </div>
                    <div class="space-y-1.5 mb-5 text-slate-500 text-[13px]">
                        <div class="flex justify-between">
                            <span>Mô tả</span>
                            <span class="font-semibold text-slate-700">${template.description || 'Không có'}</span>
                        </div>
                    </div>
                    <a href="http://localhost:3000/api/templates/${template.id_template}/download" 
                       target="_blank"
                       class="w-full flex items-center justify-center gap-2 bg-white border border-primary text-primary font-bold py-2 rounded-lg hover:bg-primary hover:text-white transition-all text-sm">
                        <span class="material-symbols-outlined text-lg">download</span>
                        <span>Tải xuống PDF</span>
                    </a>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Failed to fetch templates:', error);
        container.innerHTML = '<p class="col-span-full text-center text-red-500 py-12">Lỗi khi tải danh sách mẫu phiếu.</p>';
    }
});
