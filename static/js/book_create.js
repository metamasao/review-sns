const searchBook = document.querySelector('form .book-search')

searchBook.addEventListener('click', (event) => {
    event.preventDefault();
    const description = document.querySelector('.search-result');
    const inputValue = document.querySelector('#div_id_isbn input');
    const para = document.createElement('p');

    description.textContent = '';

    if (/^\d{13}$/.test(inputValue.value)) {
        let data = null;
        let error = null;
        let summary = null;
        
        axios
            .get(`https://api.openbd.jp/v1/get?isbn=${inputValue.value}`)
            .then(res => {
                if (res.data[0] !== null && Object.values(res.data[0].onix.CollateralDetail).length !== 0) {
                    data = res.data[0].onix.CollateralDetail;
                    summary = res.data[0].summary;
                }
            })
            .catch(err => {
                error = err;
            })
            .then(() => {
                if (data !== null) {
                    if (data.TextContent !== undefined) {
                        let title, info;
                        const bookDataArray = [];

                        data.TextContent.map(item => {
                            if (item.TextType==='02' || item.TextType==='03') {
                                title = item.Text;
                                bookDataArray.pop();
                                bookDataArray.push(title);
                            } else if (item.TextType==='04') {
                                info = item.Text;
                                bookDataArray.push(info);
                            }
                        });
                        
                        bookDataArray.map(item => {
                            const innerPara = document.createElement('p');
                            innerPara.textContent = item;
                            innerPara.setAttribute('style', 'white-space: pre-line;');
                            para.appendChild(innerPara);
                        });
                    }
                    const inputTitle = document.querySelector('form #div_id_title input');
                    inputTitle.value = summary.title;
                } else {
                    para.textContent = 'No detail data is available.';
                }     
            })
    } else {
        para.textContent = '数字のみを13文字入力してください';
    }
    description.appendChild(para);
    inputValue.focus();
})