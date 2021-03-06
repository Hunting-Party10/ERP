'''
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from . import views

from . import views

urlpatterns = [
   
    path('all/', views.final_product_list, name='product_list'),
    url(r'^get_components/(?P<final_product_id>\d+)/$', views.final_product_components_by_id),
    url(r'^get_component_info/(?P<component_id>\d+)/$', views.components_list_id),
    path('create_product/', views.create_product),
    url(r'^create_component/(?P<final_product_id>\d+)/$', views.create_component),
]

'''

from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from . import views
from . import views

urlpatterns = [

    path('all/', views.final_product_list, name='product_list'),

    path('Item_Master/', views.Item_Master, name='Item_Master'),

    path('Final_Product_List/', views.Final_Product_List_Item_Master,
         name='Final_Product_List_Item_Master'),

    path('Components_List/', views.Components_List_Item_Master,
         name='Components_List_Item_Master'),

    path('Create_Component/', views.Create_Component,
         name='Create_Component'),



    path('Inventory_List_Item_Master/', views.Inventory_List_Item_Master,
         name='Inventory_List_Item_Master'),

    path('rm/', views.Inventary, name='Inventary'),

    path('Create_Raw_Material/', views.Create_Raw_Material,
         name='Create_Raw_Material'),
    url(r'^Assign_Raw_Material/(?P<component_id>\d+)/$', views.Assign_Raw_Material),

    url(r'^Update_Raw_Material/(?P<component_id>\d+)/$',
        views.update_quantity_raw_material),

    path('ayushi/', views.ayushi, name='ayushi'),

    url(r'^get_components/(?P<final_product_id>\d+)/$',
        views.final_product_components_by_id),

    url(r'^get_component_info/(?P<component_id>\d+)/$',
        views.get_components_details),

    url(r'^get_component_info_of_selected_assembly/(?P<final_product_id>\d+)/$',
        views.get_component_info_of_selected_assembly),

    url(r'^create_component/(?P<final_product_id>\d+)/$', views.create_component),

    url(r'^delete_component/(?P<component_id>\d+)/(?P<final_product_id>\d+)/$',
        views.delete_component, name='delete_component'),

    url(r'^create_product/', views.create_product),

    url(r'^delete_Final_Product/(?P<final_product_id>\d+)/$',
        views.delete_Final_Product, name='delete_Final_Product'),










    #path('create_process/', views.get_process_details_paticular_component),

    url(r'^Add_Process_to_Component/(?P<component_id>\d+)/$',
        views.Add_Process_to_Component),
    url(r'^get_porcess_info/(?P<component_id>\d+)/$', views.create_process),

    url(r'^change_process_status/(?P<component_id>\d+)/$',
        views.change_process_status),

    # -------------------------------------

    url(r'^PO_Status/(?P<customer_id>\d+)/$', views.PO_Status),

    url(r'^create_customer/', views.create_customer),

    url(r'^customer_list/', views.customer_list),

    url(r'^create_purchase_order/(?P<customer_id>\d+)/$',
        views.create_purchase_order),

    url(r'^Select_Assembly_to_Po/(?P<po_id>\d+)/$',
        views.Select_Assembly_to_Po),


    url(r'^show_selected_final_product_components_list/(?P<po_id>\d+)/$',
        views.show_selected_final_product_components_list),

    url(r'^Select_Components_For_PO/(?P<po_id>\d+)/(?P<final_product_id>\d+)/$',
        views.Select_Components_For_PO),

    url(r'^Assembly_Status/$',
        views.Assembly_Status),

    url(r'^Approved_PO_List/$',
        views.Approved_PO_List),


]
