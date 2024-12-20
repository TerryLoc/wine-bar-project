// Hide the alert message after 3 seconds (3000ms) on the booking page
setTimeout(function () {
  const alertMessage = document.getElementById('alert-message');
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

// Confirmation dialog for canceling booking
function confirmCancel(form) {
  return confirm('Are you sure you want to cancel the selected spots?');
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
  // Show booking modal and set form action URL based on wine ID
  $('#bookingModal').on('show.bs.modal', function (event) {
    const button = $(event.relatedTarget); // Button that triggered the modal
    const wineId = button.data('wine-id'); // Extract info from data-* attributes
    const modal = $(this);
    modal.find('#wineId').val(wineId); // Set the wine ID in the modal
    const actionUrlTemplate = modal.find('#bookingForm').data('url-template');
    const actionUrl = actionUrlTemplate.replace('0', wineId); // Replace placeholder with actual wine ID
    modal.find('#bookingForm').attr('action', actionUrl); // Set the form action URL
  });

  // Handle booking form submission
  $('#bookingForm').on('submit', function (event) {
    event.preventDefault(); // Prevent default form submission
    const form = $(this);
    const actionUrl = form.attr('action'); // Get the form action URL
    $.ajax({
      type: 'POST',
      url: actionUrl,
      data: form.serialize(), // Serialize form data for submission
      success: function (response) {
        if (response.success) {
          $('#bookingModal').modal('hide'); // Hide the booking modal
          $('#confirmationMessage').text(response.message); // Set confirmation message
          $('#confirmationModal').modal('show'); // Show confirmation modal
        } else {
          alert(response.message); // Show error message
        }
      },
      error: function () {
        alert('An error occurred. Please try again.'); // Show generic error message
      },
    });
  });

  // Handle booking cancellation
  document.querySelectorAll('form.inline-form').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault(); // Prevent default form submission
      if (!confirmCancel(form)) {
        return; // If user cancels, do nothing
      }
      const formData = new FormData(form); // Create FormData object from form
      const actionUrl = form.getAttribute('action'); // Get the form action URL
      fetch(actionUrl, {
        method: 'POST',
        body: formData, // Send form data
        headers: {
          'X-Requested-With': 'XMLHttpRequest', // Indicate AJAX request
        },
      })
        .then((response) => response.json()) // Parse JSON response
        .then((data) => {
          if (data.success) {
            alert(data.message); // Show success message
            location.reload(); // Reload the page
          } else {
            alert(data.message); // Show error message
          }
        })
        .catch((error) => {
          alert('An error occurred. Please try again.'); // Show generic error message
        });
    });
  });

  // Toggle password visibility for the first password field
  const togglePassword1 = document.querySelector('#togglePassword1');
  const password1 = document.querySelector('#id_password1');
  if (togglePassword1 && password1) {
    togglePassword1.addEventListener('click', function () {
      const type =
        password1.getAttribute('type') === 'password' ? 'text' : 'password'; // Toggle password field type
      password1.setAttribute('type', type);
      this.classList.toggle('fa-eye'); // Toggle eye icon
      this.classList.toggle('fa-eye-slash'); // Toggle eye-slash icon
    });
  }

  // Toggle password visibility for the second password field
  const togglePassword2 = document.querySelector('#togglePassword2');
  const password2 = document.querySelector('#id_password2');
  if (togglePassword2 && password2) {
    togglePassword2.addEventListener('click', function () {
      const type =
        password2.getAttribute('type') === 'password' ? 'text' : 'password'; // Toggle password field type
      password2.setAttribute('type', type);
      this.classList.toggle('fa-eye'); // Toggle eye icon
      this.classList.toggle('fa-eye-slash'); // Toggle eye-slash icon
    });
  }
});
