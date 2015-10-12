cur_frm.cscript.onload = function(doc, dt, dn) {
	if(has_common(user_roles, ["Administrator", "System Manager"])) {
		// if(!cur_frm.roles_editor) {
			var module_area = $('<div style="min-height: 300px">')
				.appendTo(cur_frm.fields_dict.modules_html.wrapper);
			cur_frm.module_editor = new frappe.ModuleEditor(cur_frm, module_area)
		// } else {
		// 	cur_frm.roles_editor.show();
		// }
	}
}

frappe.ModuleEditor = Class.extend({
	init: function(frm, wrapper) {
		this.wrapper = $('<br><div class="row module-block-list"></div>').appendTo(wrapper);
		this.frm = frm;
		this.make();
	},
	make: function() {
		var me = this;
		modules = cur_frm.doc.allowed_modules.split(",")
		$.each(modules, function(i, m) {
			html = '<center><div class="case-wrapper" data-name="%(title)s" \
			data-link="Module/%(title)s" title="%(title)s"><div class="app-icon" style="background-color: \
			%(bgcolor)s" title="%(title)s" align="center"><i class="%(icon)s" title="%(title)s"></i>\
			</div><div class="case-label text-ellipsis"> <div><span class="case-label-text" \
			style="color: black;text-shadow: none;">%(title)s</span></div></div></div><center>'

			$(repl(html, {
				title: m,
				icon:frappe.boot.modules[m].icon,
				bgcolor:frappe.boot.modules[m].color}
			)).appendTo(me.wrapper);
		});
		this.bind();
	},
	refresh: function() {
		var me = this;
		this.wrapper.find(".block-module-check").prop("checked", true);
		$.each(this.frm.doc.block_modules, function(i, d) {
			me.wrapper.find(".block-module-check[data-module='"+ d.module +"']").prop("checked", false);
		});
	},
	bind: function() {
		this.wrapper.on("change", ".block-module-check", function() {
			var module = $(this).attr('data-module');
			if($(this).prop("checked")) {
				// remove from block_modules
				me.frm.doc.block_modules = $.map(me.frm.doc.block_modules || [], function(d) { d.module != module });
			} else {
				me.frm.add_child("block_modules", {"module": module});
			}
		});
	}
})
