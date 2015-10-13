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
		# TODO validation on minimum and maximum number of user
		print "Updating the USER PACKAGE"
		pkg = json.loads(pkg_json)
		for field, value in pkg.iteritems():
			frappe.db.set_value("Package Detail", "Package Detail", field, value)
		frappe.db.commit()
		print "USER PACKAGE updated successfully"
	except Exception, e:
		import traceback
		print "Error while updating package"
		# TODO disable site ?
		print traceback.format_exc();
