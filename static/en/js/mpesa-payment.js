
function initiateMpesaPayment(orderId, phoneNumber) {
    document.getElementById('payment-status').innerHTML = 'Initiating payment...';
    
    fetch(`/orders/order/${orderId}/mpesa/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken()
        },
        body: `phone_number=${phoneNumber}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            pollTransactionStatus(data.checkout_request_id);
        } else {
            document.getElementById('payment-status').innerHTML = 
                `Payment initiation failed: ${data.message}`;
        }
    })
    .catch(error => {
        document.getElementById('payment-status').innerHTML = 
            'Error initiating payment. Please try again.';
    });
}

function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function pollTransactionStatus(checkoutRequestId) {
    const maxAttempts = 24; // 2 minutes maximum (5 seconds * 24)
    let attempts = 0;
    
    const pollInterval = setInterval(() => {
        attempts++;
        
        fetch(`/mpesa/check-status/${checkoutRequestId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'completed') {
                    clearInterval(pollInterval);
                    document.getElementById('payment-status').innerHTML = 
                        `Payment completed successfully!<br>
                         Receipt Number: ${data.receipt_number}`;
                    window.location.href = '/mpesa/payment-success/';
                } else if (data.status === 'failed') {
                    clearInterval(pollInterval);
                    document.getElementById('payment-status').innerHTML = 
                        'Payment failed. Please try again.';
                    window.location.href = '/mpesa/payment-failed/';
                } else if (attempts >= maxAttempts) {
                    clearInterval(pollInterval);
                    document.getElementById('payment-status').innerHTML = 
                        'Payment status check timed out. Please check your M-Pesa messages.';
                }
            })
            .catch(error => {
                clearInterval(pollInterval);
                document.getElementById('payment-status').innerHTML = 
                    'Error checking payment status';
            });
    }, 5000);  // Poll every 5 seconds
}