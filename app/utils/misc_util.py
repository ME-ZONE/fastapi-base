## External Function ##
def create_bullet_list(items: list[str]) -> str:
    bullet_list = "\n".join([f"• {item}" for item in items])
    return bullet_list
