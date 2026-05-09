document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');

    if (dropZone && fileInput) {
        dropZone.onclick = () => fileInput.click();

        dropZone.ondragover = (e) => {
            e.preventDefault();
            dropZone.classList.add('bg-blue-100', 'border-primary');
        };

        dropZone.ondragleave = () => {
            dropZone.classList.remove('bg-blue-100', 'border-primary');
        };

        dropZone.ondrop = (e) => {
            e.preventDefault();
            dropZone.classList.remove('bg-blue-100', 'border-primary');
            handleFiles(e.dataTransfer.files);
        };

        fileInput.onchange = (e) => {
            handleFiles(e.target.files);
        };
    }

    function handleFiles(files) {
        const validFiles = Array.from(files).filter(file => file.type.startsWith('image/'));
        if (validFiles.length > 0) {
            alert('Đã nhận ' + validFiles.length + ' tệp hình ảnh hợp lệ.');
        } else {
            alert('Vui lòng chỉ tải lên tệp hình ảnh.');
        }
    }
});
