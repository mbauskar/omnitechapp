import json
import frappe
from frappe.utils import cstr, flt, getdate, comma_and, cint
from response import build_response,report_error
from omnitechapp.doctype.package_detail.package_detail import modules as erp_modules

def validate_request():
    validate_url()
    validate_authentication_token()
    validate_request_parameters()

def validate_url():
	path = frappe.request.path[1:].split("/",2)
    # path[1] in services_fields.keys() <= check if url is correct
	if len(path) == 2 and path[1] == "setUserPackage":
		frappe.local.form_dict.cmd = path[1]
	else:
		frappe.throw(_("Invalid URL"))

def validate_authentication_token():
    request = json.loads(frappe.local.form_dict.data)
    token = get_auth_token()
    condition = request.get("P_AUTHENTICATE") != token and not request and \
                not request.get("P_AUTHENTICATE")
    if condition:
        raise Exception("Invalid authentication token")

def validate_request_parameters():
    """
        # validate min, max number of users
        # validate allowed modules
        # validate package ID
    """
    request = json.loads(frappe.local.form_dict.data)
    if request:
        package_id = request.get("P_PACKAGE_ID")
        min_users = request.get("P_MIN_USERS")
        max_users = request.get("P_MAX_USERS")
        modules = request.get("P_MODULES")
        desc = request.get("P_DESC")

        if package_id and min_users and max_users and modules and desc:
            # validate min, max users
            if min_users < 1:
                raise Exception("Minimum numbers of user cannot be less than 1")
            if max_users < min_users:
                raise Exception("Maximum numbers of user should be greate than Minimum Users")

            # validate allowed module
            module_list = modules.split(",")
            invalid_mod = [mod for mod in module_list if mod not in erp_modules]
            if invalid_mod:
                raise Exception("Invalid Module(s) : %s"%(",".join(invalid_mod)))
        else:
            raise Exception("Manditory Parameter is missing, Please check the request parameters")

def get_auth_token():
    auth_token = frappe.conf.auth_token
    if not auth_token:
        raise Exception("Authentication token not found, Please contach Admin")
    else:
        return auth_token

def get_user_package_in_json_format(request):
    """
    Get request and prepare json in required format
    e.g:
        pkg = {
            "minimum_users":int,
            "maximum_users":int,
            "description":str,
            "allowed_modules":str,
            "package_id":str
        }
    """

    package = json.loads(request)

    return json.dumps({
        "minimum_users":package.get("P_MIN_USERS"),
        "maximum_users":package.get("P_MAX_USERS"),
        "description":package.get("P_DESC"),
        "allowed_modules":package.get("P_MODULES"),
        "package_id":package.get("P_PACKAGE_ID")
    })

# TODO
def validate_user(doc, method):
    pkg = get_package_detail()
    validate_users_count(pkg)
    validate_users_role()
    validate_allowed_modules()

def get_package_detail():
    pkg = frappe.get_doc("Package Detail", "Package Detail")
    return pkg.as_dict()

def validate_users_count(pkg):
    min_users = pkg.get("minimum_users")
    max_users = pkg.get("maximum_users")

    # get and check the current user count
    query = """SELECT count(name) FROM `tabUser` WHERE name NOT IN ['Guest','Administrator']"""
    result = frappe.db.sql(query, as_list=True)
    frappe.errprint(result)

def validate_users_role():
    pass

def validate_allowed_modules():
    pass
