"""Amazon integration interface and fake adapter."""

from keiji.integrations.amazon.adapter import AmazonListingAdapter
from keiji.integrations.amazon.fake_adapter import FakeAmazonListingAdapter
from keiji.integrations.amazon.models import AmazonListingSnapshot

__all__ = ["AmazonListingAdapter", "AmazonListingSnapshot", "FakeAmazonListingAdapter"]
