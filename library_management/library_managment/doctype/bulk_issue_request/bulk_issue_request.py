import frappe
from frappe.model.document import Document


class BulkIssueRequest(Document):
	def validate(self):
		if not self.items:
			frappe.throw("Please add at least one Article to issue")

		articles_seen = []
		for row in self.items:
			if row.article in articles_seen:
				frappe.throw(f"Article {row.article} is added more than once")
			articles_seen.append(row.article)

		self.total_items = len(self.items)

	def before_submit(self):
		# Submit se pehle check karo koi article already issued to nahi
		for row in self.items:
			article = frappe.get_doc("Article", row.article)
			if article.status == "Issued":
				frappe.throw(f"Article {row.article} is already issued to someone else")

	def on_submit(self):
		# Submit hone ke baad har article ke liye Library Transaction banao
		for row in self.items:
			transaction = frappe.get_doc({
				"doctype": "Library Transaction",
				"article": row.article,
				"library_member": self.library_member,
				"type": "Issue",
				"date_of_transaction": self.request_date,
			})
			transaction.insert()
			transaction.submit()
			row.status = "Issued"

		frappe.msgprint(f"{len(self.items)} articles issued successfully")
	
	def on_cancel(self):
		for row in self.items:
			article = frappe.get_doc("Article", row.article)
			article.status = "Available"
			article.save()	