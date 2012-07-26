/*global jQuery, document*/

jQuery(function ($) {
    "use strict";
    $(document).ready(function () {
        $('.peticio-dades-soa').prepOverlay({
            subtype: 'ajax',
            filter: '#content>*'
        });

    $('body').delegate('.kssattr-formname-gn6-recollir-dades input#form-buttons-envia', 
                       'click', 
                       function(event) {
                           event.preventDefault()
                           var $this = $(this)
                           this.disabled=true
                           $this.css({'vertical-align': 'top'})
			   $this.after('<img src="++resource++upc.genweb.soa.images/progressBar.gif" style="margin-left:10px;">')
                           $this.attr('value', 'Enviant ...')
                           $this.attr('name', 'disabled')
                           var $form = $this.closest('form')
                           $form.append('<input type="hidden" name="form.buttons.envia" value="Envia">')
                           $form.submit()
                       })

    });

});
