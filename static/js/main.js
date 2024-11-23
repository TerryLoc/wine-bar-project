// Hide the alert message after 5 seconds (5000ms) on the booking page
setTimeout(function () {
  var alertMessage = document.getElementById('alert-message');
  if (alertMessage) {
    alertMessage.style.display = 'none';
  }
}, 3000);

// profile page edit mode toggle
function toggleEditMode() {
  const viewDiv = document.getElementById('profileView');
  viewDiv.style.display = viewDiv.style.display === 'none' ? 'block' : 'none';
}
