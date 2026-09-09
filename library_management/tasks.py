import frappe
from frappe.utils import today

def mark_overdue_transactions():
	overdue_transactions = frappe.get_all(
		"Library Transaction",
		filters={
			"type": "Issue",
			"docstatus": 1,
		},
		fields=["name", "article"]
	)
	frappe.msgprint(f"Checked {len(overdue_transactions)} transactions")