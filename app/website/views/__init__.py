from .home_page_views import(
    IndexView,
    AboutPageView,
    PrivacyPolicyView,
    TermsAndConditionsView,
    ContactPageView,
    SubmitContactFormView,
    SignUpPageView,
    RegisterView,
    LoginPageView,
    UserLoginView,
    logout_view,
    ForgotPasswordPageView,
    SendChangePasswordLinkView,
    ResetPasswordPageView,
    ChangePasswordView,
    EmailverificationView,
    EmailVerificationPage,
    SendEmailVerificationLinkView,
)
from .product_page_views import ShopPageView, ServicePageView, ServiceDetailPageView, PurchaseProductView, ServiceBookingView, ServiceCategoryPageView
from .personal_detail_page import ProfilePageView, EditProfileFormView, TransactionFilterAjaxView
from .free_charts_page_views import FreeChartPageView, PhoneNumberChartView, PersonalChartTabPage, PersonalChartView
from .cart_pages import(
    AddServiceToCartView,
    BookingPage,
    CartPage,
    RemoveServiceFromCart,
    AddProductToCartView,
    RemoveProductFromCart,
    PaymentSuccessPage,
)
