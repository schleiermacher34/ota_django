from django.http import JsonResponse, HttpResponse
from .models import Firmware
import hashlib

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




