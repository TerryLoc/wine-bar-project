// Hide the alert message after 3 seconds (3000ms) on the booking page
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
  $('#bookingModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); // Button that triggered the modal
    var wineId = button.data('wine-id'); // Extract info from data-* attributes
    var modal = $(this);
    modal.find('#wineId').val(wineId);
    var actionUrlTemplate = modal.find('#bookingForm').data('url-template');
    var actionUrl = actionUrlTemplate.replace('0', wineId);
    modal.find('#bookingForm').attr('action', actionUrl);
  });

  // Handle booking form submission
  $('#bookingForm').on('submit', function (event) {
    event.preventDefault();
    var form = $(this);
    var actionUrl = form.attr('action');
    $.ajax({
      type: 'POST',
      url: actionUrl,
      data: form.serialize(),
      success: function (response) {
        if (response.success) {
          $('#bookingModal').modal('hide');
          $('#confirmationMessage').text(response.message);
          $('#confirmationModal').modal('show');
        } else {
          alert(response.message);
        }
      },
      error: function () {
        alert('An error occurred. Please try again.');
      },
    });
  });

  // Handle booking cancellation
  document.querySelectorAll('form.inline-form').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!confirmCancel(form)) {
        return;
      }
      var formData = new FormData(form);
      var actionUrl = form.getAttribute('action');
      fetch(actionUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert(data.message);
            location.reload();
          } else {
            alert(data.message);
          }
        })
        .catch((error) => {
          alert('An error occurred. Please try again.');
        });
    });
  });

  // Toggle password visibility
  const togglePassword1 = document.querySelector('#togglePassword1');
  const password1 = document.querySelector('#id_password1');
  togglePassword1.addEventListener('click', function () {
    const type =
      password1.getAttribute('type') === 'password' ? 'text' : 'password';
    password1.setAttribute('type', type);
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
  });

  const togglePassword2 = document.querySelector('#togglePassword2');
  const password2 = document.querySelector('#id_password2');
  togglePassword2.addEventListener('click', function () {
    const type =
      password2.getAttribute('type') === 'password' ? 'text' : 'password';
    password2.setAttribute('type', type);
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
  });
});
