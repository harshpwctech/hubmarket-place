import frappe

def get_categories():
    response = []
    categories = frappe.get_all("Hub Item Category", filters={"is_group": 1})
    for c in categories:
        if frappe.db.exists("Hub Seller Item", {"category": c.name}):
            category = frappe.get_cached_doc("Hub Item Category", c.name).as_dict()
            category.sub_category = []
            sub_categories = frappe.get_all("Hub Item Category", filters={"parent_hub_item_category": c.name})
            for s in sub_categories:
                if frappe.db.exists("Hub Seller Item", {"sub_category": s.name}):
                    category.sub_category.append(frappe.get_cached_doc("Hub Item Category", s.name))
            response.append(category)
    return response

def get_seller_categories():
    response = []
    categories = frappe.get_all("Hub Item Category", filters={"is_group": 1})
    for c in categories:
        category = frappe.get_cached_doc("Hub Item Category", c.name).as_dict()
        category.sub_category = []
        sub_categories = frappe.get_all("Hub Item Category", filters={"parent_hub_item_category": c.name})
        for s in sub_categories:
            category.sub_category.append(frappe.get_cached_doc("Hub Item Category", s.name))
        response.append(category)
    return response

def get_top_items_sellers(category):
    response = {
        "sellers": [],
        "products": []
    }
    seller_filters = [
        ["Hub Item Category Detail","category","=",category],
        ["Hub Seller", "logo", "is", "set"]
    ]
    seller_fields = ["name", "seller_name", "brand", "logo"]
    sellers = frappe.get_all("Hub Seller", fields= seller_fields, filters=seller_filters, limit_page_length=15)
    if len(sellers):
        sellers_for_item_filters = [s.name for s in sellers]
        item_filters = [
            ["Hub Seller Item","category","=",category],
            ["Hub Seller Item","hub_seller","in",sellers_for_item_filters],
            ["Hub Seller Item","image","is","set"],
        ]
        item_fields = ["name", "hub_seller", "seller_name", "item_name", "offered_price", "rating", "image"]
        items = frappe.get_all("Hub Seller Item", filters=item_filters, limit_page_length=8, fields=item_fields)
        if len(items):
            response["sellers"] = sellers
            response["products"] = items
    
    return response

def get_items(**kwargs):
    item_filters = [
        ["Hub Seller Item","image","is","set"]
        ]
    item_fields = ["name", "hub_seller", "seller_name", "item_name", "offered_price", "rating", "image"]
    filters = kwargs.get("filters", {})
    if filters:
        for k,v in filters.items():
            if isinstance(v, str):
                item_filters.append(["Hub Seller Item",k,"like", f"%{v}%"])
            elif isinstance(v, list):
                item_filters.append(["Hub Seller Item",k,"in",v])
    else:
        return frappe.throw("Filters are mandatory")
    items = frappe.get_all("Hub Seller Item", filters=item_filters, fields=item_fields)
    return items

def get_related_items(**kwargs):
    item_filters = [
        ["Hub Seller Item","image","is","set"]
        ]
    item_fields = ["name", "hub_seller", "seller_name", "item_name", "offered_price", "rating", "image"]
    item_name = kwargs.get("item_name")
    related_items = frappe.get_all("Hub Recommended Item", filters={"parenttype": "Hub Seller Item", "parent": item_name}, fields=["item"])
    item_filters.append(["Hub Seller Item","name","in",[i.item for i in related_items]])
    items = frappe.get_all("Hub Seller Item", filters=item_filters, fields=item_fields)
    return items

def get_reviews(item_name):
    # Fetch review counts grouped by rating
    review_data = frappe.db.sql(
        """
        SELECT
            rating,
            COUNT(*) AS count
        FROM
            `tabHub Item Review`
        WHERE
            hub_item = %s
        GROUP BY
            rating
        ORDER BY
            rating DESC
        """,
        (item_name,),
        as_dict=True,
    )

    # Initialize counts for all ratings (1 to 5)
    counts_dict = {rating: 0 for rating in range(1, 6)}
    for d in review_data:
        counts_dict[int(d["rating"])] = d["count"]

    # Format counts into a list
    counts = [{"rating": rating, "count": counts_dict[rating]} for rating in range(5, 0, -1)]

    # Calculate the overall average rating
    average_rating = (
        frappe.db.sql(
            """
            SELECT AVG(rating)
            FROM `tabHub Item Review`
            WHERE hub_item = %s
            """,
            (item_name,),
        )[0][0] or 0
    )

    # Fetch featured reviews
    featured_reviews = frappe.get_all(
        "Hub Item Review",
        filters={"hub_item": item_name},
        fields=["rating", "review AS content", "full_name AS author"],
        order_by="creation DESC",
        limit_page_length=5
    )

    # Calculate the total count of reviews
    total_count = sum(counts_dict.values())

    # Format featured reviews
    featured = [
        {
            "rating": review["rating"],
            "content": review["content"],
            "author": review["author"]
        }
        for review in featured_reviews
    ]

    reviews = {
        "average": round(average_rating, 2),
        "totalCount": total_count,
        "counts": counts,
        "featured": featured,
    }
    
    return reviews

def oauth_providers():
	from frappe.utils.html_utils import get_icon_html
	from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys
	from frappe.utils.password import get_decrypted_password

	out = []
	providers = frappe.get_all(
		"Social Login Key",
		filters={"enable_social_login": 1},
		fields=["name", "client_id", "base_url", "provider_name", "icon"],
		order_by="name",
	)

	for provider in providers:
		client_secret = get_decrypted_password(
			"Social Login Key", provider.name, "client_secret"
		)
		if not client_secret:
			continue

		icon = None
		if provider.icon:
			if provider.provider_name == "Custom":
				icon = get_icon_html(provider.icon, small=True)
			else:
				icon = f"<img src='{provider.icon}' alt={provider.provider_name}>"

		if provider.client_id and provider.base_url and get_oauth_keys(provider.name):
			out.append(
				{
					"name": provider.name,
					"provider_name": provider.provider_name,
					"auth_url": get_oauth2_authorize_url(provider.name, "/"),
					"icon": icon,
				}
			)

	return out

class masterServices:
    def __init__(self, data):
        self.data = frappe._dict(data)
    
    def get_categories(self):
        return get_categories()
    
    def get_seller_categories(self):
        return get_seller_categories()
    
    def get_top_items_sellers(self):
        category = self.data.category
        return get_top_items_sellers(category)
    
    def get_items(self):
        kwargs = self.data
        return get_items(**kwargs)
    
    def get_related_items(self):
        kwargs = self.data    
        return get_related_items(**kwargs)
    
    def get_seller(self):
        hub_seller = self.data.hub_seller
        return frappe.get_cached_doc("Hub Seller", hub_seller)
    
    def get_item(self):
        name = self.data.name
        return frappe.get_cached_doc("Hub Seller Item", name)
    
    def get_category(self):
        name = self.data.category
        return frappe.get_cached_doc("Hub Item Category", name)

    def get_reviews(self):
        item_name = self.data.item_name
        return get_reviews(item_name)
    
    def oauth_providers(self):
         return oauth_providers()
    