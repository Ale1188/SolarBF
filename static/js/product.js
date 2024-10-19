document.addEventListener("DOMContentLoaded", function() {
    const incrementButtons = document.querySelectorAll('[id^="increment"]');
    const decrementButtons = document.querySelectorAll('[id^="decrement"]');

    incrementButtons.forEach(button => {
        const stock = parseInt(button.dataset.stock);

        button.addEventListener('click', function() {
            const quantityInput = document.getElementById(`quantity${button.id.replace('increment', '')}`);
            let quantity = parseInt(quantityInput.value);
            
            if (quantity < stock) {
                quantityInput.value = quantity + 1;
            } else {
                // alert(`You cannot add more than ${stock} items in stock.`);
                button.disabled = true;
            }
        });
    });

    decrementButtons.forEach(button => {
        button.addEventListener('click', function() {
            const quantityInput = document.getElementById(`quantity${button.id.replace('decrement', '')}`);
            let quantity = parseInt(quantityInput.value);
            
            if (quantity > 1) {
                quantityInput.value = quantity - 1;
            }
        });
    });
});
