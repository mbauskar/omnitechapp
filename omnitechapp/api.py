from __future__ import unicode_literals
import json
import frappe
from frappe import _
from frappe.utils import cstr, flt, getdate, comma_and, cint
from response import build_response,report_error
from omnitechapp.doctype.package_detail.package_detail import modules as erp_modules
from omnitechapp.doctype.package_detail.package_detail import update_user_package

def handle():
    """
	Handler for `/api_name` methods
	**api_name = configured in api_hander hooks
	### Examples:

	`/api_name/{methodname}` will call a whitelisted method

	"""
    print "in handle"
    error_code = "02"
    error_desc = "Success"
    try:
    	validate_request()
        pkg = frappe.local.form_dict.data
    	update_user_package(pkg)
    except Exception, e:
    	import traceback
    	print traceback.format_exc()
        error_code = "01"
        error_desc = cstr(e)
    finally:
    	frappe.response['X_ERROR_CODE'] = error_code
    	frappe.response['X_ERROR_DESC'] = error_desc
    	return build_response("json")

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
        pacakge_id = request.get("P_PACKAGE_ID")
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
