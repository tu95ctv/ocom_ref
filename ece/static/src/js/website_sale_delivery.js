odoo.define('ece.checkout', function (require) {
    // var Checkout = require('website_sale_delivery.checkout');
    
    var core = require('web.core');
    var publicWidget = require('web.public.widget');

    var _t = core._t;
    var concurrency = require('web.concurrency');
    var dp = new concurrency.DropPrevious();


    publicWidget.registry.websiteSaleDelivery.include({
        
        start: function () {
            console.log('1232131231231232((d4))')
            var self = this;
            var $carriers = $('#delivery_carrier input[name="delivery_type"]');
            var $payButton = $('#o_payment_form_pay');
            // Workaround to:
            // - update the amount/error on the label at first rendering
            // - prevent clicking on 'Pay Now' if the shipper rating fails
            if ($carriers.length > 0) {
                if ($carriers.filter(':checked').length === 0) {
                    $payButton.prop('disabled', true);
                    var disabledReasons = $payButton.data('disabled_reasons') || {};
                    disabledReasons.carrier_selection = true;
                    $payButton.data('disabled_reasons', disabledReasons);
                }
                // $carriers.filter(':checked').off('click');
            }
    
            // Asynchronously retrieve every carrier price
            _.each($carriers, function (carrierInput, k) {
                self._showLoading($(carrierInput));
                self._rpc({
                    route: '/shop/carrier_rate_shipment',
                    params: {
                        'carrier_id': carrierInput.value,
                    },
                }).then(self._handleCarrierUpdateResultBadge.bind(self));
            });
    
            // return this._super.apply(this, arguments);
        },

        _onCarrierClick: function (ev) {
            console.log('ev.currentTarget***', ev.currentTarget)
            var $radio = $(ev.currentTarget).find('input[type="radio"]');
            console.log('$radio.company',$radio.attr('company'))
            this._showLoading($radio);
            $radio.prop("checked", true);
            var $payButton = $('#o_payment_form_pay');
            $payButton.prop('disabled', true);
            var disabledReasons = $payButton.data('disabled_reasons') || {};
            disabledReasons.carrier_selection = true;
            $payButton.data('disabled_reasons', disabledReasons);
            dp.add(this._rpc({
                route: '/shop/update_carrier',
                params: {
                    carrier_id: $radio.val(),
                    company_id:$radio.attr('company')
                },
            })).then(this._handleCarrierUpdateResult.bind(this));
        },





    })
    
  

});
