
// const favoriteVideoLink = document.querySelector('#favorited')
// favoriteVideoLink.addEventListener('click', event => {
//   event.preventDefault()
//   const videoId = favoriteVideoLink.dataset.videoId
//   fetch('/studiopal/' + videoId + '/favorite/', {
//     method: 'POST',
//     credentials: 'include'
//   })
//     .then(res => res.json())
//     .then(data => {
//       if (data.isFavorite) {
//         favoriteVideoLink.innerHTML = '&#9734'
//       } else {
//         favoriteVideoLink.innerHTML = '&#11088;'
//       }
//     })
// })
