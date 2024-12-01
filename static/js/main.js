// Hide the alert message after 5 seconds (5000ms) on the booking page
setTimeout(function () {
  var alertMessage = document.getElementById('alert-message');
  if (alertMessage) {
    alertMessage.style.display = 'none';
  }
}, 3000);

// Toggle between profile view and edit mode
function toggleEditMode() {
  const profileView = document.getElementById('profileView');
  const profileEdit = document.getElementById('profileEdit');
  if (profileView.style.display === 'none') {
    profileView.style.display = 'block';
    profileEdit.style.display = 'none';
  } else {
    profileView.style.display = 'none';
    profileEdit.style.display = 'block';
  }
}

// Confirmation dialog for saving changes
function confirmSaveChanges() {
  const form = document.querySelector('#profileEdit form');
  if (!form.checkValidity(false)) {
    alert('Please correct the highlighted errors before saving.');
    return false;
  }
  return confirm('Are you sure you want to save the changes?');
}

// booking modal
document.addEventListener('DOMContentLoaded', function () {
  $('#bookingModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var wineId = button.data('wine-id'); // Extract info from data-* attributes
    var modal = $(this);
    modal.find('#wineId').val(wineId);
    var actionUrl = modal
      .find('#bookingForm')
      .data('url-template')
      .replace('0', wineId);
    modal.find('#bookingForm').attr('action', actionUrl);
  });
});
