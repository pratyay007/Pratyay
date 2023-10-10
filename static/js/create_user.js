if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
  }


  $(document).ready(function () {
    // Function to update the "designation" dropdown based on the selected department
    function updateDesignationDropdown() {
      var selectedDepartment = $('#departmentNumber').val();
      var designationDropdown = $('#designation');

      // Clear existing options
      designationDropdown.empty();

      // Define options based on the selected department
      if (selectedDepartment === 'Management') {
        designationDropdown.append('<option value="CEO">CEO</option>');
        designationDropdown.append('<option value="Director & CTO">Director & CTO</option>');
        designationDropdown.append('<option value="Chaiman & Managing Director">Chaiman & Managing Director</option>');
      } else if (selectedDepartment === 'HR') {
        designationDropdown.append('<option value="Manager-HRM & Excellence">Manager-HRM & Excellence</option>');
        designationDropdown.append('<option value="HR Associate">HR Associate</option>');
      } else if (selectedDepartment === 'IT') {

        designationDropdown.append('<option value="Delivery Manager">Delivery Manager</option>');
        designationDropdown.append('<option value="IDAM & Voltage Lead">IDAM & Voltage Lead</option>');
        designationDropdown.append('<option value="Cyber Security Infrastructure Lead">Cyber Security Infrastructure Lead</option>');
        designationDropdown.append('<option value="IAM & Linux Administrator">IAM & Linux Administrator</option>');
        designationDropdown.append('<option value="Developer-Application & Data Security">Developer-Application & Data Security</option>');
        designationDropdown.append('<option value=" Java Developer"> Java Developer</option>');
        designationDropdown.append('<option value=" Python Developer"> Python Developer</option>');
        designationDropdown.append('<option value="IAM Engineer">IAM Engineer</option>');
        designationDropdown.append('<option value="Sr. ITOM Developer & Integrator">Sr. ITOM Developer & Integrator</option>');
        designationDropdown.append('<option value="Senior-ITOM Engineer">Senior-ITOM Engineer</option>');
      
      } else if (selectedDepartment === 'Accounts') {
        designationDropdown.append('<option value="Manager-Finance & Account">Manager-Finance & Account</option>');
      } else if (selectedDepartment === 'Sales & Marketing') {
        designationDropdown.append('<option value="Regional Head - Sales & Business Development (Government & PSU)">Regional Head - Sales & Business Development</option>');
      }

      // Add a default option
      designationDropdown.prepend('<option value="" disabled selected>Select Designation</option>');
    }

    // Event listener for changes in the "departmentNumber" dropdown
    $('#departmentNumber').change(updateDesignationDropdown);

    // Initial setup when the page loads
    updateDesignationDropdown();

    
  // Flag to prevent multiple submissions
  var isSubmitting = false;

  // Event listener for form submission
  $('#create_user').submit(function (event) {
    // If already submitting, prevent additional submissions
    if (isSubmitting) {
      event.preventDefault();
      return;
    }

    // Disable the submit button
    $('#submitButton').prop('disabled', true);

    // Set the submitting flag
    isSubmitting = true;

    // Show a loading indicator or message if needed
    // You can add code here to indicate that the form is being processed

    // Submit the form after a 3-second delay
    setTimeout(function () {
      // Re-enable the submit button
      $('#submitButton').prop('disabled', false);

      // Reset the submitting flag
      isSubmitting = false;

      // Hide the loading indicator or message if needed
      // You can add code here to hide the processing indication

      // Submit the form
      $('#create_user')[0].submit();
    }, 3000); // 3 seconds delay
  });
  });  
  