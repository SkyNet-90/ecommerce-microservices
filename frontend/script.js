const productForm = document.getElementById('productForm');
const orderForm = document.getElementById('orderForm');

productForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const name = document.getElementById('productName').value;
    const price = parseFloat(document.getElementById('productPrice').value);
    const quantity = parseInt(document.getElementById('productQuantity').value);

    fetch('http://172.212.77.244:80/product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, price, quantity }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Product added:', data);
        alert('Product added successfully!');
        productForm.reset();
    })
    .catch(error => {
        console.error('Error:', error);        const productForm = document.getElementById('productForm');
        const orderForm = document.getElementById('orderForm');
        
        productForm.addEventListener('submit', (event) => {
            event.preventDefault();
        
            const name = document.getElementById('productName').value;
            const price = parseFloat(document.getElementById('productPrice').value);
            const quantity = parseInt(document.getElementById('productQuantity').value);
        
            console.log('Submitting product:', { name, price, quantity });
        
            fetch('http://172.212.77.244:80/product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, price, quantity }),
            })
            .then(response => {
                console.log('Product response status:', response.status);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Product added:', data);
                alert('Product added successfully!');
                productForm.reset();
            })
            .catch(error => {
                console.error('Error adding product:', error);
                alert('Error adding product');
            });
        });
        
        orderForm.addEventListener('submit', (event) => {
            event.preventDefault();
        
            const productId = parseInt(document.getElementById('orderProductId').value);
            const quantity = parseInt(document.getElementById('orderQuantity').value);
        
            console.log('Submitting order:', { product_id: productId, quantity });
        
            fetch('http://172.212.77.254:80/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ product_id: productId, quantity }),
            })
            .then(response => {
                console.log('Order response status:', response.status);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Order added:', data);
                alert('Order added successfully!');
                orderForm.reset();
            })
            .catch(error => {
                console.error('Error adding order:', error);
                alert('Error adding order');
            });
        });
        alert('Error adding product');
    });
});

orderForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const productId = parseInt(document.getElementById('orderProductId').value);
    const quantity = parseInt(document.getElementById('orderQuantity').value);

    fetch('http://172.212.77.254:80/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId, quantity }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Order added:', data);
        alert('Order added successfully!');
        orderForm.reset();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error adding order');
    });
});
