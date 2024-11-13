from datetime import datetime, timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Residente, GastoComun
from django.contrib import messages
from django.utils import timezone

def admin_generar_gasto(request):
    if request.method == 'POST':
        mes = request.POST['mes']
        año = request.POST['año']
        valor = request.POST['valor']
        residentes = Residente.objects.all()

        for residente in residentes:
            GastoComun.objects.create(mes=mes, año=año, valor=valor, residente=residente)

        messages.success(request, 'Gasto común generado exitosamente.')
        return redirect('admin_generar_gasto')

    return render(request, 'admin_generar_gasto.html')

def listar_gastos(request):
    # Obtener todos los residentes registrados para el menú desplegable
    residentes = Residente.objects.all()
    
    nro_departamento = request.GET.get('nro_departamento')
    gastos = []

    if nro_departamento:
        # Filtrar los gastos comunes del departamento seleccionado
        gastos = GastoComun.objects.filter(residente__nro_departamento=nro_departamento)

    return render(request, 'listar_gastos.html', {
        'residentes': residentes,
        'gastos': gastos,
        'nro_departamento': nro_departamento
    })
    
def pagar_gasto(request, gasto_id):
    # Obtener el gasto común 
    gasto = GastoComun.objects.get(id=gasto_id)

    if not gasto.estado_pago:  # Solo se puede pagar si está pendiente
        gasto.estado_pago = True  # Cambiar el estado
        gasto.save()

    return redirect('listar_gastos')  




def listar_gastos_comunes(request):
    # Obtener la fecha y hora actual
    now = timezone.now()
    mes_actual = now.month  
    año_actual = now.year  

    # Convertir el mes actual a su nombre 
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    mes_actual_espanol = meses[mes_actual - 1]  

    # Filtrar los gastos comunes que estén en estado pendiente y dentro del rango de enero a mes actual
    gastos = GastoComun.objects.filter(
        estado_pago=False,  # Solo gastos pendientes
        año__lte=año_actual,  # Año menor o igual al actual
    ).order_by('año', 'mes')  # Ordenar por año y mes

    # Incluir solo los gastos de meses hasta el mes actual
    gastos = gastos.filter(mes__in=meses[:mes_actual])  # Filtrar solo los meses hasta el mes actual 

    return render(request, 'listar_gastos_comunes.html', {'gastos': gastos})

def generar_informe_json(request):

    mes_actual = datetime.now().strftime('%B').lower()  
    mes_actual_num = datetime.now().month  
    año_actual = timezone.now().year
    # Filtra los gastos comunes pendientes
    gastos = GastoComun.objects.filter(estado_pago=False)

    # Excluye los gastos comunes que están en meses posteriores al mes actua
    meses_del_año = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    
    # Excluir gastos cuyo mes esté después del mes actual
    gastos = gastos.filter(
        mes__in=meses_del_año[:mes_actual_num],  # Solo incluir meses anteriores o el actual
        año__lte=año_actual,
    )

    # Crea el informe con los gastos pendientes filtrados
    informe = []
    for gasto in gastos:
        informe.append({
            'mes': gasto.mes,
            'año': gasto.año,
            'valor': str(gasto.valor),  
            'estado_pago': 'Pagado' if gasto.estado_pago else 'Pendiente',
            'nro_departamento': gasto.residente.nro_departamento
        })

    return JsonResponse(informe, safe=False)