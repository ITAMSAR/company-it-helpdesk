from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import Equipment
import socket
import qrcode
from io import BytesIO

def item_detail_view(request, code):
    """Public view for QR code scanning - shows item details by code"""
    try:
        equipment = Equipment.objects.get(inventory_code=code)
        return render(request, 'inventory/item_detail.html', {
            'equipment': equipment,
            'scanned_at': datetime.now()
        })
    except Equipment.DoesNotExist:
        return render(request, 'inventory/item_not_found.html', {'code': code})

def test_mobile_access(request):
    """Simple test page for mobile access dengan IP detection"""
    local_ip = get_local_ip()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Mobile Access</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial; padding: 20px; text-align: center; background: #f0f8ff; }
            .success { color: green; font-size: 24px; margin-bottom: 20px; }
            .info { margin: 20px 0; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .ip-info { background: #e8f5e8; padding: 10px; border-radius: 5px; margin: 10px 0; }
            .btn { background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1 class="success">✅ SERVER BERHASIL DIAKSES!</h1>
        <div class="info">
            <div class="ip-info">
                <strong>🌐 IP Server Terdeteksi: """ + local_ip + """:8000</strong>
            </div>
            <p><strong>📱 Waktu Akses:</strong> """ + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + """</p>
            <p><strong>🔍 User Agent:</strong><br><small>""" + request.META.get('HTTP_USER_AGENT', 'Unknown') + """</small></p>
            <p><strong>📍 IP Client:</strong> """ + request.META.get('REMOTE_ADDR', 'Unknown') + """</p>
        </div>
        
        <div>
            <a href="/inventory/" class="btn">📦 Ke Halaman Inventory</a>
            <a href="/inventory/test-mobile/" class="btn">🔄 Refresh Test</a>
        </div>
        
        <div class="info">
            <h3>🔧 Cara Test QR Code:</h3>
            <ol style="text-align: left; max-width: 400px; margin: 0 auto;">
                <li>Buka inventory di komputer</li>
                <li>Klik tombol QR hijau</li>
                <li>Download QR code PNG</li>
                <li>Scan dengan HP (pastikan 1 jaringan)</li>
                <li>Browser HP akan buka halaman detail barang</li>
            </ol>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def get_local_ip():
    """Auto-detect IP lokal komputer"""
    try:
        # Method 1: Connect to external server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        try:
            # Method 2: Fallback using hostname
            return socket.gethostbyname(socket.gethostname())
        except:
            # Method 3: Last fallback
            return "192.168.1.1"

def generate_qr_code(request, equipment_id):
    """Generate QR code dengan IP lokal otomatis"""
    try:
        equipment = Equipment.objects.get(id=equipment_id)
        
        # Auto-detect IP lokal
        local_ip = get_local_ip()
        
        # Create URL dengan IP lokal dinamis
        item_url = f"http://{local_ip}:8000/item/{equipment.inventory_code}/"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=12,
            border=4,
        )
        
        qr.add_data(item_url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to buffer
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Return as download
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        response['Content-Disposition'] = f'attachment; filename="QR-{equipment.inventory_code}-{local_ip}.png"'
        
        return response
        
    except Equipment.DoesNotExist:
        return HttpResponse('Equipment not found', status=404)
    except Exception as e:
        return HttpResponse(f'Error generating QR: {str(e)}', status=500)