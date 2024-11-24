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
