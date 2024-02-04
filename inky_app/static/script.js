
function handlePaste(e) {
    
    var items = (e.clipboardData || window.clipboardData).items;
    for (var i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
            var blob = items[i].getAsFile();

            var formData = new FormData();
            formData.append('file', blob, 'clipboard-image.png');
            console.log('uploading')
            fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log('Image uploaded successfully.');
            })
            .catch(error => {
                console.error('Error uploading image:', error);
            });

            e.preventDefault();
        }
    }

}

window.onload = function() {
    document.body.addEventListener('paste', (event) => {
	handlePaste(event);
    });
}

document.addEventListener('touchmove', function(event) {
    event.preventDefault();
}, { passive: false });

