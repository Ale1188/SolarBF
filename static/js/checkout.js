document.getElementById('payment_method').addEventListener('change', function() {
    var paymentMethod = this.value;

    document.querySelectorAll('.payment-method-fields').forEach(function(fieldset) {
        fieldset.style.display = 'none';
    });

    if (paymentMethod === 'credit_card' || paymentMethod === 'debit') {
        document.getElementById('credit_card_fields').style.display = 'block';
    } else if (paymentMethod === 'paypal') {
        document.getElementById('paypal_fields').style.display = 'block';
    }
});