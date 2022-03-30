function getBookData(isbnData, description) {
    let data = null;
    let error = null;

    axios
        .get(`https://api.openbd.jp/v1/get?isbn=${isbnData}`)
        .then(res => {
            if (res.data[0] !== null && Object.values(res.data[0].onix.CollateralDetail).length !== 0) {
                data = res.data[0].onix.CollateralDetail;
            }
        })
        .catch(err => {
            error = err;
        })
        .then(() => {
            if (data !== null) {
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
                    const para = document.createElement('p');
                    para.textContent = item;
                    para.setAttribute('style', 'white-space: pre-line;');
                    description.appendChild(para);
                });            
            } else {
                const para = document.createElement('p');
                para.textContent = 'No data is available.';
                description.appendChild(para);
            }     
        })
}