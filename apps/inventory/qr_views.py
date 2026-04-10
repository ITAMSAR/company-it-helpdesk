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
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Mobile Access</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                padding: 20px; 
                text-align: center; 
                background: linear-gradient(135deg, #f0f8ff, #e6f3ff); 
                min-height: 100vh;
                margin: 0;
            }}
            .container {{
                max-width: 500px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                animation: slideIn 0.8s ease-out;
            }}
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateY(30px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            .success {{ 
                color: #059669; 
                font-size: 2rem; 
                margin-bottom: 20px; 
                font-weight: bold;
            }}
            .info {{ 
                margin: 20px 0; 
                background: #f8fafc;
                padding: 20px;
                border-radius: 12px;
                border-left: 4px solid #0ea5e9;
            }}
            .ip-info {{ 
                background: linear-gradient(135deg, #dcfce7, #bbf7d0); 
                padding: 15px; 
                border-radius: 10px; 
                margin: 15px 0; 
                border: 2px solid #86efac;
            }}
            .btn {{ 
                background: linear-gradient(135deg, #0ea5e9, #0284c7); 
                color: white; 
                padding: 15px 25px; 
                text-decoration: none; 
                border-radius: 10px; 
                display: inline-block; 
                margin: 10px; 
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            .btn:hover {{ 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(14, 165, 233, 0.3);
                color: white;
                text-decoration: none;
            }}
            .instructions {{
                background: #fef3c7;
                border: 2px solid #fcd34d;
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                text-align: left;
            }}
            .instructions h3 {{
                color: #92400e;
                margin-bottom: 15px;
                text-align: center;
            }}
            .instructions ol {{
                color: #92400e;
                line-height: 1.6;
            }}
            .instructions li {{
                margin-bottom: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="success">✅ SERVER BERHASIL DIAKSES!</h1>
            <div class="info">
                <div class="ip-info">
                    <strong>🌐 IP Server: {local_ip}:8000</strong>
                </div>
                <p><strong>📱 Waktu Akses:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                <p><strong>🔍 User Agent:</strong><br><small>{request.META.get('HTTP_USER_AGENT', 'Unknown')}</small></p>
                <p><strong>📍 IP Client:</strong> {request.META.get('REMOTE_ADDR', 'Unknown')}</p>
            </div>
            
            <div>
                <a href="/inventory/" class="btn">📦 Ke Halaman Inventory</a>
                <a href="/inventory/test-mobile/" class="btn">🔄 Refresh Test</a>
            </div>
            
            <div class="instructions">
                <h3>🔧 Cara Test QR Code:</h3>
                <ol>
                    <li>Buka inventory di komputer</li>
                    <li>Klik tombol QR hijau pada barang</li>
                    <li>Download QR code PNG</li>
                    <li>Scan dengan HP (pastikan WiFi sama)</li>
                    <li>Browser HP akan buka halaman detail barang</li>
                </ol>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 0.9rem;">
                <strong>🎯 QR Code System Ready!</strong><br>
                Server berjalan dengan benar dan siap untuk QR scanning
            </div>
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