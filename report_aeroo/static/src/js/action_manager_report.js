odoo.define('report_aeroo.ActionManager', function (require) {
"use strict";

var ActionManager = require('web.ActionManager');

ActionManager.include({

    _makeReportUrls: function (action) {
        var self = this;
        var result = self._super(action);
        result['aeroo'] = result['pdf'].replace('/report/pdf/', '/report/aeroo/');
        return result;
    },

    _executeReportAction: function (action, options){
        var self = this;
        if (action.report_type === 'aeroo'){
            return self._triggerDownload(action, options, 'aeroo');
        } else {
            return self._super(action, options);
        }
    }
});

});
