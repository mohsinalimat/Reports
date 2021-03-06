# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _
#from frappe.utils import (cstr, validate_email_address, cint, comma_and, has_gravatar, now, getdate, nowdate)
#from frappe.model.mapper import get_mapped_doc
import requests
#from erpnext.controllers.selling_controller import SellingController
#from frappe.contacts.address_and_contact import load_address_and_contact
#from erpnext.accounts.party import set_taxes
#from frappe.email.inbox import link_communication_to_document

#sender_field = "email_id"

class NewEnquiry(Document):
    pass


@frappe.whitelist(allow_guest=True)
def existing_lead(mobile_number,name=None,gender=None,blood_group=None,age=None,diseases=None,address=None,city=None,landmark=None):
	if mobile_number:
		lead = frappe.db.sql("""select * from `tabLead`
                                where name=%s """, (mobile_number),as_dict=1)
		#frappe.msgprint(str(lead))
		if not lead:
			form=frappe.new_doc("Lead")
			form.phone=mobile_number
			form.lead_name=name
			form.mobile_number=mobile_number
			form.gender=gender
			form.blood_group=blood_group
			form.age=age
			form.diseases=diseases
			form.save()
			add_form=frappe.new_doc("Address")
			add_form.address_title = name
			add_form.address_line1=address
			add_form.city=city
			add_form.address_line2=landmark
			add_form.insert()
			child = add_form.append('links', {})
			child.link_doctype= "Lead"
			child.link_name=mobile_number
			child.link_title=mobile_number
			child.parent = add_form.name
			frappe.msgprint(str(child))
			child.insert()
			#add_form.save()
			frappe.msgprint("Successfully Added")
		else:
			form=frappe.get_doc("Lead",mobile_number)
			child=form.append('realtions',{})
			child.name1=name
			child.diseases=diseases
			frappe.msgprint(str(child))
			child.insert()
			frappe.msgprint("Add")
		return lead

@frappe.whitelist(allow_guest=True)
def search(state):
	if state:
		data=frappe.db.sql_list("""select distinct district_name from `tabPincode Master` where state_name=%s """,(state))
		#frappe.msgprint(str(data))
		return data
@frappe.whitelist(allow_guest=True)
def search_tehsil(district):
	if district:
		tehsils=frappe.db.sql_list("""select distinct related_headoffice from `tabPincode Master` where  related_headoffice=%s""",(district))
		#frappe.msgprint(str(tehsils))
		return tehsils
@frappe.whitelist(allow_guest=True)
def search_city(tehsil):
	if tehsil:
		cities=frappe.db.sql_list("""select distinct related_suboffice from `tabPincode Master` where related_headoffice=%s""",(tehsil))
		#frappe.msgprint(str(cities))
		return cities
@frappe.whitelist(allow_guest=True)
def search_pincode(city):
	if city:
		pincode=frappe.db.sql("""select pincode from `tabPincode Master` where related_suboffice=%s""",(city))
		return pincode
@frappe.whitelist(allow_guest=True)
def handling_incoming_call(**kwargs):
	response=kwargs
	frappe.msgprint(response)
