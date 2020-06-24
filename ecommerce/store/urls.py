from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	#path('productView/<int:id>/',views.productView, name='productView'),
    path('slider/<int:id>', views.slider, name="slider"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),
	path('logout/', views.logoutUser, name="logout"),
    path('update_theme/', views.updateTheme, name="update_theme"),
    path('user_settings/', views.userSettings, name="user_settings"),
    path('about/',views.aboutus, name='aboutus'),
    path('contactus/',views.contactus, name='contactus'),


    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"),
        name="reset_password"),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"),
        name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"),
        name="password_reset_complete"),

]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''