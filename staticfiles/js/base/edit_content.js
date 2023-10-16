function editContent(displayId, editorId, saveButtonId) {
    document.getElementById(displayId).classList.add('hidden');
    document.getElementById(editorId).classList.remove('hidden');
    document.getElementById(saveButtonId).classList.remove('hidden');
}

function saveContent(editorId, displayId, contentType) {
    const newValue = document.getElementById(editorId).value;
    const sectionElement = document.getElementById(editorId).closest("[data-section]");
    const sectionName = sectionElement.getAttribute('data-section');

    fetch(`/save-content/${sectionName}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: contentType === 'title' ? newValue : undefined,
            content: contentType === 'content' ? newValue : undefined
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(displayId).innerText = newValue;
            document.getElementById(displayId).classList.remove('hidden');
            document.getElementById(editorId).classList.add('hidden');
        }
    });
}

function previewImage(input, imgId) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(imgId).src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
        document.getElementById(`upload-button-${imgId.split('-')[2]}`).classList.remove('hidden');
    }
}


function uploadImage(imageInputId, displayImageId) {
    const imageInput = document.getElementById(imageInputId);
    const sectionElement = imageInput.closest("[data-section]");
    const sectionName = sectionElement.getAttribute('data-section');

    // Create FormData to append the image
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    fetch(`/upload-image/${sectionName}/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`upload-button-${sectionName}`).classList.add('hidden');
        }
    });
}
