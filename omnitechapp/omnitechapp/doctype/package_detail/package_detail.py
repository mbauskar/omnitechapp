# -*- coding: utf-8 -*-
# Copyright (c) 2015, omnitechapp and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import json

class PackageDetail(Document):
	pass

def update_user_package(pkg_json):
	"""Update the Package Details doctype with pkg_json content"""
	try:
		print "Updating the USER PACKAGE"

		pkg = json.loads(pkg_json)
		for field, value in pkg.iteritems():
			frappe.db.set_value("Package Detail", "Package Detail", field, value)
		# TODO remove the admin roles
		remove_admin_roles()
		frappe.db.commit()

		print "USER PACKAGE updated successfully"
		return True
	except Exception, e:
		import traceback
		print "Error while updating package"
		print traceback.format_exc();
		raise Exception("ERROR : %s"%(e))

# all erp, frappe modules
modules = [
	"Accounts", "Activity", "Api Handler", "Buying", "CRM", "Calendar", "Core",
	"File Manager", "HR", "Installer", "Integrations", "Learn", "Manufacturing",
	"Messages", "Notes", "Omnitechapp", "POS", "Projects", "Selling", "Setup",
	"Stock", "Support", "To Do", "Website"
]

# module roles mapper
mapper = {
    "Accounts":["Accounts Manager", "Accounts User", "Auditor", "Purchase User", "Sales User"],
    # "Core":["Customer"],
    "Activity":["Projects User", "System Manager"],
    "Buying":["Purchase Master Manager", "Purchase Manager", "Purchase User", "Supplier"],
    # "CRM":["Customer"],
    # "Core":["Customer"],
	"HR":["Expense Approver", "HR Manager", "HR User", "Leave Approver"],
    # "HR":["Employee", "Expense Approver", "HR Manager", "HR User", "Leave Approver"],
    "Integrations":["Customer"],
    "Manufacturing":["Manufacturing Manager", "Manufacturing User",],
    # "Messages":["Customer"],
    # "Notes":["Customer"],
    # "POS":["Customer"],
    "Projects":["Projects User", "Projects Manager"],
    "Selling":["Sales Manager", "Sales User", "Sales Master Manager"],
    "Setup":["Customer"],
    "Stock":["Item Manager", "Stock Manager", " Stock User"],
    "Support":["Support Team", "Maintenance User", "Maintenance Manager", ],
    "Website":["Website Manager"]
}

@frappe.whitelist()
def get_package_detail():
	doc = frappe.get_doc("Package Detail", "Package Detail")
	if doc:
		result = get_roles_to_restrict(doc)
		return result
	else:
		return None

def get_roles_to_restrict(doc):
	roles = []
	allowed_modules = doc.allowed_modules.split(",")
	[roles.extend(mapper.get(mod)) for mod in modules if mod not in allowed_modules and mapper.get(mod)]
	restricted_roles = list(set(roles))
	return {
		"roles_to_hide": restricted_roles,
		"allowed_modules": allowed_modules
	}

@frappe.whitelist()
def get_allowed_roles():
	doc = frappe.get_doc("Package Detail", "Package Detail")
	if doc:
		all_roles = [r[0] for r in frappe.db.sql("""select name from tabRole where name not in ('Administrator', 'Guest', 'All') order by name""")]
		restricted_roles = get_roles_to_restrict(doc)
		return [role for role in all_roles if role not in restricted_roles.get("roles_to_hide")]
	else:
		return None

def remove_admin_roles():
	"""Remove all the Administrator roles except allowed roles"""
	try:
		roles = ["'%s'"%(role) for role in get_allowed_roles()]
		
		if not roles:
			frappe.throw("Error occured during setup, Please contact Administrator")
		
		query = """ DELETE FROM tabUserRole WHERE parent='Administrator' AND
					role NOT IN ('Administrator',%s)"""%(",".join(roles))
		
		frappe.db.sql(query)
	except Exception, e:
		frappe.throw(e)