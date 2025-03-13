"use strict";

// Class definition
var CheckinApp = function() {
    // Private functions
    var handleCheckInOut = function() {
        // Handle geolocation for check-in
        if (document.querySelector('.checkin-form')) {
            document.querySelectorAll('.checkin-form').forEach(function(form) {
                form.addEventListener('submit', function(e) {
                    const locationInputs = this.querySelector('.needs-location');
                    if (locationInputs) {
                        e.preventDefault();
                        
                        if (navigator.geolocation) {
                            navigator.geolocation.getCurrentPosition(function(position) {
                                const latInput = document.createElement('input');
                                latInput.type = 'hidden';
                                latInput.name = 'checkin_latitude';
                                latInput.value = position.coords.latitude;
                                
                                const longInput = document.createElement('input');
                                longInput.type = 'hidden';
                                longInput.name = 'checkin_longitude';
                                longInput.value = position.coords.longitude;
                                
                                form.appendChild(latInput);
                                form.appendChild(longInput);
                                form.submit();
                            }, function(error) {
                                alert("Error getting location: " + error.message);
                            });
                        } else {
                            alert("Geolocation is not supported by this browser.");
                        }
                    }
                });
            });
        }
    };

    // Mobile responsive menu handlers
    var handleMobileMenu = function() {
        // Handle mobile toggler
        const togglerBtn = document.getElementById('kt_aside_mobile_toggle');
        if (togglerBtn) {
            togglerBtn.addEventListener('click', function() {
                document.body.classList.toggle('aside-mobile-toggled');
            });
        }
    };

    // Public methods
    return {
        init: function() {
            handleCheckInOut();
            handleMobileMenu();
        }
    };
}();

// On document ready
document.addEventListener("DOMContentLoaded", function() {
    CheckinApp.init();
});