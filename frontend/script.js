document.addEventListener('DOMContentLoaded', () => {
    const productForm = document.getElementById('productForm');
    const orderForm = document.getElementById('orderForm');

    productForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const name = document.getElementById('productName').value;
        const price = parseFloat(document.getElementById('productPrice').value);
        const quantity = parseInt(document.getElementById('productQuantity').value);

        fetch('http://48.216.147.49:31911/product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, price, quantity }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Product added:', data);
            alert('Product added successfully!');
            productForm.reset();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error adding product');
        });
    });

    orderForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const productId = parseInt(document.getElementById('orderProductId').value);
        const quantity = parseInt(document.getElementById('orderQuantity').value);

        fetch('http://48.216.147.224:32172/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ product_id: productId, quantity }),
        })
        .then(response => response.json())
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
});
