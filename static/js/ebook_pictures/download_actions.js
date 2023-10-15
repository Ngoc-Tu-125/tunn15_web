document.addEventListener('DOMContentLoaded', function() {
    const downloadButtons = document.querySelectorAll('.download-btn');

    downloadButtons.forEach(button => {
        button.addEventListener('click', function() {
            const imageUrl = this.dataset.imageUrl;
            const caption = this.dataset.caption;

            createDownloadableImageCard(imageUrl, caption);
        });
    });
});

function createDownloadableImageCard(imageUrl, caption) {
    const img = new Image();
    img.crossOrigin = "anonymous"; // This ensures we can use the image on the canvas without tainting it
    img.src = imageUrl;

    img.onload = function() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = img.width;
        canvas.height = img.height + 30; // extra space for caption

        // Draw image
        ctx.drawImage(img, 0, 0);

        // Add caption
        ctx.font = '20px Arial';
        ctx.fillStyle = 'black';
        ctx.fillText(caption, 10, img.height + 25); // adjust these values to position caption as needed

        // Trigger download
        const a = document.createElement('a');
        a.href = canvas.toDataURL('image/png');
        a.download = 'image_card.png';
        a.click();
    };
}
