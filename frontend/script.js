document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const productForm = document.getElementById('productForm');
    const orderForm = document.getElementById('orderForm');

    // Handle register form submission
    registerForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.getElementById('registerUsername').value;
        const password = document.getElementById('registerPassword').value;

        try {
            const response = await fetch('http://48.216.147.30/user', { // User registration URL
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
            alert('User registered successfully');
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to register user');
        }
    });

    // Handle login form submission
    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('http://48.216.147.30/login', { // User login URL
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

        fetch('http://172.212.77.244/product', { // Product service URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name, price, quantity })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Product added:', data);
            // Handle successful product addition
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

        fetch('http://172.212.77.254/order', { // Order service URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ productId, quantity })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Order added:', data);
            // Handle successful order addition
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to add order');
        });
    });
});