// function hexToRgb(hex) {
//     hex = hex.replace(/^#/, '');
//     if (hex.length === 3) {
//         hex = hex.split('').map(char => char + char).join('');
//     }
//     const bigint = parseInt(hex, 16);
//     const r = (bigint >> 16) & 255;
//     const g = (bigint >> 8) & 255;
//     const b = bigint & 255;
//     return { r, g, b };
// }

// document.addEventListener('DOMContentLoaded', function() {
//   const rootStyles = getComputedStyle(document.documentElement);
//   const hexColor = rootStyles.getPropertyValue('--primary-color').trim();
//   const { r, g, b } = hexToRgb(hexColor);
//   const posts = document.querySelectorAll(".post-card");
//   posts.forEach(post => post.style.backgroundColor = `rgba(${r}, ${g}, ${b}, .5)`);
// });


document.querySelector('.upload-image-icon').addEventListener('click', function() {
    document.querySelector('.image-form').click(); 
});