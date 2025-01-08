import frappe
from requests import request
from frappe.integrations.utils import create_request_log

class sellerConnector:
    def __init__(self, seller):
        self.seller = seller
        self.prepare_connection()
    
    def prepare_connection(self):
        self.base_url = frappe.db.get_value("Hub Seller", self.seller, "erpnext_url")
        user = frappe.get_cached_doc("User", frappe.db.get_value("Hub Seller", self.seller, "owner"))
        self.headers = {
            "Content-Type": "application/json",
            "Hub-Authorization": "token {0}:{1}".format(user.api_key, user.get_password("api_secret"))
        }
    
    def create_lead_for_item_inquiry(self, data):
        url = self.base_url+"/capture_lead"
        integration_request = create_request_log(data=data, service_name="Hub Seller Lead", request_headers=self.headers, url=url)
        try:
            response = request(method="POST", url=url, data=frappe.as_json(data), headers=self.headers)
            integration_request.db_set("output", frappe.as_json(response.json(), indent=4))
            if response.status_code == 200:
                integration_request.db_set("status", "Completed")
                return response.json().get("message")
            else:
                integration_request.db_set("output", frappe.as_json(response.json(), indent=4))
                integration_request.db_set("status", "Failed")
                frappe.throw(frappe.as_json(response.json(), indent=4))
        except Exception:
            frappe.log_error("Error while creating Hub Seller Lead", frappe.get_traceback())
