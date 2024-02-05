
function handlePaste(e) {
    var items = (e.clipboardData || window.clipboardData).items;
    for (var i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
            var blob = items[i].getAsFile();

            var formData = new FormData();
            formData.append('file', blob, 'clipboard-image.png');
            console.log('uploading from clipboard')
            doLabel();
	    fetch('/upload', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log('Image uploaded successfully.');
            })
            .catch(error => {
                //console.error('Error uploading image:', error);
            });

            e.preventDefault();
        }
    }
}


 function updateDisplayFromGallery(filename){
    console.log('using ', filename)
    doLabel();
    fetch(`/display_image/${filename}`)
        .then(response => {
            if (response.ok) {
                console.log('Display updated successfully');
            } else {
                console.error('Failed to update display');
            }
        })
        .catch(error => console.error('Error:', error));
 }

function doLabel(){
    document.getElementById("synclabel").style.opacity = 1.;
    setTimeout(()=>{document.getElementById("synclabel").style.opacity = 0.}, 15000);
}

function handleButton(e){
	doLabel();
	console.log('uploading');
	document.getElementById('uploadForm').submit();
}

window.onload = function() {
    document.body.addEventListener('paste', (event) => {
	handlePaste(event);
    });
}

