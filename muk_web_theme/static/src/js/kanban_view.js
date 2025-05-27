odoo.define('muk_web_theme.kanban_view', function (require) {
    "use strict";
    var WebClient = require('web.WebClient');
    WebClient.include({
        show_application: function() {
            this._super.apply(this, arguments);
            var $sidebar = this.$('.o_sidebar');
            if ($sidebar.length) {
                $sidebar.hide();
                var $menu_toggle = this.$('.o_menu_toggle');
                if ($menu_toggle.length) {
                    $menu_toggle.click();
                }
            }
        },
    });
});
