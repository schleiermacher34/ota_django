from django.http import JsonResponse, HttpResponse
from .models import Firmware, Machine, MachineLog
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
import hashlib
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import MachineLogSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import SupportTicketForm
from django.contrib.auth.models import User
from .vtiger_client import VtigerClient
from django.views.decorators.csrf import csrf_exempt
import json




@csrf_exempt
def create_asset(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            serial_number = data.get('serial_number')
            if serial_number:
                # Process the serial number
                # For example, create or update an asset in your database
                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'error': 'Serial number not provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['POST'])
def sync_vtiger(request):
    vtiger = VtigerClient(
        url="https://vtiger.anatol.com/",
        access_key="68jhKPOiltQdklnL",
        username="admin-andrii",

    )

    # Fetch assets from Vtiger
    assets = vtiger.get_assets()

    for asset in assets:
        serial_number = asset.get('serial_number')
        product_name = asset.get('product_name')
        asset_name = asset.get('assetname')
        customer_name = asset.get('customer_name')

        # Find or create a user
        user, created = User.objects.get_or_create(username=customer_name)

        # Find or create a machine entry
        Machine.objects.update_or_create(
            serial_number=serial_number,
            defaults={
                'user': user,
                'product_name': product_name,
                'asset_name': asset_name,
                'customer_name': customer_name,
            }
        )

    return JsonResponse({'status': 'success', 'message': 'Synchronized Vtiger assets successfully.'})


def check_update(request):
    current_version = request.GET.get('version', '')
    try:
        latest_firmware = Firmware.objects.latest('uploaded_at')
    except Firmware.DoesNotExist:
        return JsonResponse({'update_available': False})

    if latest_firmware.version != current_version:
        return JsonResponse({
            'update_available': True,
            'version': latest_firmware.version,
            'url': request.build_absolute_uri(latest_firmware.file.url),
        })
    else:
        return JsonResponse({'update_available': False})
    if latest_firmware.version != current_version:
        # Calculate SHA256 checksum
        sha256_hash = hashlib.sha256()
        for chunk in latest_firmware.file.chunks():
            sha256_hash.update(chunk)
        checksum = sha256_hash.hexdigest()

        return JsonResponse({
            'update_available': True,
            'version': latest_firmware.version,
            'url': request.build_absolute_uri(latest_firmware.file.url),
            'checksum': checksum,
        })
    else:
        return JsonResponse({'update_available': False})

@login_required
def create_ticket(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id, user=request.user)
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.machine = machine
            ticket.save()
            return redirect('ticket_list')
    else:
        form = SupportTicketForm()
    return render(request, 'firmware/create_ticket.html', {'form': form, 'machine': machine})

@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.filter(user=request.user)
    return render(request, 'firmware/ticket_list.html', {'tickets': tickets})

@login_required
def machine_list(request):
    machines = Machine.objects.filter(user=request.user)
    return render(request, 'firmware/machine_list.html', {'machines': machines})

@login_required
def machine_detail(request, pk):
    machine = get_object_or_404(Machine, pk=pk, user=request.user)
    logs = MachineLog.objects.filter(machine=machine)
    return render(request, 'firmware/machine_detail.html', {'machine': machine, 'logs': logs})

@api_view(['POST'])
def validate_license(request):
    serial_number = request.data.get('serial_number')
    license_key = request.data.get('license_key')

    if not serial_number or not license_key:
        return Response({'status': 'error', 'message': 'Serial number and license key are required.'}, status=400)

    try:
        machine = Machine.objects.get(serial_number=serial_number, license_key=license_key)
        if not machine.activation_date:
            machine.activation_date = timezone.now()
            machine.save()
        return Response({'status': 'success', 'message': 'License validated.'})
    except Machine.DoesNotExist:
        return Response({'status': 'error', 'message': 'Invalid license.'}, status=400)

@api_view(['POST'])
def upload_log(request):
    serializer = MachineLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'message': 'Log uploaded.'})
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def get_token(request):
    serial_number = request.data.get('serial_number')
    license_key = request.data.get('license_key')

    try:
        machine = Machine.objects.get(serial_number=serial_number, license_key=license_key)
        user = machine.user
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 'success',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    except Machine.DoesNotExist:
        return Response({'status': 'error', 'message': 'Invalid credentials.'}, status=400)

