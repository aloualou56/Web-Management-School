document.getElementById('addPaymentForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const url = 'add_payment/';  
    const formData = new FormData(this);

    $.ajax({
        url: url,
        method: 'POST', 
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            alert('Payment added successfully!');
            closeModal();  
            location.reload();  
        },
        error: function() {
            alert('An error occurred while adding the payment.');
        }
    });
});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function openModal() {
    document.getElementById('addStudentModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('addStudentModal').style.display = 'none';
}

function openReceiptModal(paymentId) {

    document.getElementById('receiptPaymentId').value = paymentId;

    document.getElementById('addReceiptModal').style.display = 'flex';
    
}

function closeReceiptModal() {
    document.getElementById('addReceiptModal').style.display = 'none';
}  

function deletePayment(PaymentID) {
    if (confirm('Are you sure you want to delete this?')) {
        
        $.ajax({
            url: `/payments/${PaymentID}/delete/`,  
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') 
            },
            success: function() {
                
                location.reload();
            },
            error: function() {
                alert('Failed to delete');
            }
        });
    }
}
