document.addEventListener('DOMContentLoaded', async () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const answerSetSelect = document.getElementById('batch-answer-set-select');
    const startBatchBtn = document.getElementById('start-batch-btn');
    const exportBtn = document.getElementById('export-btn');
    
    // Progress elements
    const progressText = document.getElementById('progress-text');
    const progressPercent = document.getElementById('progress-percent');
    const progressBar = document.getElementById('progress-bar');
    
    // Results table
    const resultsTableBody = document.getElementById('results-table-body');
    
    // Checklist/stats elements
    const totalFilesCount = document.getElementById('total-files-count');
    const validFilesCount = document.getElementById('valid-files-count');
    const errorFilesCount = document.getElementById('error-files-count');
    const checklistContainer = document.getElementById('checklist-container');
    
    // Chart and summary elements
    const averageScoreEl = document.getElementById('average-score');
    const maxScoreEl = document.getElementById('max-score');
    const minScoreEl = document.getElementById('min-score');
    
    const scoreBars = {
        '0-2': { bar: document.getElementById('bar-0-2'), text: document.getElementById('bar-text-0-2') },
        '2-4': { bar: document.getElementById('bar-2-4'), text: document.getElementById('bar-text-2-4') },
        '4-6': { bar: document.getElementById('bar-4-6'), text: document.getElementById('bar-text-4-6') },
        '6-8': { bar: document.getElementById('bar-6-8'), text: document.getElementById('bar-text-6-8') },
        '8-10': { bar: document.getElementById('bar-8-10'), text: document.getElementById('bar-text-8-10') }
    };

    let answerSets = [];
    let selectedAnswerSetId = localStorage.getItem('grade_smart_selected_answer_set_id') || null;
    let filesToProcess = [];
    let processedResults = [];
    let isProcessing = false;

    // Load available answer sets
    const loadAnswerSets = async () => {
        try {
            const results = await api.get('/results');
            answerSets = results.map(r => ({
                id: r.id_result,
                name: r.name,
                templateId: r.id_template,
                templateName: r.template ? r.template.name : 'Phiếu mẫu chuẩn',
                questionCount: r.totalQuestions,
                answers: r.details.reduce((arr, d) => {
                    arr[d.question - 1] = d.answer;
                    return arr;
                }, Array(r.totalQuestions).fill(''))
            })) || [];
            
            populateAnswerSetSelect();
        } catch (error) {
            console.error('Không thể tải danh sách bộ đáp án:', error);
            answerSetSelect.innerHTML = '<option value="">Lỗi tải dữ liệu</option>';
        }
    };

    const populateAnswerSetSelect = () => {
        answerSetSelect.innerHTML = '<option value="">Chọn bộ đáp án chuẩn</option>';
        
        if (answerSets.length === 0) {
            answerSetSelect.innerHTML = '<option value="">Chưa có bộ đáp án</option>';
            return;
        }

        answerSets.forEach(set => {
            const option = document.createElement('option');
            option.value = set.id;
            option.textContent = `${set.name} (${set.questionCount} câu - ${set.templateName})`;
            if (set.id === selectedAnswerSetId) {
                option.selected = true;
            }
            answerSetSelect.appendChild(option);
        });
    };

    answerSetSelect.addEventListener('change', (e) => {
        selectedAnswerSetId = e.target.value;
        if (selectedAnswerSetId) {
            localStorage.setItem('grade_smart_selected_answer_set_id', selectedAnswerSetId);
        } else {
            localStorage.removeItem('grade_smart_selected_answer_set_id');
        }
    });

    const dropZoneContent = document.getElementById('drop-zone-content');
    const originalDropZoneHTML = `
        <div class="w-16 h-16 rounded-full bg-blue-50 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <span class="material-symbols-outlined text-blue-800 text-3xl" data-icon="upload">upload</span>
        </div>
        <h3 class="text-body-lg font-semibold text-slate-800">Kéo và thả các tệp hình ảnh vào đây</h3>
        <p class="text-body-sm text-slate-500 mt-2 mb-4">Hỗ trợ JPG, PNG, tối đa 50MB (Chỉ nhận tệp hình ảnh)</p>
        <button type="button" class="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold rounded-lg text-sm transition-colors shadow-sm">
            Chọn ảnh từ thiết bị
        </button>
    `;

    // File selection / Drag and Drop
    if (dropZone && fileInput) {
        dropZone.onclick = (e) => {
            if (isProcessing) return;
            
            // Prevent double-clicking file input trigger if clicking input child itself
            if (e.target.id === 'file-input') return;
            
            fileInput.click();
        };

        dropZone.ondragover = (e) => {
            e.preventDefault();
            if (!isProcessing) {
                dropZone.classList.add('bg-blue-100', 'border-primary');
            }
        };

        dropZone.ondragleave = () => {
            dropZone.classList.remove('bg-blue-100', 'border-primary');
        };

        dropZone.ondrop = (e) => {
            e.preventDefault();
            dropZone.classList.remove('bg-blue-100', 'border-primary');
            if (!isProcessing) {
                handleFiles(e.dataTransfer.files);
            }
        };

        fileInput.onchange = (e) => {
            handleFiles(e.target.files);
        };
    }

    const updateDropZoneWithFiles = () => {
        if (!dropZoneContent) return;
        if (filesToProcess.length === 0) {
            dropZoneContent.innerHTML = originalDropZoneHTML;
            return;
        }

        const filesListHTML = filesToProcess.map(file => `
            <div class="flex items-center gap-2 text-slate-600 bg-white py-2 px-3 rounded-lg border border-slate-200 truncate shadow-sm">
                <span class="material-symbols-outlined text-sm text-slate-400">image</span>
                <span class="text-xs font-semibold truncate">${file.name}</span>
            </div>
        `).join('');

        dropZoneContent.innerHTML = `
            <div class="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center mb-3">
                <span class="material-symbols-outlined text-blue-800 text-2xl" data-icon="library_add">library_add</span>
            </div>
            <h4 class="font-semibold text-slate-800 text-sm mb-1">Đã thêm ${filesToProcess.length} tệp hình ảnh thành công:</h4>
            <p class="text-xs text-slate-400 mb-4">Bạn có thể nhấn bắt đầu chấm bài hoặc nhấp vào đây để thay đổi ảnh</p>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 w-full max-w-xl max-h-40 overflow-y-auto p-1.5 text-left mb-4 bg-slate-50/50 rounded-lg border border-slate-100 scrollbar-thin">
                ${filesListHTML}
            </div>

            <button type="button" class="px-4 py-2.5 bg-slate-200 hover:bg-slate-300 text-slate-700 font-semibold rounded-lg text-xs transition-colors shadow-sm">
                Chọn ảnh khác từ thiết bị
            </button>
        `;
    };

    const handleFiles = (files) => {
        const validFiles = Array.from(files).filter(file => file.type.startsWith('image/'));
        if (validFiles.length === 0) {
            alert('Vui lòng chọn hoặc kéo thả các tệp hình ảnh hợp lệ (PNG, JPG).');
            return;
        }

        const newFiles = validFiles.filter(file => {
            return !filesToProcess.some(existing =>
                existing.name === file.name && existing.size === file.size && existing.lastModified === file.lastModified
            );
        });

        if (newFiles.length === 0) {
            alert('Các ảnh bạn chọn đã nằm trong danh sách. Vui lòng chọn ảnh khác.');
            fileInput.value = '';
            return;
        }

        filesToProcess = filesToProcess.concat(newFiles);
        fileInput.value = '';
        updateDropZoneWithFiles();
        resetStatsAndCharts();
        renderChecklist();
    };

    const resetStatsAndCharts = () => {
        // Reset progress bar
        progressText.textContent = `Sẵn sàng chấm ${filesToProcess.length} tệp.`;
        progressPercent.textContent = '0%';
        progressBar.style.width = '0%';

        // Reset counts
        totalFilesCount.textContent = filesToProcess.length;
        validFilesCount.textContent = '0';
        errorFilesCount.textContent = '0';

        // Clear tables
        resultsTableBody.innerHTML = `
            <tr id="empty-table-row">
                <td colspan="5" class="px-6 py-8 text-center text-slate-400 italic">Chưa có kết quả chấm bài. Hãy tải ảnh lên và nhấn bắt đầu chấm.</td>
            </tr>
        `;

        // Clear chart
        Object.keys(scoreBars).forEach(range => {
            scoreBars[range].bar.style.height = '0%';
            scoreBars[range].text.textContent = '0 HS';
        });

        // Clear averages
        averageScoreEl.textContent = '--';
        maxScoreEl.textContent = '--';
        minScoreEl.textContent = '--';
    };

    const renderChecklist = () => {
        checklistContainer.innerHTML = '';
        filesToProcess.forEach((file, index) => {
            const item = document.createElement('div');
            item.className = 'flex items-center justify-between p-2.5 rounded border border-slate-100 text-xs bg-slate-50/50 hover:bg-slate-50 transition-all duration-200';
            item.id = `checklist-item-${index}`;
            item.innerHTML = `
                <span class="flex items-center gap-2 font-medium text-slate-700">
                    <span class="material-symbols-outlined text-sm text-slate-400" data-icon="image">image</span> 
                    ${file.name}
                </span>
                <span class="status-badge font-bold text-slate-400">Đang chờ...</span>
            `;
            checklistContainer.appendChild(item);
        });
    };

    // OMR Grading Logic
    const gradeWithAnswerSet = (omrResult, activeSet) => {
        let correct = 0;
        let wrong = 0;
        let blank = 0;
        const details = [];
        const questionCount = activeSet.questionCount;
        
        for (let i = 0; i < questionCount; i++) {
            const correctAnswer = activeSet.answers[i];
            const omrDetail = omrResult.details ? omrResult.details.find(d => d.question === (i + 1)) : null;
            const studentAnswer = omrDetail ? omrDetail.studentAnswer : 'Bỏ trống';
            
            let status = 'bỏ trống';
            let isCorrect = false;

            if (studentAnswer === 'Bỏ trống') {
                blank++;
                status = 'bỏ trống';
            } else if (studentAnswer === correctAnswer) {
                correct++;
                status = 'đúng';
                isCorrect = true;
            } else {
                wrong++;
                status = 'sai';
            }

            details.push({
                question: i + 1,
                studentAnswer,
                correctAnswer,
                status,
                isCorrect
            });
        }

        const score = Math.round((correct / questionCount) * 100) / 10;
        
        return {
            paperCode: omrResult.paperCode || '---',
            studentId: omrResult.studentId || 'Chưa nhận diện',
            studentCode: omrResult.studentCode || `HS-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`,
            score: score,
            totalScore: 10,
            totalQuestions: questionCount,
            correct: correct,
            wrong: wrong,
            blank: blank,
            details: details,
            timestamp: omrResult.timestamp || new Date().toISOString(),
            gradedImagePath: omrResult.gradedImagePath
        };
    };

    const processSingleFile = async (file, index, activeSet) => {
        const itemEl = document.getElementById(`checklist-item-${index}`);
        const statusBadge = itemEl ? itemEl.querySelector('.status-badge') : null;
        
        if (statusBadge) {
            statusBadge.className = 'status-badge font-bold text-blue-600 animate-pulse';
            statusBadge.textContent = 'Đang xử lý OMR...';
        }

        const formData = new FormData();
        formData.append('image', file);
        formData.append('answers', JSON.stringify(activeSet.answers));

        try {
            const omrResult = await api.post('/omr/process', formData, true);
            const graded = gradeWithAnswerSet(omrResult, activeSet);
            graded.filename = file.name;
            graded.isValid = true;

            // Update checklist status
            if (itemEl && statusBadge) {
                itemEl.classList.remove('border-slate-100');
                itemEl.classList.add('border-emerald-100', 'bg-emerald-50/20');
                statusBadge.className = 'status-badge font-bold text-emerald-600';
                statusBadge.textContent = 'Hợp lệ';
            }

            return graded;
        } catch (err) {
            console.error(`Error processing file ${file.name}:`, err);
            
            // Update checklist error status
            if (itemEl && statusBadge) {
                itemEl.classList.remove('border-slate-100');
                itemEl.classList.add('border-red-100', 'bg-red-50/20');
                statusBadge.className = 'status-badge font-bold text-red-600';
                statusBadge.textContent = 'Lỗi';
            }

            return {
                filename: file.name,
                studentId: 'Chưa nhận diện',
                paperCode: '---',
                score: 0.0,
                correct: 0,
                wrong: 0,
                blank: activeSet.questionCount,
                isValid: false,
                statusText: err.message || 'Lỗi nhận diện OMR'
            };
        }
    };

    const updateRealTimeStatsAndCharts = () => {
        const validResults = processedResults.filter(r => r.isValid);
        const errorResults = processedResults.filter(r => !r.isValid);

        validFilesCount.textContent = validResults.length;
        errorFilesCount.textContent = errorResults.length;

        // Render Results Table
        const emptyRow = document.getElementById('empty-table-row');
        if (emptyRow) emptyRow.remove();

        // Clear existing dynamic rows
        resultsTableBody.innerHTML = '';

        processedResults.forEach(res => {
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-50 transition-colors border-b border-slate-100';
            
            const badgeClass = res.isValid 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800';
            const statusText = res.isValid ? 'Hợp lệ' : (res.statusText || 'Lỗi OMR');
            
            tr.innerHTML = `
                <td class="px-6 py-4 text-body-sm font-semibold text-slate-700">${res.filename}</td>
                <td class="px-6 py-4 text-body-sm text-slate-600">${res.studentId}</td>
                <td class="px-6 py-4 text-body-sm text-slate-600">${res.paperCode}</td>
                <td class="px-6 py-4 text-body-sm font-bold text-slate-800">${res.isValid ? res.score.toFixed(1) : '--'}</td>
                <td class="px-6 py-4 text-right">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${badgeClass}">
                        ${statusText}
                    </span>
                </td>
            `;
            resultsTableBody.appendChild(tr);
        });

        if (validResults.length > 0) {
            const scores = validResults.map(r => r.score);
            const average = scores.reduce((sum, s) => sum + s, 0) / scores.length;
            const max = Math.max(...scores);
            const min = Math.min(...scores);

            averageScoreEl.textContent = average.toFixed(1);
            maxScoreEl.textContent = max.toFixed(1);
            minScoreEl.textContent = min.toFixed(1);

            // Distribution logic
            const distribution = { '0-2': 0, '2-4': 0, '4-6': 0, '6-8': 0, '8-10': 0 };
            scores.forEach(score => {
                if (score >= 0 && score <= 2) distribution['0-2']++;
                else if (score > 2 && score <= 4) distribution['2-4']++;
                else if (score > 4 && score <= 6) distribution['4-6']++;
                else if (score > 6 && score <= 8) distribution['6-8']++;
                else if (score > 8 && score <= 10) distribution['8-10']++;
            });

            const maxCount = Math.max(...Object.values(distribution));
            Object.keys(scoreBars).forEach(range => {
                const count = distribution[range];
                const heightPercentage = maxCount > 0 ? (count / maxCount) * 90 + 10 : 0;
                
                scoreBars[range].bar.style.height = `${heightPercentage}%`;
                scoreBars[range].text.textContent = `${count} HS`;
            });
        }
    };

    startBatchBtn.addEventListener('click', async () => {
        if (isProcessing) return;
        
        if (!selectedAnswerSetId) {
            alert('Vui lòng chọn bộ đáp án chuẩn trước khi bắt đầu chấm bài!');
            answerSetSelect.focus();
            return;
        }

        const activeSet = answerSets.find(s => s.id === selectedAnswerSetId);
        if (!activeSet) {
            alert('Bộ đáp án đã chọn không hợp lệ hoặc đã bị xóa. Vui lòng tải lại trang.');
            return;
        }

        if (filesToProcess.length === 0) {
            alert('Vui lòng tải hoặc kéo thả các ảnh phiếu trả lời vào trước.');
            return;
        }

        isProcessing = true;
        startBatchBtn.disabled = true;
        startBatchBtn.classList.add('opacity-50', 'cursor-not-allowed');
        answerSetSelect.disabled = true;
        dropZone.classList.add('opacity-40', 'cursor-not-allowed');

        processedResults = [];
        resetStatsAndCharts();

        const total = filesToProcess.length;
        
        // Loop and process sequentially for smooth real-time progress update
        for (let i = 0; i < total; i++) {
            const file = filesToProcess[i];
            
            // Update progress bar
            const percentVal = Math.round((i / total) * 100);
            progressText.textContent = `Đang chấm phiếu: ${file.name} (${i + 1}/${total})...`;
            progressPercent.textContent = `${percentVal}%`;
            progressBar.style.width = `${percentVal}%`;

            // Process OMR
            const result = await processSingleFile(file, i, activeSet);
            processedResults.push(result);

            // Update stats, tables, distribution chart, averages in real time
            updateRealTimeStatsAndCharts();
        }

        // Processing finished! Set progress bar to 100%
        progressText.textContent = `Đã hoàn tất chấm ${total} bài thi thi thành công!`;
        progressPercent.textContent = '100%';
        progressBar.style.width = '100%';

        // Save batch to server database
        try {
            const batchName = `Đợt chấm hàng loạt - ${new Date().toLocaleString('vi-VN')}`;
            const imagesPayload = processedResults.map(res => ({
                url: res.gradedImagePath || res.filename || '',
                score: res.score,
                studentId: res.studentId,
                paperCode: res.paperCode,
                gradedImagePath: res.gradedImagePath,
                status: res.isValid ? 'completed' : 'error'
            }));

            await api.post('/batches/upload', {
                resultId: activeSet.id,
                name: batchName,
                images: imagesPayload
            });

            console.log('Đợt chấm đã được lưu vào cơ sở dữ liệu.');
        } catch (dbErr) {
            console.error('Lỗi khi lưu đợt chấm vào CSDL:', dbErr);
            alert('Đợt chấm hoàn tất nhưng không thể lưu kết quả vào máy chủ: ' + dbErr.message);
        }

        // Clean up locks
        isProcessing = false;
        startBatchBtn.disabled = false;
        startBatchBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        answerSetSelect.disabled = false;
        dropZone.classList.remove('opacity-40', 'cursor-not-allowed');

        alert(`Chấm bài hàng loạt hoàn tất! Đã chấm ${total} bài.`);
    });

    // Export CSV Excel
    exportBtn.addEventListener('click', () => {
        if (processedResults.length === 0) {
            alert('Không có dữ liệu kết quả để xuất! Vui lòng hoàn thành đợt chấm trước.');
            return;
        }

        // Define CSV Headers and rows
        const headers = ['TEN_FILE', 'MA_HOC_SINH', 'MA_DE', 'CAU_DUNG', 'CAU_SAI', 'CAU_TRONG', 'DIEM_SO', 'TRANG_THAI'];
        const csvRows = [headers.join(',')];

        processedResults.forEach(res => {
            const row = [
                `"${res.filename}"`,
                `"${res.studentId}"`,
                `"${res.paperCode}"`,
                res.isValid ? res.correct : 0,
                res.isValid ? res.wrong : 0,
                res.isValid ? res.blank : 0,
                res.isValid ? res.score.toFixed(1) : '0.0',
                `"${res.isValid ? 'Hợp lệ' : 'Lỗi OMR'}"`
            ];
            csvRows.push(row.join(','));
        });

        // Add UTF-8 BOM so Vietnamese characters display correctly in Microsoft Excel
        const csvContent = '\uFEFF' + csvRows.join('\n');
        
        // Trigger download
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        
        const timestamp = new Date().toISOString().slice(0, 10);
        link.setAttribute('download', `Ket_Qua_Cham_Hang_Loat_${timestamp}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    // Run setup
    await loadAnswerSets();
});
