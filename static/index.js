function uploadFile() {
    let fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = ".txt"
    fileInput.onchange = e => { 
        let file = e.target.files[0]; 
        let formData = new FormData();
        formData.append('file', file);

        // Show loader GIF
        document.getElementById('upload-btn').style.display = 'none';
        document.getElementById('loader').style.display = 'block';

        fetch('/', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
          .then(html => {
              // Hide loader GIF
              document.getElementById('loader').style.display = 'none';

              // Update page content
              document.documentElement.innerHTML = html;
          });
    }
    fileInput.click();
}
