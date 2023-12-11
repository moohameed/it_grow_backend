from home.views import login,signup,test_token,user_list,user_detail,verify_email,send_reset_email,reset_password
from WoocemerceData.views import woocommerce_orders , woo_list , woo_create , woo_user,woo_delete,woocommerce_orders_unique
from prestashopData.views import presta_create , presta_list , prestashop_orders 
from django.urls import path
from facebookIntegration.views import facebook_login , get_insights
from googleAnalytics.views import  google_auth , google_auth_callback,google_analytics_properties , google_analytics_data


app_name = 'api'  # This is the app name


urlpatterns = [
    #Les URLs de user auth
    path ('user/login' , login),
    path ('user/register' , signup),
    path ('verify_email/<str:token>/', verify_email, name='verify_email'),
    path ('send_reset_email',send_reset_email),
    path ('reset_password/<str:tokenn>',reset_password),
    path ('token' , test_token),
    path ('getUser' , user_list),
    path ('userDetail/<int:pk>' , user_detail),
    #Les URLs de woocomerce
    path ('getOrders' , woocommerce_orders),
    path ('getWoo' , woo_list),
    path ('createWoo' , woo_create),
    path ('getWooUser' , woo_user),
    path ('woo_delete/<int:pk>' , woo_delete),
    path ('woocommerce_orders_unique/<int:pk>' , woocommerce_orders_unique),
    #Les URLs de prestashop
    path ('createPresta' , presta_create),
    path ('getPresta' , presta_list),
    path ('getPrestaOrders' , prestashop_orders),
    #Les URLs de FACEBOOK
    path('facebook-login/',  facebook_login ,name='facebook_login'),
    path('get_insights/',  get_insights ,name='get_insights'),
    #Les URLs de google analytics
    path('google-auth/', google_auth, name='google-auth'),
    path('google-auth-callback/', google_auth_callback, name='google-auth-callback'),
    path('google-analytics-properties/', google_analytics_properties, name='google_analytics_properties'),
    path('google-analytics-data/', google_analytics_data, name='google_analytics_data'),
    
]