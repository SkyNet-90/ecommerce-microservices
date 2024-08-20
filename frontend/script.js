const productForm = document.getElementById('productForm');
const orderForm = document.getElementById('orderForm');
const loginForm = document.getElementById('loginForm');

// Handle login form submission
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('http://your-user-service-url/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        localStorage.setItem('authToken', data.token);
        loginForm.style.display = 'none';
        document.getElementById('content').style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        alert('Login failed');
    }
});

// Handle product form submission
productForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const name = document.getElementById('productName').value;
    const price = parseFloat(document.getElementById('productPrice').value);
    const quantity = parseInt(document.getElementById('productQuantity').value);
    const token = localStorage.getItem('authToken');

    fetch('http://172.212.77.244:80/product', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
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
        console.error('Error:', error);
        alert('Failed to add product');
    });
});

// Handle order form submission
orderForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const productId = parseInt(document.getElementById('orderProductId').value);
    const quantity = parseInt(document.getElementById('orderQuantity').value);
    const token = localStorage.getItem('authToken');

    fetch('http://172.212.77.244:80/order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
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
        alert('Failed to add order');
    });
});