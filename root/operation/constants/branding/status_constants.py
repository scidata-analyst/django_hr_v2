"""
Branding Status Constants
"""

# Asset Status
ACTIVE = "ACTIVE"
INACTIVE = "INACTIVE"
DEPRECATED = "DEPRECATED"
IN_REVIEW = "IN_REVIEW"

ASSET_STATUS_CHOICES = [
    (ACTIVE, "Active"),
    (INACTIVE, "Inactive"),
    (DEPRECATED, "Deprecated"),
    (IN_REVIEW, "In Review"),
]

# Asset Type
LOGO = "LOGO"
BANNER = "BANNER"
ICON = "ICON"
COLOR_SCHEME = "COLOR_SCHEME"
FONT = "FONT"

ASSET_TYPE_CHOICES = [
    (LOGO, "Logo"),
    (BANNER, "Banner"),
    (ICON, "Icon"),
    (COLOR_SCHEME, "Color Scheme"),
    (FONT, "Font"),
]
