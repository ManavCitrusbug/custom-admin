from .testimonials import (
    TestimonialAjaxPagination,
    TestimonialCreateView,
    TestimonialDeleteView,
    TestimonialListView,
    TestimonialUpdateView,
)

from .users import (
    IndexView,
    UserDetailView,
    UserAjaxPagination,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserPasswordView,
    UserUpdateView,
    export_user_csv,
)

from .service_categories import(
    ServiceCategoryListView,
    ServiceCategoryAjaxPagination,
    ServiceCategoryCreateView,
    ServicecategoryUpdateView,
    ServiceCategoryDeleteView,
    ServiceCategoryDetailView,
)
from .inquiry_type import(
    InquiryTypeAjaxPagination, InquiryTypeCreateView, InquiryTypeDeleteView, InquiryTypeUpdateView, InquiryTypeListView,
)
from .inquiry import InquiryAjaxPagination, InquiryCreateView, InquiryDeleteView, InquiryDetailView, InquiryListView, InquiryUpdateView
from .phone_code import PhoneNumberCodeAjaxPagination, PhoneNumberCodeCreateView, PhoneNumberCodeDeleteView, PhoneNumberCodeUpdateView, PhoneNumberCodeListView
from .foundation_code import(
    FoundationCodeCreateView,
    FoundationCodeUpdateView,
    FoundationCodeListView,
    FoundationCodeDeleteView,
    FoundationCodeAjaxPagination,
)
from .family_code import(
    FamilyCodeCreateView,
    FamilyCodeUpdateView,
    FamilyCodeListView,
    FamilyCodeDeleteView,
    FamilyCodeAjaxPagination,
)
from .social_code import(
    SocialCodeCreateView,
    SocialCodeUpdateView,
    SocialCodeListView,
    SocialCodeDeleteView,
    SocialCodeAjaxPagination,
)
from .other_code import(
    OtherCodeCreateView,
    OtherCodeUpdateView,
    OtherCodeListView,
    OtherCodeDeleteView,
    OtherCodeAjaxPagination,
)
from .number_code import(
    NumberCodeCreateView,
    NumberCodeUpdateView,
    NumberCodeListView,
    NumberCodeDeleteView,
    NumberCodeAjaxPagination,
)
from .product import(
    ShopProductCreateView,
    ShopProductUpdateView,
    ShopProductListView,
    ShopProductDeleteView,
    ShopProductAjaxPagination,
    ShopProductDetailView,
)
from .service import(
    ServiceCreateView,
    ServiceUpdateView,
    ServiceListView,
    ServiceDeleteView,
    ServiceAjaxPagination,
    ServiceDetailView,
)
from .purchased_product import(
    PurchasedProductCreateView,
    PurchasedProductUpdateView,
    PurchasedProductListView,
    PurchasedProductDeleteView,
    PurchasedProductAjaxPagination,
)
from .service_booking import(
    BookedServiceCreateView,
    BookedServiceUpdateView,
    BookedServiceListView,
    BookedServiceDeleteView,
    BookedServiceAjaxPagination,
)

from .time_slots import(
    TimeSlotAjaxPagination,
    TimeSlotCreateView,
    TimeSlotDeleteView,
    TimeSlotUpdateView,
    TimeSlotListView,
)

from .category_image import(
    CategoryImageListView,
    CategoryImageCreateView,
    CategoryImageUpdateView,
    CategoryImageDeleteView,
    CategoryImageAjaxPagination,
)