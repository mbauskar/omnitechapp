from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr, flt, getdate, comma_and, cint
from response import build_response,report_error
from omnitechapp.doctype.package_detail.package_detail import update_user_package
from validate import validate_request, get_user_package_in_json_format

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
        pkg = get_user_package_in_json_format(frappe.local.form_dict.data)
    	if not update_user_package(pkg):
            raise Exception("Error while updating package")
    except Exception, e:
    	import traceback
    	print traceback.format_exc()
        error_code = "01"
        error_desc = cstr(e)
    finally:
    	frappe.response['X_ERROR_CODE'] = error_code
    	frappe.response['X_ERROR_DESC'] = error_desc
    	return build_response("json")
