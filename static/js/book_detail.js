const isbnElement = document.querySelector('div.book-detail');
const description = document.querySelector('div.book-detail div.description');
const isbnData = isbnElement.dataset.isbn;

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
		const para = document.createElement('p');

        if (data !== null && data.TextContent !== undefined) {
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
        } else {
            para.textContent = 'No detail data is available.';
        }

		description.appendChild(para);
    })

const descriptionButton = document.querySelector('.card-footer button');

descriptionButton.addEventListener('click', () => {
	const description = document.querySelector('div.book-detail div.description');
	description.style.display = description.style.display==='none' ? 'block' : 'none';
})

/*
 	Object.values(summary).map(item => {
		let contentElement = document.createElement('p');
		contentElement.textContent = item;
		isbnElement.appendChild(contentElement);
*/

