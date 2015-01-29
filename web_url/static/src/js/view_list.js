openerp.web_url = function(openerp) {
    var _t = openerp.web._t,
       _lt = openerp.web._lt;
    var QWeb = openerp.web.qweb;

openerp.web.ListView.List = openerp.web.ListView.List.extend({
    render: function () {
        var self = this;
        if (this.$current) {
            this.$current.remove();
        }
        this.$current = this.$_element.clone(true);
        this.$current.empty().append(
            QWeb.render('ListView.rows', _.extend({
                    render_cell: function () {
                        return self.render_cell.apply(self, arguments); }
                }, this)));
        this.records.each(function(record){
            var $row = self.$current.find('[data-id=' + record.get('id') + ']');
            for(var i=0, length=self.columns.length; i<length; ++i) {
		if(self.columns[i].widget === 'url') {
                	var $cell = $row.find((_.str.sprintf('[data-field=%s]', self.columns[i].id)));
                	$cell.html(_.template('<a class="oe_form_uri" href="<%-text%>" target="blank" data-model="<%-model%>" data-id="<%-id%>"><%-text%></a>', 	{
                        text: openerp.web.format_value(record.get(self.columns[i].id), self.columns[i], ''),
                        model: self.columns[i].relation,
                        id: record.get(self.columns[i].id)[0]
                    	}))
                }
            }
        });
        this.pad_table_to(5);
    }
});

openerp.web.form.One2ManyList = openerp.web.ListView.List.extend({
    render: function () {
        var self = this;
        if (this.$current) {
            this.$current.remove();
        }
        this.$current = this.$_element.clone(true);
        this.$current.empty().append(
            QWeb.render('ListView.rows', _.extend({
                    render_cell: function () {
                        return self.render_cell.apply(self, arguments); }
                }, this)));
        this.records.each(function(record){
            var $row = self.$current.find('[data-id=' + record.get('id') + ']');
            for(var i=0, length=self.columns.length; i<length; ++i) {
                if(self.columns[i].widget === 'url') {
                	var $cell = $row.find((_.str.sprintf('[data-field=%s]', self.columns[i].id)));
                	$cell.html(_.template('<a class="oe_form_uri" href="<%-text%>" target="blank" data-model="<%-model%>" data-id="<%-id%>"><%-text%></a>', {
                        text: openerp.web.format_value(record.get(self.columns[i].id), self.columns[i], ''),
                        model: self.columns[i].relation,
                        id: record.get(self.columns[i].id)[0]
                    	}))
                }
            }
        });
        this.pad_table_to(5);
    }
});

};
