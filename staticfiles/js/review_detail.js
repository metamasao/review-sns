const likeButton = document.querySelector('a.like');

likeButton.addEventListener('click', (event) => {
    event.preventDefault();
    const previousLike = likeButton.dataset.action;
    const reviewId = likeButton.dataset.id;
    
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    axios.defaults.headers['x-requested-with'] = 'XMLHttpRequest';
    axios({
        method: 'post',
        url: 'https://metamasao-review-sns.herokuapp.com/review/like/',
        data: `id=${reviewId}&action=${previousLike}`
    }).then(res => {
        if (res.data.status === 'ok') {
            let likeCount = document.querySelector('span.like-count');
            if (previousLike === 'unlike') {
                likeButton.dataset.action = 'like';
                likeButton.textContent = 'いいね';
                likeCount.textContent = parseInt(likeCount.textContent) - 1;
            } else {
                likeButton.dataset.action = 'unlike';
                likeButton.textContent = 'いいねをやめる';
                likeCount.textContent = parseInt(likeCount.textContent) + 1;
            }
        }
    }).catch(error => {
        const likeText = document.querySelector('div.like-text');
        const para = document.createElement('p');
        para.textContent = '接続に問題が発生し、いいねができません。後ほど再度お試しください。';
        likeText.appendChild(para);
    })
});