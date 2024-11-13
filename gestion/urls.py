from django.urls import path
from . import views

urlpatterns = [
    path('generar_gasto/', views.admin_generar_gasto, name='admin_generar_gasto'),
    path('', views.listar_gastos, name='listar_gastos'),
    path('pagar_gasto/<int:gasto_id>/', views.pagar_gasto, name='pagar_gasto'),
    path('listar_gastos_com/', views.listar_gastos_comunes, name='listar_gastos_comunes'),
    path('generar_informe_json/', views.generar_informe_json, name='generar_informe_json')
]