openerp.web_smile_hide_buttons = function(openerp) {

    // Models for which we'll hide create and duplicate buttons
    var MODELS_TO_HIDE = ['packaging.board'];

    // Hide the create button on all list views, which affect tree views and many2one pop-up search view
    openerp.web.ListView.include({
        start: function() {
            var self = this;
            var ret = this._super.apply(this, arguments);
            var res_model = this.dataset.model;
            if ($.inArray(res_model, MODELS_TO_HIDE) != -1) {
                self.options.addable = false;
            };
            return ret;
        },
    });

    // Hide the save button on form views
    openerp.web.FormView.include({
        on_loaded: function(data) {
            var self = this;
            var ret = this._super.apply(this, arguments);
            var res_model = this.dataset.model;
            if ($.inArray(res_model, MODELS_TO_HIDE) != -1) {
                this.$element.find('button.oe_form_button_save').remove();
            };
            return ret;
        },
    });

    // Hide the create and duplicate button on all page views (i.e. read-only form views)
    openerp.web.PageView.include({
        on_loaded: function(data) {
            var self = this;
            var ret = this._super.apply(this, arguments);
            var res_model = this.dataset.model;
            if ($.inArray(res_model, MODELS_TO_HIDE) != -1) {
                this.$element.find('button.oe_form_button_create').remove();
                this.$element.find('button.oe_form_button_duplicate').remove();
            };
            return ret;
        },
    });

};
