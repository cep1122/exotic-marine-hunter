"""
Institutional Email Notification Service
Autonomous Exotic & Marine Hunter AI (A.E.M.H. AI)
Engineered by IC Neural Systems LLC (Israel Cepero)
Automated 6-Digit Password Reset OTP Delivery
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fallback credentials from IC Neural Systems environment
GMAIL_USER = os.getenv("GMAIL_USER", "elisra1122@gmail.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "diyugtepgyhndcaw")

def send_password_reset_email(to_email: str, recipient_name: str, code: str) -> bool:
    """
    Sends an institutional security notification with the 6-digit verification code.
    Includes both rich HTML and text fallback.
    """
    subject = f"Código de Recuperación de Acceso: {code} | Exotic & Marine Hunter AI"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #030712; color: #F3F4F6; margin: 0; padding: 24px; }}
            .card {{ max-width: 540px; margin: 0 auto; background: #0B1120; border: 1px solid #1E293B; border-radius: 16px; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
            .header {{ border-bottom: 1px solid #1E293B; padding-bottom: 20px; margin-bottom: 24px; }}
            .brand {{ font-size: 18px; font-weight: 800; color: #F59E0B; letter-spacing: -0.5px; text-transform: uppercase; }}
            .sub-brand {{ font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }}
            .greeting {{ font-size: 16px; color: #E2E8F0; margin-bottom: 16px; }}
            .text {{ font-size: 14px; color: #94A3B8; line-height: 1.6; margin-bottom: 24px; }}
            .code-box {{ background: #030712; border: 2px dashed #F59E0B; border-radius: 12px; padding: 20px; text-align: center; margin: 24px 0; }}
            .code-title {{ font-size: 11px; color: #F59E0B; text-transform: uppercase; letter-spacing: 2px; font-weight: bold; margin-bottom: 8px; }}
            .code-digits {{ font-family: 'JetBrains Mono', monospace, Consolas, Courier; font-size: 36px; font-weight: 800; color: #FFFFFF; letter-spacing: 8px; }}
            .security-notice {{ font-size: 12px; color: #64748B; border-top: 1px solid #1E293B; padding-top: 16px; margin-top: 24px; line-height: 1.5; }}
            .footer {{ margin-top: 24px; text-align: center; font-size: 11px; color: #475569; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <div class="brand">⚡ EXOTIC & MARINE HUNTER AI</div>
                <div class="sub-brand">IC Neural Systems LLC • Institutional Deal Sourcing Desk</div>
            </div>
            
            <div class="greeting">Estimado(a) <strong>{recipient_name}</strong>,</div>
            
            <div class="text">
                Hemos recibido una solicitud para restablecer la contraseña de su cuenta de inversionista. Utilice el siguiente código de verificación de un solo uso para completar la operación:
            </div>
            
            <div class="code-box">
                <div class="code-title">Código de Seguridad de 6 Dígitos</div>
                <div class="code-digits">{code}</div>
            </div>
            
            <div class="text" style="font-size: 13px;">
                ⏱️ Este código expira en <strong>15 minutos</strong>. Si usted no solicitó este cambio, por favor ignore este mensaje; su cuenta continuará protegida por el escudo de seguridad Argus Sentinel.
            </div>
            
            <div class="security-notice">
                <strong>Aviso de Seguridad:</strong> El equipo de IC Neural Systems nunca le solicitará esta clave por teléfono ni por mensajería externa. No comparta este código con terceros.
            </div>
            
            <div class="footer">
                © 2026 IC Neural Systems LLC • apibankaiempire.com • Todos los derechos reservados.
            </div>
        </div>
    </body>
    </html>
    """

    plain_text = f"""
EXOTIC & MARINE HUNTER AI - IC Neural Systems LLC
Solicitud de Restablecimiento de Contraseña

Estimado(a) {recipient_name},

Su código de verificación para restablecer su contraseña es: {code}

Este código expira en 15 minutos. Si no solicitó este cambio, ignore este mensaje.
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Exotic & Marine Hunter AI <{GMAIL_USER}>"
        msg["To"] = to_email

        msg.attach(MIMEText(plain_text, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, [to_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"[EmailService Error] Failed to send email to {to_email}: {e}")
        # Return True so users in isolated environments still receive positive acknowledgement
        return False

def send_forfeiture_alert_confirmation(to_email: str, category: str, county_or_state: str, min_spread: float) -> bool:
    """
    Sends an institutional alert subscription confirmation via Gmail SMTP.
    """
    subject = f"🔔 Alerta Activada: Radar de Incautaciones Judiciales | Exotic & Marine Hunter AI"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #030712; color: #F3F4F6; margin: 0; padding: 24px; }}
            .card {{ max-width: 540px; margin: 0 auto; background: #0B1120; border: 1px solid #1E293B; border-radius: 16px; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
            .header {{ border-bottom: 1px solid #1E293B; padding-bottom: 20px; margin-bottom: 24px; }}
            .brand {{ font-size: 18px; font-weight: 800; color: #F59E0B; letter-spacing: -0.5px; text-transform: uppercase; }}
            .sub-brand {{ font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }}
            .badge {{ display: inline-block; background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid #10B981; border-radius: 6px; padding: 4px 10px; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 16px; }}
            .greeting {{ font-size: 16px; color: #E2E8F0; margin-bottom: 16px; }}
            .text {{ font-size: 14px; color: #94A3B8; line-height: 1.6; margin-bottom: 20px; }}
            .criteria-box {{ background: #030712; border: 1px solid #334155; border-radius: 12px; padding: 16px; margin: 20px 0; }}
            .criteria-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1E293B; font-size: 13px; }}
            .criteria-row:last-child {{ border-bottom: none; }}
            .criteria-label {{ color: #94A3B8; }}
            .criteria-val {{ color: #F59E0B; font-weight: 600; }}
            .footer {{ margin-top: 24px; text-align: center; font-size: 11px; color: #475569; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <div class="brand">⚡ EXOTIC & MARINE HUNTER AI</div>
                <div class="sub-brand">IC Neural Systems LLC • Institutional Deal Sourcing Desk</div>
            </div>
            
            <div class="badge">Radar Sentinel Activo</div>
            <div class="greeting">Confirmación de Suscripción Institucional</div>
            
            <div class="text">
                Su radar de subastas federales y embargos marítimos ha sido configurado con éxito. Recibirá notificaciones en tiempo real cuando un expediente cumpla con sus parámetros:
            </div>
            
            <div class="criteria-box">
                <div class="criteria-row">
                    <span class="criteria-label">Categoría Seleccionada:</span>
                    <span class="criteria-val">{category}</span>
                </div>
                <div class="criteria-row">
                    <span class="criteria-label">Jurisdicción / Condado:</span>
                    <span class="criteria-val">{county_or_state}</span>
                </div>
                <div class="criteria-row">
                    <span class="criteria-label">Margen Spread Mínimo:</span>
                    <span class="criteria-val">+${min_spread:,.2f} USD</span>
                </div>
                <div class="criteria-row">
                    <span class="criteria-label">Protocolo de Notificación:</span>
                    <span class="criteria-val">Gmail SMTP & SMS Flash Alert</span>
                </div>
            </div>
            
            <div class="text" style="font-size: 13px; color: #64748B;">
                Usted puede actualizar o pausar estas alertas en cualquier momento desde su panel de inversionista.
            </div>
            
            <div class="footer">
                © 2026 IC Neural Systems LLC • apibankaiempire.com • Todos los derechos reservados.
            </div>
        </div>
    </body>
    </html>
    """

    plain_text = f"""
EXOTIC & MARINE HUNTER AI - Radar de Incautaciones Activo
Suscripción de Alertas Confirmada

Categoría: {category}
Jurisdicción: {county_or_state}
Margen Mínimo: ${min_spread:,.2f} USD

Recibirá alertas en cuanto un nuevo expediente judicial o embargo marítimo ingrese al radar.
IC Neural Systems LLC • apibankaiempire.com
    """

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Exotic & Marine Hunter AI <{GMAIL_USER}>"
        msg["To"] = to_email

        msg.attach(MIMEText(plain_text, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_USER, [to_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"[EmailService Error] Failed to send alert email to {to_email}: {e}")
        return False

