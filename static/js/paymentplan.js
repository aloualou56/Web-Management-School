function openPaymentPlanModal() {
    document.getElementById('PaymentPlanModal').style.display = 'flex';
}

function closePaymentPlanModal() {
    document.getElementById('PaymentPlanModal').style.display = 'none';
    
    resetPaymentPlanForm(); 
}

function resetPaymentPlanForm() {
    const PaymentPlanForm = document.getElementById('PaymentPlanForm');
    PaymentPlanForm.reset();

    $('#months').val(''); 
    $('#months').trigger('chosen:updated');

    document.querySelector('#PaymentPlanModal h2').textContent = 'Προσθήκη Σχεδίου Πληρωμής';
    document.querySelector('.modal-submit-btn').textContent = 'Προσθήκη';
}

$(document).ready(function() {
    $('.chosen-select').chosen({
        placeholder_text_multiple: "Επιλέξτε Μήνες",  
        no_results_text: "Δεν βρέθηκαν αποτελέσματα",     
        width: "100%"                                     
    });
});

document.getElementById('monthly_fee').addEventListener('input', function() {
    this.value = this.value.replace(/[^0-9.]/g, ''); 
});

document.getElementById('one_time_fee').addEventListener('input', function() {
    this.value = this.value.replace(/[^0-9.]/g, ''); 
});


document.getElementById('PaymentPlanForm').addEventListener('submit', function(event) {
    event.preventDefault(); 

    const PaymentPlan_id = document.getElementById('PaymentPlan_id').value;
    const url = PaymentPlan_id ? `/paymentplans/${PaymentPlan_id}/update/` : '/paymentplans/';  
    const method = PaymentPlan_id ? 'POST' : 'POST'; 

    const formData = new FormData(this); 

    $.ajax({
        url: url,
        method: method,
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            closePaymentPlanModal()
            
            location.reload();
        },
        error: function() {
            alert('An error occurred while saving\.'); 
        }
    });
});

function editPaymentPlan(PaymentPlan_id) {
    $.ajax({
        url: `/paymentplans/${PaymentPlan_id}/edit/`, 
        method: 'GET',
        success: function(PaymentPlan) {
            populatePaymentPlanForm(PaymentPlan); 
            openPaymentPlanModal(); 
        },
        error: function() {
            alert('Could not fetch \data.'); 
        }
    });
}

function populatePaymentPlanForm(PaymentPlan) {
    document.getElementById('PaymentPlan_id').value = PaymentPlan.id;
    document.getElementById('name').value = PaymentPlan.name;
    document.getElementById('description').value = PaymentPlan.description;
    document.getElementById('one_time_fee').value = PaymentPlan.one_time_fee;
    document.getElementById('monthly_fee').value = PaymentPlan.monthly_fee;
    

    $('#months').val(PaymentPlan.months);
    $('#months').trigger('chosen:updated');

    document.querySelector('#PaymentPlanModal h2').textContent = 'Επεξεργασία Σχεδίου Πληρωμής';
    document.querySelector('.modal-submit-btn').textContent = 'Αποθήκευση';
}

function deletePaymentPlan(PaymentPlan_id) {
    if (confirm('Are you sure you want to delete this?')) {
        
        $.ajax({
            url: `/paymentplans/${PaymentPlan_id}/delete/`,  
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