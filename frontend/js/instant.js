document.addEventListener('DOMContentLoaded', () => {
    const startScanBtn = document.getElementById('start-scan-btn');
    const scanOptions = document.getElementById('scan-options');
    const fileInput = document.getElementById('instant-file-input');
    const camBtn = document.getElementById('cam-btn');
    const uploadBtn = document.getElementById('upload-btn');
    const resultPanel = document.getElementById('result-panel');
    const resultCode = document.getElementById('result-code');
    const resultSummary = document.getElementById('result-summary');
    const resultStats = document.getElementById('result-stats');
    const resultTableContainer = document.getElementById('result-table-container');
    const resultLoading = document.getElementById('result-loading');
    const resultError = document.getElementById('result-error');
    const resultErrorText = document.getElementById('result-error-text');
    const apiUrl = 'http://localhost:3000/api/omr/process';

    const showLoading = () => {
        resultLoading.classList.remove('hidden');
        resultPanel.classList.add('hidden');
        resultError.classList.add('hidden');
        resultErrorText.textContent = '';
    };

    const hideLoading = () => {
        resultLoading.classList.add('hidden');
    };

    const showError = (message) => {
        resultErrorText.textContent = message;
        resultError.classList.remove('hidden');
        resultPanel.classList.add('hidden');
    };

    const renderResult = (data) => {
        const studentId = data.studentId ? `Số báo danh: ${data.studentId}` : '';
        const paperCode = data.paperCode ? `Mã đề: ${data.paperCode}` : '';
        resultCode.innerHTML = `${studentId}${studentId && paperCode ? '<br/>' : ''}${paperCode}`;
        resultSummary.textContent = `Điểm: ${data.score}/${data.totalScore} — Đúng ${data.correct}, Sai ${data.wrong}, Bỏ trống ${data.blank}`;

        resultStats.innerHTML = `
            <div class="bg-slate-50 p-4 rounded-lg text-center">
                <p class="text-[10px] text-slate-500 uppercase font-bold">Tổng điểm</p>
                <p class="text-3xl font-black text-slate-900">${data.score}</p>
            </div>
            <div class="bg-slate-50 p-4 rounded-lg text-center">
                <p class="text-[10px] text-slate-500 uppercase font-bold">Đúng</p>
                <p class="text-3xl font-black text-emerald-600">${data.correct}</p>
            </div>
            <div class="bg-slate-50 p-4 rounded-lg text-center">
                <p class="text-[10px] text-slate-500 uppercase font-bold">Sai</p>
                <p class="text-3xl font-black text-red-600">${data.wrong}</p>
            </div>
            <div class="bg-slate-50 p-4 rounded-lg text-center">
                <p class="text-[10px] text-slate-500 uppercase font-bold">Bỏ trống</p>
                <p class="text-3xl font-black text-slate-900">${data.blank}</p>
            </div>
        `;

        const rows = data.details.map((item) => `
            <tr class="hover:bg-slate-50 transition-colors">
                <td class="px-4 py-3 text-sm font-semibold">${item.question}</td>
                <td class="px-4 py-3 text-sm">${item.studentAnswer}</td>
                <td class="px-4 py-3 text-sm">${item.correctAnswer}</td>
                <td class="px-4 py-3 text-sm ${item.status === 'đúng' ? 'text-emerald-600' : item.status === 'sai' ? 'text-red-600' : 'text-slate-500'} font-bold">${item.status}</td>
            </tr>
        `).join('');

        resultTableContainer.innerHTML = `
            <div class="px-6 py-4 border-b border-outline-variant bg-slate-50">
                <h4 class="font-medium text-slate-900">Chi tiết câu trả lời</h4>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-separate border-spacing-y-2">
                    <thead class="text-[11px] text-on-surface-variant font-bold uppercase tracking-wider">
                        <tr>
                            <th class="px-4 py-3">Câu</th>
                            <th class="px-4 py-3">Trả lời</th>
                            <th class="px-4 py-3">Đáp án</th>
                            <th class="px-4 py-3">Trạng thái</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-outline-variant">${rows}</tbody>
                </table>
            </div>
        `;

        resultPanel.classList.remove('hidden');
        resultTableContainer.classList.remove('hidden');
    };

    const uploadImage = async (file) => {
        showLoading();

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || data.message || 'Lỗi khi chấm ảnh');
            }

            renderResult(data);
        } catch (err) {
            showError(err.message);
        } finally {
            hideLoading();
        }
    };

    if (startScanBtn && scanOptions) {
        startScanBtn.addEventListener('click', () => {
            startScanBtn.classList.add('hidden');
            scanOptions.classList.remove('hidden');
        });
    }

    if (camBtn) {
        camBtn.addEventListener('click', () => {
            alert('Đang mở camera...');
        });
    }

    if (uploadBtn && fileInput) {
        uploadBtn.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                uploadImage(e.target.files[0]);
            }
        });
    }
});
