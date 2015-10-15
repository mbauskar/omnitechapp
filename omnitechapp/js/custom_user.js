frappe.ui.form.on("User",{
    onload: function(frm){
        // hide or unhide role according to package
        // if user is admin then skip
        if(user != "Administrator")
            get_modules();
    },
    reload: function(frm){
        // hide or unhide role according to package
        // if user is admin then skip
        if(user != "Administrator")
            get_modules();
    }
});

get_modules = function(){
    // get allowed module for users from Package Detail
    frappe.call({
        method: "omnitechapp.omnitechapp.doctype.package_detail.package_detail.get_package_detail",
        callback: function(r){
            if(r.message){
                pkg = r.message;
                hide_roles(pkg.roles_to_hide);
                hide_modules(pkg.allowed_modules);
            }
        }
    });
}

hide_roles = function(roles){
    if(roles){
        $.each(roles, function(i, role){
            role_div = $("[data-user-role='"+ role +"']");
            role_div.css("display", "none");
            role_div.find("input[type='checkbox']").prop("checked",0);
        });
    }
}

hide_modules = function(allowed_modules){
    if(allowed_modules){
        $.each(keys(frappe.boot.modules), function(i, mod){
            if(!in_list(allowed_modules, mod)){
                console.log(mod);
                $("[data-module='"+ mod +"']").prop("checked",0);
                $("[data-module='"+ mod +"']").parents().eq(2).css("display","none");
            }
        })
    }
}
