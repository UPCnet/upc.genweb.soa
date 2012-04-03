/*global jQuery, document*/

jQuery(function ($) {
    "use strict";
    $(document).ready(function () {
        $('.peticio-dades-soa').prepOverlay({
            subtype: 'ajax',
            filter: '#content>*'
        });

    });
});