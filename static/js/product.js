document.addEventListener('DOMContentLoaded', function() {

    // Search functionality
    document.getElementById('searchInput').addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const products = document.querySelectorAll('.product-card');

        products.forEach(product => {
            const title = product.querySelector('.product-title').textContent.toLowerCase();
            const description = product.querySelector('.product-description').textContent.toLowerCase();

            if (title.includes(searchTerm) || description.includes(searchTerm)) {
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
            }
        });
    });

    // Category filter
    document.getElementById('categoryFilter').addEventListener('change', function(e) {
        const category = e.target.value.toLowerCase();
        const products = document.querySelectorAll('.product-card');

        products.forEach(product => {
            if (!category || product.dataset.category.toLowerCase() === category) {
                product.style.display = 'block';
            } else {
                product.style.display = 'none';
            }
        });
    });

    // Modal functionality
    function openEditModal(productId) {
        const modal = document.getElementById('editModal');
        modal.style.display = 'block';

        htmx.ajax('GET', `/products/edit_product/${productId}/`, {
            target: '#editFormContainer',
            swap: 'innerHTML'
        });
    }

    // Modal close functionality
    const closeModalBtn = document.querySelector('.close-modal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            closeEditModal();
        });
    }

    function closeEditModal() {
        const modal = document.getElementById('editModal');
        modal.style.display = 'none';
        document.getElementById('editFormContainer').innerHTML = '';  // Clear form
    }

    function confirmDelete(productId) {
        if (confirm('Are you sure you want to delete this product?')) {
            htmx.ajax('POST', `/products/delete_product/${productId}/`, {
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                target: '#productsGrid',
                swap: 'innerHTML',
                onSuccess: function(response) {
                    try {
                        const data = JSON.parse(response.xhr.responseText);
                        if (data.status === 'success') {
                            document.getElementById('productsGrid').innerHTML = data.html;
                            alert(data.message);
                        }
                    } catch (e) {
                        console.error('Error parsing response:', e);
                    }
                }
            });
        }
    }

    // Close modal when clicking outside
    window.onclick = function(event) {
        const modal = document.getElementById('editModal');
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // Escape key support for closing modal
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeEditModal();
        }
    });

    // Handle HTMX after request
    document.addEventListener('htmx:afterRequest', function(evt) {
        if (evt.detail.successful && evt.detail.xhr.response) {
            try {
                const response = JSON.parse(evt.detail.xhr.response);
                if (response.status === 'success' && response.html) {
                    document.getElementById('productsGrid').innerHTML = response.html;
                    document.getElementById('editModal').style.display = 'none';
                }
            } catch (e) {
                console.log('Not a JSON response');
            }
        }
    });

});
