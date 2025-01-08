# Copyright (c) 2024, pwctech technologies private limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from hub_marketplace.api.seller_connector import sellerConnector

class HubLead(Document):
	def validate(self):
		self.send_leads_to_sellers()
	
	def send_leads_to_sellers(self):
		if not any(self.default_seller == s.seller for s in self.hub_sellers):
			self.append("hub_sellers", {"seller": self.default_seller})
		if self.contact_sellers:
			self.add_other_sellers()
		self.connect_sellers()

	def add_other_sellers(self):
		return

	def connect_sellers(self):
		item_url = "https://sit.mytra.money/hub_marketplace/product/{0}".format(self.item)
		lead_name = frappe.db.get_value("User", self.buyer, "full_name")
		data = {
			"lead_name": lead_name,
			"company_name": self.company_name or lead_name,
			"email_id": self.buyer,
			"phone": self.contact_number,
			"subject": "Hub Marketplace Lead",
			"message": """
				<p>You have a lead from hubmarket.place. A buyer is looking to purchase an item ({url}) you may be dealing with.</p>
				<p>If you supply this item, do contact the buyer to fulfill the requirement.</p>
				<p>Buyer Remarks:{remarks}</p>
			""".format(url=item_url, remarks=self.remarks)
		}
		for s in self.hub_sellers:
			if s.seller_lead_reference:
				continue
			seller_lead = sellerConnector(s.seller).create_lead_for_item_inquiry(data)
			s.seller_lead_reference = seller_lead.get("name")





