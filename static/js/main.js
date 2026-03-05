// Main JavaScript for IT Hub Internal

// Show delete confirmation modal
function showDeleteModal(itemName, deleteUrl) {
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    document.getElementById('deleteItemName').textContent = itemName;
    document.getElementById('deleteForm').action = deleteUrl;
    modal.show();
}

document.addEventListener('DOMContentLoaded', function() {
    // Delete button click handlers
    document.querySelectorAll('.btn-delete-item').forEach(function(button) {
        button.addEventListener('click', function() {
            const itemName = this.getAttribute('data-item-name');
            const deleteUrl = this.getAttribute('data-delete-url');
            showDeleteModal(itemName, deleteUrl);
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm delete actions (legacy)
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Apakah Anda yakin ingin menghapus data ini?')) {
                e.preventDefault();
            }
        });
    });
});
