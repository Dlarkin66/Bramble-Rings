var thumbnails = document.querySelectorAll('.thumbnail');
var activeImage = document.querySelector('.main-image img');

thumbnails.forEach(function(thumbnail) {
    thumbnail.addEventListener('click', function() {
        var newImageSrc = this.querySelector('img').getAttribute('src');
        activeImage.setAttribute('src', newImageSrc);
    });
});