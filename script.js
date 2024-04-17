function uploadFile() {
    var files = document.getElementById('fileInput').files;
    var formData = new FormData();
    var totalFiles = files.length;
    var completedFiles = 0; // Counter to track completed conversions

    for (var i = 0; i < totalFiles; i++) {
        formData.append('files', files[i]);
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/upload', true);
    xhr.upload.onprogress = function(event) {
        if (event.lengthComputable) {
            var percentComplete = (event.loaded / event.total) * 100;
            document.getElementById('progressBar').value = percentComplete;
        }
    };
    xhr.onload = function() {
        if (xhr.status === 200) {
            document.getElementById('status').textContent = 'Conversion complete.';
            window.location.href = "http://127.0.0.1:5500/generalpage.html";
        } else {
            document.getElementById('status').textContent = 'An error occurred during conversion.';
        }
    };
    xhr.onerror = function() {
        document.getElementById('status').textContent = 'An error occurred during conversion.';
    };
    xhr.send(formData);
}
