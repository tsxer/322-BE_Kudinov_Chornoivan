from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

def base_template(content: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width">
    </head>
    <body style="margin:0;padding:0;background:#f5f5f7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 20px;">
        <tr>
          <td align="center">
            <table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
              <tr>
                <td style="background:#1a56db;padding:32px 40px;">
                  <table cellpadding="0" cellspacing="0">
                    <tr>
                      <td style="color:#ffffff;font-size:22px;font-weight:700;letter-spacing:2px;">NTI</td>
                      <td style="padding-left:10px;color:#93c5fd;font-size:11px;padding-top:6px;letter-spacing:1px;">NITRIANSKY TECHNOLOGICKÝ INKUBÁTOR</td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td style="padding:40px;">
                  {content}
                </td>
              </tr>
              <tr>
                <td style="background:#f5f5f7;padding:24px 40px;border-top:1px solid #e5e7eb;">
                  <p style="margin:0;font-size:12px;color:#9ca3af;text-align:center;">
                    © 2026 Nitriansky technologický inkubátor<br>
                    Trieda Andreja Hlinku 603/1, 949 74 Nitra-Chrenová
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

STATUS_LABELS = {
    "draft": "Koncept",
    "submitted": "Odoslané",
    "formal_check": "Formálna kontrola",
    "in_review": "V hodnotení",
    "needs_info": "Vyžaduje doplnenie",
    "approved": "Schválené",
    "rejected": "Zamietnuté",
    "active": "Aktívne",
    "archived": "Archivované"
}

STATUS_COLORS = {
    "approved": "#10b981",
    "rejected": "#ef4444",
    "needs_info": "#f59e0b",
    "submitted": "#3b82f6",
    "formal_check": "#6366f1",
    "in_review": "#8b5cf6",
    "active": "#10b981",
    "archived": "#6b7280",
    "draft": "#9ca3af"
}

async def send_email(to: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to],
        body=body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_registration_email(email: str):
    content = f"""
        <h1 style="margin:0 0 8px;font-size:28px;font-weight:700;color:#111827;">Vitajte v NTI!</h1>
        <p style="margin:0 0 24px;font-size:16px;color:#6b7280;line-height:1.6;">Váš účet bol úspešne vytvorený. Teraz môžete podávať prihlášky do programov NTI inkubátora.</p>
        
        <table cellpadding="0" cellspacing="0" style="background:#f0f9ff;border-radius:12px;padding:24px;margin-bottom:24px;width:100%;">
          <tr>
            <td>
              <p style="margin:0 0 8px;font-size:13px;font-weight:600;color:#1a56db;text-transform:uppercase;letter-spacing:0.5px;">Čo ďalej?</p>
              <p style="margin:0 0 8px;font-size:14px;color:#374151;">✓ Doplňte váš profil</p>
              <p style="margin:0 0 8px;font-size:14px;color:#374151;">✓ Prehliadnite dostupné programy</p>
              <p style="margin:0;font-size:14px;color:#374151;">✓ Podajte prihlášku</p>
            </td>
          </tr>
        </table>
        
        <a href="http://localhost:5173/dashboard" style="display:inline-block;background:#1a56db;color:#ffffff;text-decoration:none;padding:14px 32px;border-radius:50px;font-size:14px;font-weight:600;">Prejsť do portálu →</a>
    """
    await send_email(
        to=email,
        subject="Vitajte v NTI systéme",
        body=base_template(content)
    )

async def send_application_status_email(email: str, status: str, app_id: int):
    label = STATUS_LABELS.get(status, status)
    color = STATUS_COLORS.get(status, "#6b7280")
    
    content = f"""
        <h1 style="margin:0 0 8px;font-size:28px;font-weight:700;color:#111827;">Stav prihlášky sa zmenil</h1>
        <p style="margin:0 0 24px;font-size:16px;color:#6b7280;line-height:1.6;">Vaša prihláška č. <strong>#{app_id}</strong> má nový stav.</p>
        
        <table cellpadding="0" cellspacing="0" style="background:#f9fafb;border-radius:12px;padding:24px;margin-bottom:24px;width:100%;border-left:4px solid {color};">
          <tr>
            <td>
              <p style="margin:0 0 4px;font-size:13px;color:#9ca3af;text-transform:uppercase;letter-spacing:0.5px;">Nový stav prihlášky</p>
              <p style="margin:0;font-size:20px;font-weight:700;color:{color};">{label}</p>
            </td>
          </tr>
        </table>
        
        <a href="http://localhost:5173/applications" style="display:inline-block;background:#1a56db;color:#ffffff;text-decoration:none;padding:14px 32px;border-radius:50px;font-size:14px;font-weight:600;">Zobraziť prihlášku →</a>
    """
    await send_email(
        to=email,
        subject=f"Zmena stavu prihlášky #{app_id}",
        body=base_template(content)
    )