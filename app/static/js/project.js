function addToCart(productId, productName) {
    var productCount = parseInt(sessionStorage.getItem('product_' + productId)) || null;
    getProductData(productId, productName) // Fetch product data
        .then(productData => {
            if (productCount === null) {
                sessionStorage.setItem('product_' + productId, JSON.stringify(productData));
            } else {
                var updatedProduct = JSON.parse(sessionStorage.getItem('product_' + productId));
                updatedProduct.count += 1;
                sessionStorage.setItem('product_' + productId, JSON.stringify(updatedProduct));
            }
            updateMainButton();
            updateProductDisplay(productId, productName);
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch operation
            console.error('Error fetching product data:', error);
        });
}


function decreaseCount(productId, productName) {
    var product = JSON.parse(sessionStorage.getItem('product_' + productId));
    if (product.count > 1) {
        product.count -= 1;
        sessionStorage.setItem('product_' + productId, JSON.stringify(product));
    } else {
        sessionStorage.removeItem('product_' + productId);
    }
    updateMainButton();
    updateProductDisplay(productId, productName);
}

function increaseCount(productId, productName) {
    var product = JSON.parse(sessionStorage.getItem('product_' + productId)) || {'count': 1};
    product.count += 1;
    sessionStorage.setItem('product_' + productId, JSON.stringify(product));
    updateMainButton();
    updateProductDisplay(productId, productName);
}

function getCartItemCount() {
    var totalPrice = 0;
    var itemCount = 0;

    for (var i = 0; i < sessionStorage.length; i++) {
        var key = sessionStorage.key(i);
        if (key.startsWith('product_')) {
            var product = JSON.parse(sessionStorage.getItem(key));
            itemCount += product.count; // Increment itemCount by the count of each product
            totalPrice += product.count * product.price; // Calculate the total price
        }
    }

    return {itemCount: itemCount, totalPrice: totalPrice};
}
