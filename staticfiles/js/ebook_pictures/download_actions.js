document.addEventListener('DOMContentLoaded', function() {
    const downloadButtons = document.querySelectorAll('.download-btn');

    downloadButtons.forEach(button => {
        button.addEventListener('click', function() {
            const imageUrl = this.dataset.imageUrl;
            const title = this.dataset.title;
            const shortIntro = this.dataset.shortIntro;

            createDownloadableImageCard(imageUrl, title, shortIntro);
        });
    });
});

function createDownloadableImageCard(imageUrl, title, shortIntro) {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.src = imageUrl;


    img.onload = function() {
        const isLandscape = img.width > img.height;
        const borderRatio = isLandscape ? 0.02 : 0.025;;  // 2% border
        const borderSize = Math.floor(borderRatio * img.width);

        const titleFontSize = isLandscape ? img.width * 0.02 : img.width * 0.03;
        const shortIntroFontSize = isLandscape ? img.width * 0.015 : img.width * 0.02;


        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = img.width + 2 * borderSize;
        canvas.height = img.height + 2 * borderSize + (isLandscape ? 120 : 130);

        // Fill entire canvas with white
        ctx.fillStyle = 'white';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Draw image inside the border
        ctx.drawImage(img, borderSize, borderSize);

        // Add title
        ctx.font = `bold ${titleFontSize}px Arial`;
        ctx.fillStyle = 'black';
        const titleWidth = ctx.measureText(title).width;
        const titleXPosition = (canvas.width - titleWidth) / 2;
        ctx.fillText(title, titleXPosition, canvas.height - 105);

        // Add shortIntro
        ctx.font = `${shortIntroFontSize}px Arial`;
        ctx.fillStyle = 'gray';
        const introWidth = ctx.measureText(shortIntro).width;
        const introXPosition = (canvas.width - introWidth) / 2;
        ctx.fillText(shortIntro, introXPosition, canvas.height - 55);

        // Trigger download
        const a = document.createElement('a');
        a.href = canvas.toDataURL('image/png');
        a.download = 'image_card.png';
        a.click();
    };
}
