from pydantic import BaseModel


class URLBase(BaseModel):
    """Base schema for URL-related operations.
    Attributes:
        target_url (str): The original URL that is to be shortened or processed.
    """
    
    target_url: str


class URL(URLBase):
    """Represents a URL entity with additional metadata. Extends URLBase.
    Attributes:
        target_url (str): The original URL that is to be shortened or processed.
        is_active (bool): Indicates whether the URL is currently active.
        clicks (int): The number of times the shortened URL has been accessed.
    """
    
    is_active: bool
    clicks: int

    class Config:
        """
        Pydantic configuration class to enable ORM mode, allowing models to be created from ORM objects.
        """
        from_attributes = True


# You could also add the two strings url and admin_url to URL. But by adding url and admin_url to the URLInfo subclass, you can use the data in your API without storing it in your database.
class URLInfo(URL):
    """URL information schema for API responses. Extends URL.

    Attributes:
        target_url (str): The original URL that is to be shortened or processed.
        is_active (bool): Indicates whether the URL is currently active.
        clicks (int): The number of times the shortened URL has been accessed.
        url (str): The shortened URL.
        admin_url (str): The admin URL for managing the shortened URL.
    """
    url: str
    admin_url: str
