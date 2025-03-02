document.addEventListener('DOMContentLoaded', () => {
    const partsList = document.getElementById('parts-list');
    const cartCount = document.getElementById('cart-count');
    const loginButton = document.getElementById('login-button');
    const logoutButton = document.getElementById('logout-button');
    const loginModal = document.getElementById('login-modal');
    const closeModal = document.querySelector('.close');
    const loginForm = document.getElementById('login-form');
    const viewCartButton = document.getElementById('view-cart');
    const cartPage = document.getElementById('cart-page');
    const cartItemsDiv = document.getElementById('cart-items');
    let accessToken = null;

    // Function to set a cookie
    const setCookie = (name, value, days) => {
        const d = new Date();
        d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + d.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/";
    };

    // Function to get a cookie
    const getCookie = (name) => {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    };

    // Function to create or load a cart
    const createOrLoadCart = () => {
        let publicCartId = getCookie('public_cart_id');
        if (!publicCartId) {

            fetch('http://localhost:5000/api/cart', {
                method: 'GET',
                credentials: 'include'  // Include credentials (cookies) with the request
            })
            .then(response => response.json())
            .then(items => {
                if (Array.isArray(items)) {
                    cartCount.textContent = items.length;
                } else {
                    cartCount.textContent = '0';
                }
            });
        } else {
            updateCartCount();
        }
    };

    // Fetch parts and display them
    fetch('http://localhost:5000/api/parts', {
        credentials: 'include'  // Include credentials (cookies) with the request
    })
    .then(response => response.json())
    .then(parts => {
        parts.forEach(part => {
            const partDiv = document.createElement('div');
            partDiv.className = 'part';
            partDiv.innerHTML = `
                <h3>${part.name}</h3>
                <p>Price: $${part.price}</p>
                <button onclick="addToCart(${part.id})">Add to Cart</button>
            `;
            partsList.appendChild(partDiv);
        });
    });

    // Add to cart function
    window.addToCart = (partId) => {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (accessToken) {
            headers['Authorization'] = `Bearer ${accessToken}`;
        }

        fetch('http://localhost:5000/api/cart', {
            method: 'POST',
            headers: headers,
            credentials: 'include',  // Include credentials (cookies) with the request
            body: JSON.stringify({ part_id: partId, quantity: 1 })
        })
        .then(response => response.json())
        .then(data => {
            if (data.msg === 'Item added to cart') {
                updateCartCount();
            } else {
                alert(data.error || 'Error adding item to cart');
            }
        });
    };

    // Update cart count
    const updateCartCount = () => {
        const headers = {};
        if (accessToken) {
            headers['Authorization'] = `Bearer ${accessToken}`;
        }

        fetch('http://localhost:5000/api/cart', {
			method: 'GET',
            headers: headers,
            credentials: 'include'  // Include credentials (cookies) with the request
        })
        .then(response => response.json())
        .then(items => {
            if (Array.isArray(items)) {
                cartCount.textContent = items.length;
            } else {
                cartCount.textContent = '0';
            }
        });
    };

    // Show login modal
    loginButton.addEventListener('click', () => {
        loginModal.style.display = 'block';
    });

    // Close login modal
    closeModal.addEventListener('click', () => {
        loginModal.style.display = 'none';
    });

    // Login form submission
    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password }),
            credentials: 'include'  // Include credentials (cookies) with the request
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                accessToken = data.access_token;
                loginModal.style.display = 'none';
                loginButton.style.display = 'none';
                logoutButton.style.display = 'block';
                updateCartCount();
            } else {
                alert('Login failed');
            }
        });
    });

    // Logout function
    logoutButton.addEventListener('click', () => {
        fetch('http://localhost:5000/api/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            },
            credentials: 'include'  // Include credentials (cookies) with the request
        })
        .then(response => response.json())
        .then(data => {
            if (data.msg === 'Successfully logged out') {
                accessToken = null;
                loginButton.style.display = 'block';
                logoutButton.style.display = 'none';
                cartCount.textContent = '0';
            } else {
                alert('Logout failed');
            }
        });
    });

    // Close modal when clicking outside of it
    window.onclick = (event) => {
        if (event.target === loginModal) {
            loginModal.style.display = 'none';
        }
    };

    // View cart
    viewCartButton.addEventListener('click', (event) => {
        event.preventDefault();
        partsList.style.display = 'none';
        cartPage.style.display = 'block';
        loadCartItems();
    });

    // Load cart items
    const loadCartItems = () => {
        const headers = {};
        if (accessToken) {
            headers['Authorization'] = `Bearer ${accessToken}`;
        }

        fetch('http://localhost:5000/api/cart', {
            headers: headers,
            credentials: 'include'  // Include credentials (cookies) with the request
        })
        .then(response => response.json())
        .then(items => {
            cartItemsDiv.innerHTML = '';
            items.forEach(item => {
                const cartItemDiv = document.createElement('div');
                cartItemDiv.className = 'cart-item';
                cartItemDiv.innerHTML = `
                    <h3>${item.name}</h3>
                    <p>Price: $${item.price}</p>
                    <p>Quantity: <input type="number" value="${item.quantity}" min="1" onchange="updateCartItem(${item.part_id}, this.value)"></p>
                    <button onclick="removeCartItem(${item.part_id})">Remove</button>
                `;
                cartItemsDiv.appendChild(cartItemDiv);
            });
        });
    };

    // Update cart item function
    window.updateCartItem = (partId, quantity) => {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (accessToken) {
            headers['Authorization'] = `Bearer ${accessToken}`;
        }

        fetch(`http://localhost:5000/api/cart/${partId}`, {
            method: 'PUT',
            headers: headers,
            credentials: 'include',  // Include credentials (cookies) with the request
            body: JSON.stringify({ quantity: parseInt(quantity) })
        })
        .then(response => response.json())
        .then(data => {
            if (data.msg === 'Cart item updated') {
                updateCartCount();
            } else {
                alert(data.error || 'Error updating cart item');
            }
        });
    };

    // Remove cart item function
    window.removeCartItem = (partId) => {
        const headers = {};
        if (accessToken) {
            headers['Authorization'] = `Bearer ${accessToken}`;
        }

        fetch(`http://localhost:5000/api/cart/${partId}`, {
            method: 'DELETE',
            headers: headers,
            credentials: 'include'  // Include credentials (cookies) with the request
        })
        .then(response => response.json())
        .then(data => {
            if (data.msg === 'Cart item removed') {
                loadCartItems();
                updateCartCount();
            } else {
                alert(data.error || 'Error removing cart item');
            }
        });
    };

    // Initial cart creation or loading
    createOrLoadCart();
});