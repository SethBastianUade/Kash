// Funciones de utilidad
const showLoading = () => {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    document.body.appendChild(spinner);
};

const hideLoading = () => {
    const spinner = document.querySelector('.spinner');
    if (spinner) {
        spinner.remove();
    }
};

// Manejo de formularios
document.addEventListener('DOMContentLoaded', () => {
    // Validación de formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Manejo de alertas
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Funciones para el manejo de QR
const generateQR = async (amount = null) => {
    showLoading();
    try {
        const response = await fetch('/api/generate-qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount }),
        });
        const data = await response.json();
        if (data.success) {
            document.getElementById('qr-code').src = data.qr_url;
        }
    } catch (error) {
        console.error('Error generating QR:', error);
    } finally {
        hideLoading();
    }
};

const scanQR = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            showLoading();
            const formData = new FormData();
            formData.append('qr', file);
            try {
                const response = await fetch('/api/scan-qr', {
                    method: 'POST',
                    body: formData,
                });
                const data = await response.json();
                if (data.success) {
                    // Mostrar modal con detalles del pago
                    const modal = new bootstrap.Modal(document.getElementById('paymentModal'));
                    document.getElementById('payment-amount').textContent = data.amount;
                    document.getElementById('payment-user').textContent = data.user;
                    modal.show();
                }
            } catch (error) {
                console.error('Error scanning QR:', error);
            } finally {
                hideLoading();
            }
        }
    };
    input.click();
};

// Funciones para el dashboard
const updateBalance = async () => {
    try {
        const response = await fetch('/api/balance');
        const data = await response.json();
        document.getElementById('balance-amount').textContent = `$${data.balance.toFixed(2)}`;
    } catch (error) {
        console.error('Error updating balance:', error);
    }
};

const loadTransactions = async () => {
    showLoading();
    try {
        const response = await fetch('/api/transactions');
        const data = await response.json();
        const transactionsList = document.getElementById('transactions-list');
        transactionsList.innerHTML = data.transactions.map(transaction => `
            <div class="transaction-card card mb-2 fade-in">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-0">${transaction.type}</h6>
                            <small class="text-muted">${transaction.date}</small>
                        </div>
                        <span class="${transaction.amount > 0 ? 'text-success' : 'text-danger'}">
                            ${transaction.amount > 0 ? '+' : ''}$${transaction.amount.toFixed(2)}
                        </span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading transactions:', error);
    } finally {
        hideLoading();
    }
};

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    // Actualizar balance y transacciones si estamos en el dashboard
    if (document.getElementById('balance-amount')) {
        updateBalance();
        loadTransactions();
    }
}); 