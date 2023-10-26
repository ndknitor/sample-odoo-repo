odoo.define('kn_auto_backup.my_script', function (require) {
    "use strict";

    var core = require('web.core');

    var _t = core._t;

    // Your custom JavaScript code here
    $(document).ready(function () {
        if (odoo.session_info.is_logged_in) {
            // Execute your code when the user is logged in
            alert('Welcome, logged-in user!');
            // Add your code here
        }
    });
});
