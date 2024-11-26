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
  profileView.style.display =
    profileView.style.display === 'none' ? 'block' : 'none';
  profileEdit.style.display =
    profileEdit.style.display === 'none' ? 'block' : 'none';
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
