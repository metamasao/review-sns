const follow = document.querySelector('a.follow');

follow.addEventListener('click', (event) => {
    event.preventDefault();
    const previousAction = follow.dataset.action;
    const userId = follow.dataset.id;

    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    axios.defaults.headers['x-requested-with'] = 'XMLHttpRequest';
    axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/follow/',
        data: `id=${userId}&action=${previousAction}`
    }).then(res => {
        if (res.data.status === 'ok') {
            const followerCount = document.querySelector('span.follower-count');
            if (previousAction === 'unfollow') {
                follow.dataset.action = 'follow';
                follow.textContent = 'フォローする';
                followerCount.textContent = parseInt(followerCount.textContent) - 1;
            } else {
                follow.dataset.action = 'unfollow';
                follow.textContent = 'フォローをやめる';
                followerCount.textContent = parseInt(followerCount.textContent) + 1;
            }
        }
    }).catch(err => {
        const followText= document.querySelector('div.follow-text');
        const para = document.createElement('p');
        para.textContent = '接続に問題が発生しフォローできません。後ほど再度お試しください。'
        followText.appendChild(para);
    })
});