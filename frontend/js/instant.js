document.addEventListener('DOMContentLoaded', async () => {
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
    const newAnswerSetBtn = document.getElementById('new-answer-set-btn');
    const answerSetForm = document.getElementById('answer-set-form');
    const answerSetList = document.getElementById('answer-set-list');
    const templateSelect = document.getElementById('answer-template-select');
    const questionCountInput = document.getElementById('answer-question-count');
    const answerSetNameInput = document.getElementById('answer-set-name');
    const answerFieldsContainer = document.getElementById('answer-fields-container');
    const saveAnswerSetBtn = document.getElementById('save-answer-set-btn');
    const cancelAnswerSetBtn = document.getElementById('cancel-answer-set-btn');
    const answerSetsContent = document.getElementById('answer-sets-content');
    const toggleAnswerSetsBtn = document.getElementById('toggle-answer-sets-btn');
    const toggleAnswerSetsIcon = document.getElementById('toggle-answer-sets-icon');
    const apiUrl = 'http://localhost:3000/api/omr/process';

    const gradedImageContainer = document.getElementById('graded-image-container');
    const gradedImage = document.getElementById('graded-image');
    const scanContainer = document.getElementById('scan-container');

    let availableTemplates = [];
    let answerSets = [];
    let selectedAnswerSetId = localStorage.getItem('grade_smart_selected_answer_set_id') || null;
    let lastOmrResult = null;
    let collapsedAnswerSetIds = JSON.parse(localStorage.getItem('grade_smart_collapsed_answer_set_ids')) || [];

    const showLoading = () => {
        resultLoading.classList.remove('hidden');
        resultPanel.classList.add('hidden');
        resultError.classList.add('hidden');
        resultErrorText.textContent = '';
        if (gradedImageContainer) {
            gradedImageContainer.classList.add('hidden');
        }
        if (scanContainer) {
            scanContainer.classList.remove('hidden');
        }
    };

    const hideLoading = () => {
        resultLoading.classList.add('hidden');
    };

    const showError = (message) => {
        resultErrorText.textContent = message;
        resultError.classList.remove('hidden');
        resultPanel.classList.add('hidden');
        if (gradedImageContainer) {
            gradedImageContainer.classList.add('hidden');
        }
        if (scanContainer) {
            scanContainer.classList.remove('hidden');
        }
    };

    const renderResult = (data) => {
        const studentId = data.studentId ? `Số báo danh: ${data.studentId}` : '';
        const paperCode = data.paperCode ? `Mã đề: ${data.paperCode}` : '';
        resultCode.innerHTML = `${studentId}${studentId && paperCode ? '<br/>' : ''}${paperCode}`;
        resultSummary.textContent = `Điểm: ${data.score}/${data.totalScore} — Đúng ${data.correct}, Sai ${data.wrong}, Bỏ trống ${data.blank}`;

        // Hiển thị ảnh sau khi chấm (nếu backend trả về)
        if (data.gradedImagePath && gradedImage && gradedImageContainer) {
            gradedImage.src = `http://localhost:3000/uploads/${data.gradedImagePath}`;
            gradedImageContainer.classList.remove('hidden');
            if (scanContainer) {
                scanContainer.classList.add('hidden');
            }
        }

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

    const gradeWithAnswerSet = (omrResult, activeSet) => {
        let correct = 0;
        let wrong = 0;
        let blank = 0;
        const details = [];

        const questionCount = activeSet.questionCount;
        
        for (let i = 0; i < questionCount; i++) {
            const correctAnswer = activeSet.answers[i]; // e.g. 'A'
            
            // Get student answer from OMR result
            const omrDetail = omrResult.details.find(d => d.question === (i + 1));
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
            paperCode: omrResult.paperCode,
            studentId: omrResult.studentId,
            studentCode: omrResult.studentCode,
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

    const uploadImage = async (file, activeSet) => {
        showLoading();

        const formData = new FormData();
        formData.append('image', file);
        formData.append('answers', JSON.stringify(activeSet.answers));

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || data.message || 'Lỗi khi chấm ảnh');
            }

            // Save raw OMR result to allow dynamic editing/re-grading
            lastOmrResult = data;

            // Grade using selected answer set!
            const gradedResult = gradeWithAnswerSet(data, activeSet);
            renderResult(gradedResult);
        } catch (err) {
            showError(err.message);
        } finally {
            hideLoading();
        }
    };

    const populateTemplateSelect = () => {
        templateSelect.innerHTML = '<option value="">Chọn mẫu phiếu</option>';

        if (!availableTemplates.length) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Chưa có mẫu phiếu';
            option.disabled = true;
            templateSelect.appendChild(option);
            templateSelect.disabled = true;
            return;
        }

        availableTemplates.forEach((template) => {
            const option = document.createElement('option');
            option.value = template.id_template || template.id || template.id_template;
            option.textContent = template.name;
            templateSelect.appendChild(option);
        });
        templateSelect.disabled = false;
    };

    const loadTemplates = async () => {
        try {
            const templates = await api.get('/templates');
            availableTemplates = templates || [];
        } catch (error) {
            console.error('Không thể tải danh sách mẫu phiếu:', error);
            availableTemplates = [];
        }
        populateTemplateSelect();
    };

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
            
            // If the previously selected set is not found in database, clear selected set
            if (selectedAnswerSetId && !answerSets.some(s => s.id === selectedAnswerSetId)) {
                if (answerSets.length > 0) {
                    selectedAnswerSetId = answerSets[0].id;
                } else {
                    selectedAnswerSetId = null;
                }
                localStorage.setItem('grade_smart_selected_answer_set_id', selectedAnswerSetId || '');
            }
        } catch (error) {
            console.error('Không thể tải danh sách bộ đáp án:', error);
            answerSets = [];
        }
    };

    const createAnswerFields = (count) => {
        answerFieldsContainer.innerHTML = '';
        answerFieldsContainer.className = 'mt-6 grid gap-3 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4';
        const safeCount = Math.min(Math.max(count, 1), 200);

        for (let index = 1; index <= safeCount; index += 1) {
            const field = document.createElement('div');
            field.className = 'flex items-center gap-3 p-2.5 rounded-2xl border border-slate-100 bg-slate-50/20 hover:bg-slate-50/60 hover:border-slate-200 transition-all';
            field.innerHTML = `
                <div class="rounded-xl bg-slate-100 px-2 py-1.5 text-xs font-semibold text-slate-700 text-center min-w-[52px]">Câu ${index}</div>
                <div class="flex gap-2 items-center" data-question-index="${index}">
                    <button type="button" class="choice-btn w-8 h-8 flex items-center justify-center font-bold text-xs rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 hover:border-slate-400 transition cursor-pointer select-none" data-choice="A">A</button>
                    <button type="button" class="choice-btn w-8 h-8 flex items-center justify-center font-bold text-xs rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 hover:border-slate-400 transition cursor-pointer select-none" data-choice="B">B</button>
                    <button type="button" class="choice-btn w-8 h-8 flex items-center justify-center font-bold text-xs rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 hover:border-slate-400 transition cursor-pointer select-none" data-choice="C">C</button>
                    <button type="button" class="choice-btn w-8 h-8 flex items-center justify-center font-bold text-xs rounded-full border border-slate-300 bg-white text-slate-700 hover:bg-slate-100 hover:border-slate-400 transition cursor-pointer select-none" data-choice="D">D</button>
                    <input type="hidden" name="answer-${index}" value="" />
                </div>
            `;
            answerFieldsContainer.appendChild(field);
        }

        // Add event listeners to the choice buttons
        answerFieldsContainer.querySelectorAll('.choice-btn').forEach((btn) => {
            btn.addEventListener('click', (e) => {
                const parent = btn.parentElement;
                const choice = btn.getAttribute('data-choice');
                const hiddenInput = parent.querySelector('input[type="hidden"]');

                // Deselect all sibling choice buttons
                parent.querySelectorAll('.choice-btn').forEach((sibling) => {
                    sibling.classList.remove('bg-primary', 'border-primary', 'text-white', 'shadow-md', 'ring-2', 'ring-blue-100');
                    sibling.classList.add('bg-white', 'border-slate-300', 'text-slate-700', 'hover:bg-slate-100', 'hover:border-slate-400');
                });

                // Select current button
                btn.classList.remove('bg-white', 'border-slate-300', 'text-slate-700', 'hover:bg-slate-100', 'hover:border-slate-400');
                btn.classList.add('bg-primary', 'border-primary', 'text-white', 'shadow-md', 'ring-2', 'ring-blue-100');
                
                hiddenInput.value = choice;
            });
        });
    };

    const renderAnswerSetList = () => {
        if (!answerSets.length) {
            answerSetList.innerHTML = '<div class="text-slate-500 italic text-center py-4 bg-slate-50 rounded-xl border border-dashed border-slate-200">Chưa có bộ đáp án nào. Nhấn nút phía trên để tạo mới bộ đáp án của bạn.</div>';
            return;
        }

        answerSetList.innerHTML = answerSets.map((set, index) => {
            const isSelected = set.id === selectedAnswerSetId;
            const borderClass = isSelected ? 'border-emerald-500 bg-emerald-50/20 ring-2 ring-emerald-500/20' : 'border-slate-200 bg-slate-50';
            const badgeClass = isSelected ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-700';
            const selectButtonText = isSelected ? '✓ Đang chọn làm đáp án chuẩn' : 'Chọn làm đáp án chuẩn';
            const selectButtonClass = isSelected 
                ? 'bg-emerald-600 hover:bg-emerald-700 text-white' 
                : 'bg-white hover:bg-slate-50 text-slate-700 border border-slate-300';

            const isAnswersCollapsed = collapsedAnswerSetIds.includes(set.id);
            const toggleAnswersIcon = isAnswersCollapsed ? 'expand_more' : 'expand_less';
            const answersDisplayClass = isAnswersCollapsed ? 'hidden' : '';

            return `
                <div class="mb-4 rounded-2xl border p-5 transition-all duration-200 ${borderClass}" data-set-id="${set.id}">
                    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                        <div>
                            <div class="flex items-center gap-2">
                                <p class="font-bold text-slate-900 text-base">${set.name}</p>
                                <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${badgeClass}">Mẫu: ${set.templateName}</span>
                            </div>
                            <p class="text-xs text-slate-500 mt-1">${set.questionCount} câu hỏi · Tự động chấm theo bộ đáp án này</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <button class="select-set-btn px-4 py-2 text-xs font-semibold rounded-lg shadow-sm transition ${selectButtonClass}" data-id="${set.id}">
                                ${selectButtonText}
                            </button>
                            <button class="toggle-answers-btn p-2 text-slate-500 hover:bg-slate-200/60 rounded-lg transition" title="Hiện/Ẩn danh sách câu hỏi" data-id="${set.id}">
                                <span class="material-symbols-outlined text-base">${toggleAnswersIcon}</span>
                            </button>
                            <button class="delete-set-btn p-2 text-red-600 hover:bg-red-50 rounded-lg transition" title="Xóa bộ đáp án" data-id="${set.id}">
                                <span class="material-symbols-outlined text-base">delete</span>
                            </button>
                        </div>
                    </div>
                    <div class="mt-4 grid gap-2 grid-cols-2 sm:grid-cols-5 md:grid-cols-10 transition-all duration-200 ${answersDisplayClass}">
                        ${set.answers.map((answer, answerIndex) => `
                            <div class="question-edit-btn rounded-lg border border-slate-200 bg-white px-2 py-1.5 text-center text-xs shadow-sm cursor-pointer hover:bg-blue-50 hover:border-blue-300 hover:scale-105 active:scale-95 transition-all relative"
                                 data-set-id="${set.id}"
                                 data-answer-index="${answerIndex}"
                                 data-current-answer="${answer || ''}">
                                <span class="font-semibold text-slate-500">${answerIndex + 1}:</span>
                                <span class="font-bold text-slate-900">${answer || '-'}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }).join('');

        // Attach event listeners to select and delete buttons
        document.querySelectorAll('.select-set-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = btn.getAttribute('data-id');
                selectedAnswerSetId = id;
                localStorage.setItem('grade_smart_selected_answer_set_id', id);
                renderAnswerSetList();
                
                // Clear any error if it was shown previously
                resultError.classList.add('hidden');
            });
        });

        document.querySelectorAll('.delete-set-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = btn.getAttribute('data-id');
                if (confirm('Bạn có chắc chắn muốn xóa bộ đáp án này không?')) {
                    api.delete(`/results/${id}`).then(() => {
                        if (selectedAnswerSetId === id) {
                            selectedAnswerSetId = null;
                            localStorage.removeItem('grade_smart_selected_answer_set_id');
                        }
                        loadAnswerSets().then(() => {
                            renderAnswerSetList();
                        });
                    }).catch((err) => {
                        alert(`Lỗi khi xóa bộ đáp án: ${err.message}`);
                    });
                }
            });
        });

        document.querySelectorAll('.toggle-answers-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const id = btn.getAttribute('data-id');
                const idx = collapsedAnswerSetIds.indexOf(id);
                if (idx > -1) {
                    collapsedAnswerSetIds.splice(idx, 1);
                } else {
                    collapsedAnswerSetIds.push(id);
                }
                localStorage.setItem('grade_smart_collapsed_answer_set_ids', JSON.stringify(collapsedAnswerSetIds));
                renderAnswerSetList();
            });
        });

        // Attach event listeners to editable question answers
        document.querySelectorAll('.question-edit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                
                // If a popover is already open in this button, close it
                const existingPopover = btn.querySelector('.popover-container');
                if (existingPopover) {
                    existingPopover.remove();
                    return;
                }
                
                // Close any other open popovers on the page
                document.querySelectorAll('.popover-container').forEach(p => p.remove());
                
                const setId = btn.getAttribute('data-set-id');
                const answerIndex = parseInt(btn.getAttribute('data-answer-index'), 10);
                const currentAnswer = btn.getAttribute('data-current-answer') || '';
                
                // Create popover container element
                const popover = document.createElement('div');
                popover.className = 'popover-container absolute z-50 bottom-full left-1/2 -translate-x-1/2 mb-2 bg-white rounded-2xl shadow-xl border border-slate-200 p-2 flex gap-1.5 items-center';
                
                const choices = ['A', 'B', 'C', 'D'];
                choices.forEach(choice => {
                    const choiceBtn = document.createElement('button');
                    choiceBtn.type = 'button';
                    choiceBtn.className = choice === currentAnswer
                        ? 'w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs bg-primary text-white border border-primary shadow-sm cursor-pointer select-none'
                        : 'w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs border border-slate-200 bg-white text-slate-700 hover:bg-slate-100 transition cursor-pointer select-none';
                    choiceBtn.textContent = choice;
                    
                    choiceBtn.addEventListener('click', (choiceEvent) => {
                        choiceEvent.stopPropagation();
                        popover.remove(); // Close popover
                        
                        const targetSet = answerSets.find(s => s.id === setId);
                        if (targetSet) {
                            targetSet.answers[answerIndex] = choice;
                            api.put(`/results/${setId}`, { answers: targetSet.answers }).then(() => {
                                renderAnswerSetList();
                                
                                // Live dynamic re-grading if this is the active selected set and we have a scan result displayed!
                                if (selectedAnswerSetId === setId && lastOmrResult) {
                                    const gradedResult = gradeWithAnswerSet(lastOmrResult, targetSet);
                                    renderResult(gradedResult);
                                }
                            }).catch((err) => {
                                alert(`Lỗi khi cập nhật đáp án: ${err.message}`);
                            });
                        }
                    });
                    popover.appendChild(choiceBtn);
                });
                
                // Add tiny caret pointer pointing down
                const caret = document.createElement('div');
                caret.className = 'absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-white';
                popover.appendChild(caret);
                
                btn.appendChild(popover);
            });
        });

        // Close popovers when clicking anywhere else on the document
        document.addEventListener('click', () => {
            document.querySelectorAll('.popover-container').forEach(p => p.remove());
        });
    };

    const resetAnswerSetForm = () => {
        answerSetForm.classList.add('hidden');
        templateSelect.value = '';
        questionCountInput.value = '';
        answerSetNameInput.value = '';
        answerFieldsContainer.innerHTML = '';
    };

    const showAnswerSetForm = () => {
        answerSetForm.classList.remove('hidden');
        answerSetForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };

    const getAnswerValues = () => {
        const inputs = answerFieldsContainer.querySelectorAll('input[type="hidden"]');
        return Array.from(inputs).map((input) => input.value.trim().toUpperCase());
    };

    const collapseAnswerSets = () => {
        if (answerSetsContent) {
            answerSetsContent.classList.add('hidden');
            if (toggleAnswerSetsIcon) {
                toggleAnswerSetsIcon.textContent = 'expand_more';
            }
            localStorage.setItem('grade_smart_answer_sets_collapsed', 'true');
        }
    };

    const expandAnswerSets = () => {
        if (answerSetsContent) {
            answerSetsContent.classList.remove('hidden');
            if (toggleAnswerSetsIcon) {
                toggleAnswerSetsIcon.textContent = 'expand_less';
            }
            localStorage.setItem('grade_smart_answer_sets_collapsed', 'false');
        }
    };

    // Toggle button event listener
    if (toggleAnswerSetsBtn) {
        toggleAnswerSetsBtn.addEventListener('click', () => {
            const isCollapsed = answerSetsContent.classList.contains('hidden');
            if (isCollapsed) {
                expandAnswerSets();
            } else {
                collapseAnswerSets();
            }
        });
    }

    // Load initial collapse state
    const isInitiallyCollapsed = localStorage.getItem('grade_smart_answer_sets_collapsed') === 'true';
    if (isInitiallyCollapsed) {
        collapseAnswerSets();
    } else {
        expandAnswerSets();
    }

    if (newAnswerSetBtn && answerSetForm) {
        newAnswerSetBtn.addEventListener('click', () => {
            expandAnswerSets(); // Automatically expand when creating a new answer set
            showAnswerSetForm();
        });
    }

    const getSelectedTemplateLimit = () => {
        const templateId = templateSelect.value;
        if (!templateId) return null;
        const template = availableTemplates.find(t => (t.id_template || t.id) === templateId);
        return template ? template.totalQuestions : null;
    };

    if (templateSelect) {
        templateSelect.addEventListener('change', () => {
            const limit = getSelectedTemplateLimit();
            if (limit !== null) {
                questionCountInput.placeholder = `Tối đa ${limit} câu`;
                const currentCount = parseInt(questionCountInput.value, 10);
                if (!Number.isNaN(currentCount) && currentCount > limit) {
                    alert(`Số lượng câu hỏi của mẫu phiếu này tối đa là ${limit} câu! Hệ thống đã tự động giới hạn lại.`);
                    questionCountInput.value = limit;
                    createAnswerFields(limit);
                }
            } else {
                questionCountInput.placeholder = 'Nhập số câu hỏi';
            }
        });
    }

    if (questionCountInput) {
        questionCountInput.addEventListener('input', (e) => {
            const limit = getSelectedTemplateLimit();
            let count = parseInt(e.target.value, 10);
            if (!Number.isNaN(count) && count > 0) {
                if (limit !== null && count > limit) {
                    alert(`Số lượng câu hỏi không được lớn hơn số lượng câu hỏi của mẫu phiếu đó (${limit} câu)!`);
                    e.target.value = limit;
                    count = limit;
                }
                createAnswerFields(count);
            } else {
                answerFieldsContainer.innerHTML = '';
            }
        });
        
        questionCountInput.addEventListener('change', (e) => {
            const limit = getSelectedTemplateLimit();
            let count = parseInt(e.target.value, 10);
            if (!Number.isNaN(count) && count > 0) {
                if (limit !== null && count > limit) {
                    e.target.value = limit;
                    count = limit;
                }
                createAnswerFields(count);
            }
        });
    }

    if (saveAnswerSetBtn) {
        saveAnswerSetBtn.addEventListener('click', () => {
            const templateId = templateSelect.value;
            const questionCount = parseInt(questionCountInput.value, 10);
            const setName = answerSetNameInput.value.trim();
            const answers = getAnswerValues();

            if (!templateId) {
                return alert('Vui lòng chọn mẫu phiếu.');
            }
            if (Number.isNaN(questionCount) || questionCount < 1) {
                return alert('Vui lòng nhập số lượng câu hợp lệ.');
            }
            const limit = getSelectedTemplateLimit();
            if (limit !== null && questionCount > limit) {
                return alert(`Số lượng câu hỏi của bộ đáp án (${questionCount}) không được lớn hơn số lượng câu hỏi tối đa của mẫu phiếu (${limit} câu)!`);
            }
            if (!setName) {
                return alert('Vui lòng nhập tên bộ đề.');
            }
            if (answers.length !== questionCount || answers.some((answer) => !answer)) {
                return alert('Vui lòng điền đủ đáp án cho tất cả câu.');
            }

            api.post('/results', {
                name: setName,
                id_template: templateId,
                totalQuestions: questionCount,
                answers: answers
            }).then((newResult) => {
                if (!selectedAnswerSetId) {
                    selectedAnswerSetId = newResult.id_result;
                    localStorage.setItem('grade_smart_selected_answer_set_id', selectedAnswerSetId);
                }
                loadAnswerSets().then(() => {
                    renderAnswerSetList();
                    resetAnswerSetForm();
                });
            }).catch((err) => {
                alert(`Lỗi khi tạo bộ đáp án: ${err.message}`);
            });
        });
    }

    if (cancelAnswerSetBtn) {
        cancelAnswerSetBtn.addEventListener('click', () => {
            resetAnswerSetForm();
        });
    }

    const checkAnswerSetSelected = () => {
        if (answerSets.length === 0) {
            const errorMsg = 'Chưa có bộ đáp án nào được tạo. Vui lòng thêm bộ đáp án trước khi thực hiện chấm điểm.';
            alert(errorMsg);
            showError(errorMsg);
            expandAnswerSets();
            document.getElementById('answer-sets-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
            return null;
        }

        const selected = answerSets.find(s => s.id === selectedAnswerSetId);
        if (!selected) {
            const errorMsg = 'Vui lòng chọn một bộ đáp án chuẩn từ danh sách dưới đây làm đáp án tham chiếu.';
            alert(errorMsg);
            showError(errorMsg);
            expandAnswerSets();
            document.getElementById('answer-sets-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
            return null;
        }
        return selected;
    };

    await loadTemplates();
    await loadAnswerSets();
    renderAnswerSetList();

    if (startScanBtn && scanOptions) {
        startScanBtn.addEventListener('click', () => {
            const activeSet = checkAnswerSetSelected();
            if (activeSet) {
                startScanBtn.classList.add('hidden');
                scanOptions.classList.remove('hidden');
            }
        });
    }

    if (camBtn) {
        camBtn.addEventListener('click', () => {
            const activeSet = checkAnswerSetSelected();
            if (activeSet) {
                alert('Hệ thống đang kết nối Camera...');
            }
        });
    }

    if (uploadBtn && fileInput) {
        uploadBtn.addEventListener('click', () => {
            const activeSet = checkAnswerSetSelected();
            if (activeSet) {
                fileInput.click();
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                const activeSet = checkAnswerSetSelected();
                if (activeSet) {
                    uploadImage(e.target.files[0], activeSet);
                } else {
                    fileInput.value = '';
                }
            }
        });
    }

    const ensureTestAnswerSet = async () => {
        // If there's already a selected answer set, return it
        let activeSet = answerSets.find(s => s.id === selectedAnswerSetId);
        if (activeSet) return activeSet;

        // If there are answer sets but none is selected, select the first one
        if (answerSets.length > 0) {
            selectedAnswerSetId = answerSets[0].id;
            localStorage.setItem('grade_smart_selected_answer_set_id', selectedAnswerSetId);
            renderAnswerSetList();
            return answerSets[0];
        }

        // If no answer sets exist, let's create a default one!
        // Find a template with >= 40 questions (Form 120 or Form 40)
        let template = availableTemplates.find(t => t.totalQuestions >= 40) || availableTemplates[0];
        if (!template) {
            throw new Error('Không tìm thấy mẫu phiếu nào trong hệ thống để tạo bộ đáp án.');
        }

        const defaultAnswers = [
            "B", "C", "C", "C", "D", "D", "C", "B", "D", "A", 
            "A", "A", "B", "C", "C", "C", "D", "B", "A", "C", 
            "B", "C", "C", "C", "D", "D", "C", "B", "D", "A", 
            "A", "A", "B", "C", "C", "C", "D", "B", "A", "C"
        ];

        // Create new result via API
        const newResult = await api.post('/results', {
            name: 'Bộ đáp án Test',
            id_template: template.id_template || template.id,
            totalQuestions: 40,
            answers: defaultAnswers
        });

        // Reload answer sets and render
        await loadAnswerSets();
        selectedAnswerSetId = newResult.id_result || newResult.id;
        localStorage.setItem('grade_smart_selected_answer_set_id', selectedAnswerSetId);
        renderAnswerSetList();

        return answerSets.find(s => s.id === selectedAnswerSetId);
    };

    const testBtn = document.getElementById('test-btn');
    if (testBtn) {
        testBtn.addEventListener('click', async () => {
            try {
                showLoading(); // Hiển thị loading ngay lập tức để người dùng có phản hồi trực quan
                
                const activeSet = await ensureTestAnswerSet();
                if (!activeSet) {
                    throw new Error('Không thể tìm thấy hoặc tạo bộ đáp án thử nghiệm. Vui lòng tạo bộ đáp án thủ công.');
                }

                let response;
                try {
                    response = await fetch('MDD.jpg');
                    if (!response.ok) {
                        throw new Error('Local fetch failed');
                    }
                } catch (e) {
                    console.warn('Không thể tải MDD.jpg từ frontend local, thử tải từ backend...', e);
                    response = await fetch('http://localhost:3000/uploads/MDD.jpg');
                }

                if (!response.ok) {
                    throw new Error('Không thể tải tệp ảnh test MDD.jpg từ cả frontend và backend. Vui lòng kiểm tra lại đường dẫn file.');
                }
                const blob = await response.blob();
                const file = new File([blob], 'MDD.jpg', { type: 'image/jpeg' });
                await uploadImage(file, activeSet);
            } catch (err) {
                showError(err.message);
                hideLoading();
            }
        });
    }

    const regradeBtn = document.getElementById('regrade-btn');
    if (regradeBtn) {
        regradeBtn.addEventListener('click', () => {
            const activeSet = checkAnswerSetSelected();
            if (activeSet) {
                fileInput.value = '';
                fileInput.click();
            }
        });
    }

    const resetPageBtn = document.getElementById('reset-page-btn');
    if (resetPageBtn) {
        resetPageBtn.addEventListener('click', () => {
            window.location.reload();
        });
    }
});
