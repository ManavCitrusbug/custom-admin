from .auth import SignUpApiView, LoginAPIView, LogoutAPIView, UserProfileAPI, ForgotPasswordAPIView, SetPasswordAPIView
from .testimonials import TestimonialsListingAPIView
from .inquiry import InquiryAPIView, InquirycategoryListing
from .products import ProductsListingAPIView, PurchaseProductAPIView
from .services import ServiceCategoryListingAPIView, ServiceListingAPIView, ServiceDetailAPI, ServiceTimeSlotsAPIView, ServiceBookingAPIView, PackageListingAPIView
from .plot_chart import PhoneNumberChartAPIView, PersonalDetailChartAPIView
from .cart import ProductCartAPIView, ServiceCartAPIView, ShoppingCartAPIView
from .transactions import TransactionListingAPIView, TransactionDetailAPIView