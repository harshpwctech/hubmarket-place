import frappe
from frappe.commands.site import add_new_user
from frappe.core.doctype.user.user import generate_keys


def register_seller(user_data):
    frappe.session.user = "Administrator"
    user_info = user_data.get("user")
    user_email = user_info["email"]
    user = frappe.db.get("User", {"email": user_email})
    if user:
        user = frappe.get_doc("User", user)
        user.add_roles("Hub Seller")
        api_secret = generate_keys(user_email)
    else:
        add_new_user(email=user_email, first_name=user_info["first_name"], last_name=user_info["last_name"], role=["Hub Seller"])
        api_secret = generate_keys(user_email)
    return {"api_key": frappe.db.get_value("User", {"email": user_email}, "api_key"), "api_secret": api_secret["api_secret"]}

def update_catalog(catalog):
    seller_data = catalog["seller"]
    seller_items = catalog["items"]
    hub_seller = update_seller_info(seller_data)
    frappe.enqueue(update_seller_items, queue="long", seller_items=seller_items, hub_seller=hub_seller)
    return hub_seller
    
def update_seller_info(seller_data):
    hub_seller_data = {
        "doctype": "Hub Seller",
        "seller_name": seller_data.get("seller_name"),
        "brand": seller_data.get("brand"),
        "logo": seller_data.get("logo"),
        "erpnext_url": seller_data.get("erpnext_url"),
        "mobile_number": seller_data.get("mobile_number"),
        "email": seller_data.get("email")
    }
    if not frappe.db.exists("Hub Seller", {"erpnext_url": seller_data.get("erpnext_url")}):
        hub_seller = frappe.get_doc(hub_seller_data).insert()
        frappe.get_doc({
            "doctype": "User Permission",
            "user": frappe.session.user,
            "allow": "Hub Seller",
            "for_value": hub_seller.name
            }).insert(ignore_permissions=True)
    else:
        hub_seller = frappe.get_last_doc("Hub Seller", filters={"erpnext_url": seller_data.get("erpnext_url")})
        hub_seller.update(hub_seller_data)
    
    frappe.db.commit()
    
    for w in seller_data.get("warehouse_details"):
        address = w.get("address")
        address_data = {
            "doctype": "Address",
            "address_title": hub_seller.seller_name,
            "address_type": "Warehouse",
            "address_line1": address.get("address_line1"),
            "address_line2": address.get("address_line2"),
            "city": address.get("city"),
            "country": address.get("country"),
            "pincode": address.get("pincode"),
            "state": address.get("state")
        }
        if len(hub_seller.locations):
            if any (w.get("warehouse_id") == l.warehouse_id for l in hub_seller.locations):
                for l in hub_seller.locations:
                    if w.get("warehouse_id") == l.warehouse_id:
                        update_address(address_data, l.address, hub_seller)
                        l.disabled = w.get("disabled")
            else:
                warehouse_address = add_address(address_data, hub_seller)
                hub_seller.append("locations", {"warehouse_id": w.get("warehouse_id"), "address": warehouse_address.name, "disabled": w.get("disabled")})
        else:
            warehouse_address = add_address(address_data, hub_seller)
            hub_seller.append("locations", {"warehouse_id": w.get("warehouse_id"), "address": warehouse_address.name, "disabled": w.get("disabled")})
    
    return hub_seller.save()

def update_address(address_data, address_doc, hub_seller):
    address = frappe.get_doc("Address", address_doc)
    address.update(address_data)
    if not any(l.link_doctype == "Hub Seller" and l.link_name == hub_seller for l in address.links):
        address.append("links", {"link_doctype": "Hub Seller", "link_name": hub_seller})
    return address.save(ignore_permissions=True)

def add_address(address_data, hub_seller):
    address = frappe.get_doc(address_data).insert(ignore_permissions=True)
    address.append("links", {"link_doctype": "Hub Seller", "link_name": hub_seller})
    address.save(ignore_permissions=True)
    return address

def update_seller_items(seller_items, hub_seller):
    return

class sellerServices:
    def __init__(self, data):
        self.data = frappe._dict(data)
    
    def register_seller(self):
        return register_seller(self.data)
    
    def update_catalog(self):
        return update_catalog(catalog=self.data)