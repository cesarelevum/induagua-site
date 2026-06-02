# -*- coding: utf-8 -*-
"""Genera 6 landing pages SEO-optimizadas por aplicación industrial."""
import re

# 1. Lee el template (plantas-tratamiento.html) y extrae styles + nav + footer
with open('plantas-tratamiento.html', 'r', encoding='utf-8') as f:
    template = f.read()

style_match = re.search(r'<style>(.*?)</style>', template, re.DOTALL)
STYLES = style_match.group(0)

# Extrae navbar (entre <body> y antes de la primera <section> del hero original)
nav_match = re.search(r'(<!-- NAVBAR -->.*?</nav>)', template, re.DOTALL)
if not nav_match:
    nav_match = re.search(r'(<nav.*?</nav>)', template, re.DOTALL)
NAVBAR = nav_match.group(0) if nav_match else ''

# Extrae footer
footer_match = re.search(r'(<footer.*?</footer>)', template, re.DOTALL)
FOOTER = footer_match.group(0) if footer_match else ''

# Extrae scripts finales
scripts_match = re.search(r'(<script[^>]*>.*?</script>\s*</body>)', template, re.DOTALL)
SCRIPTS_END = '<script>document.querySelectorAll(".reveal").forEach(e=>e.classList.add("visible"));</script></body>'

# WhatsApp flotante
WHATSAPP_FLOAT = '''<a href="https://wa.me/528112993935" class="whatsapp-float" target="_blank" rel="noopener" aria-label="WhatsApp INDUAGUA" style="position:fixed;bottom:24px;right:24px;width:60px;height:60px;background:#25D366;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,0,0,0.2);z-index:999;animation:pulse-ring 2s infinite;"><svg viewBox="0 0 24 24" width="32" height="32" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg></a>'''


def build_page(slug, title, h1, meta_desc, keywords, hero_image, hero_intro, sections, faqs, wa_msg):
    """Construye el HTML completo de una landing page."""
    schema_faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    }
    import json
    faq_json = json.dumps(schema_faq, ensure_ascii=False, indent=2)

    schema_service = f'''{{
      "@context": "https://schema.org",
      "@type": "Service",
      "name": "{title}",
      "description": "{meta_desc}",
      "provider": {{
        "@type": "LocalBusiness",
        "name": "INDUAGUA",
        "url": "https://www.induagua.com",
        "telephone": "+528112993935",
        "address": {{ "@type": "PostalAddress", "streetAddress": "Av. Central 230-Int.132, Los Lermas", "addressLocality": "Guadalupe", "addressRegion": "Nuevo León", "postalCode": "67190", "addressCountry": "MX" }}
      }},
      "areaServed": [
        {{ "@type": "City", "name": "Monterrey" }},
        {{ "@type": "City", "name": "Apodaca" }},
        {{ "@type": "City", "name": "Santa Catarina" }},
        {{ "@type": "City", "name": "García" }},
        {{ "@type": "City", "name": "General Escobedo" }},
        {{ "@type": "City", "name": "Guadalupe" }},
        {{ "@type": "State", "name": "Nuevo León" }}
      ]
    }}'''

    schema_breadcrumb = f'''{{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://www.induagua.com" }},
        {{ "@type": "ListItem", "position": 2, "name": "Aplicaciones", "item": "https://www.induagua.com/#productos" }},
        {{ "@type": "ListItem", "position": 3, "name": "{h1[:60]}", "item": "https://www.induagua.com/{slug}.html" }}
      ]
    }}'''

    sections_html = '\n'.join([f'''
        <section style="padding:64px 0;{s.get("bg","background:var(--white);")}">
            <div class="container" style="max-width:900px;">
                <h2 style="font-size:1.875rem;font-weight:800;color:var(--navy);margin-bottom:20px;letter-spacing:-0.02em;line-height:1.2;">{s["title"]}</h2>
                {s["content"]}
            </div>
        </section>''' for s in sections])

    faqs_html = '\n'.join([f'''
                <div style="background:var(--white);border:1px solid var(--gray-200);border-radius:12px;padding:24px 28px;margin-bottom:16px;">
                    <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:12px;">{q}</h3>
                    <p style="color:var(--gray-600);font-size:.95rem;line-height:1.7;">{a}</p>
                </div>''' for q, a in faqs])

    canonical = f"https://www.induagua.com/{slug}.html"

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="INDUAGUA">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="es-MX" href="{canonical}">

    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:image" content="https://www.induagua.com/images/{hero_image}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="es_MX">
    <meta property="og:site_name" content="INDUAGUA">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{meta_desc}">
    <meta name="twitter:image" content="https://www.induagua.com/images/{hero_image}">

    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

    <script type="application/ld+json">{schema_service}</script>
    <script type="application/ld+json">{schema_breadcrumb}</script>
    <script type="application/ld+json">{faq_json}</script>

    {STYLES}
</head>
<body>
{NAVBAR}

<section style="padding-top:120px;padding-bottom:80px;background:linear-gradient(180deg,var(--navy) 0%,var(--blue-900,#1e3a5f) 100%);position:relative;overflow:hidden;">
    <div class="container">
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:48px;align-items:center;">
            <div>
                <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(37,99,235,0.15);border:1px solid rgba(37,99,235,0.3);color:var(--blue-500,#3b82f6);font-size:.75rem;font-weight:700;padding:8px 16px;border-radius:100px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:24px;">Aplicación Industrial · Nuevo León</div>
                <h1 style="font-size:clamp(1.875rem,4vw,2.875rem);font-weight:800;color:white;line-height:1.1;letter-spacing:-0.03em;margin-bottom:20px;">{h1}</h1>
                <p style="font-size:1.0625rem;color:rgba(255,255,255,0.72);line-height:1.7;margin-bottom:32px;max-width:560px;">{hero_intro}</p>
                <div style="display:flex;flex-wrap:wrap;gap:14px;">
                    <a href="https://wa.me/528112993935?text={wa_msg}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:10px;background:var(--blue-600);color:white;font-weight:600;padding:14px 28px;border-radius:8px;font-size:.95rem;">Cotizar suministro &rarr;</a>
                    <a href="/#productos" style="display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,0.08);color:white;font-weight:600;padding:14px 28px;border-radius:8px;border:1px solid rgba(255,255,255,0.18);font-size:.95rem;">Ver otras aplicaciones</a>
                </div>
            </div>
            <div>
                <img src="/images/{hero_image}" alt="{h1}" style="width:100%;height:380px;object-fit:cover;border-radius:16px;box-shadow:0 25px 50px -12px rgba(0,0,0,0.4);">
            </div>
        </div>
    </div>
</section>

{sections_html}

<section style="padding:80px 0;background:var(--gray-50);">
    <div class="container" style="max-width:900px;">
        <div style="text-align:center;margin-bottom:48px;">
            <div style="display:inline-flex;align-items:center;gap:8px;font-size:.75rem;font-weight:700;color:var(--blue-600);text-transform:uppercase;letter-spacing:.12em;margin-bottom:14px;">Preguntas Frecuentes</div>
            <h2 style="font-size:1.875rem;font-weight:800;color:var(--navy);letter-spacing:-0.02em;">Lo que más nos preguntan</h2>
        </div>
        {faqs_html}
    </div>
</section>

<section style="padding:72px 0;background:var(--gradient-dark);text-align:center;">
    <div class="container" style="max-width:720px;">
        <h2 style="font-size:1.875rem;font-weight:800;color:white;margin-bottom:16px;letter-spacing:-0.02em;">¿Confirmamos disponibilidad para tu planta?</h2>
        <p style="color:rgba(255,255,255,0.65);font-size:1rem;line-height:1.7;margin-bottom:32px;">Cuéntanos cuánta agua consumes al mes y para qué proceso. Te confirmamos disponibilidad, especificación y precio en menos de 1 hora hábil.</p>
        <a href="https://wa.me/528112993935?text={wa_msg}" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:10px;background:#25D366;color:white;font-weight:700;padding:16px 36px;border-radius:8px;font-size:1rem;box-shadow:0 8px 24px rgba(37,211,102,0.3);">Hablar por WhatsApp &rarr;</a>
    </div>
</section>

{FOOTER}
{WHATSAPP_FLOAT}
{SCRIPTS_END}
</html>
'''


# =========================================================================
# CONTENIDO POR APLICACIÓN
# =========================================================================

PAGES = [
    {
        'slug': 'agua-para-calderas-industriales',
        'title': 'Agua Desmineralizada para Calderas Industriales | INDUAGUA Monterrey',
        'h1': 'Agua Desmineralizada para Calderas Industriales en Nuevo León',
        'meta': 'Agua desmineralizada para alimentación de calderas industriales en Monterrey y Nuevo León. Previene incrustaciones, reduce consumo de combustible y extiende la vida útil del equipo. Análisis certificado por lote.',
        'keywords': 'agua para calderas, agua desmineralizada para calderas, tratamiento agua calderas industriales Monterrey, agua alimentación caldera Nuevo León, proveedor agua calderas Apodaca',
        'hero_image': 'caldera.jpg',
        'hero_intro': 'Suministro de agua desmineralizada para calderas de vapor industriales en Monterrey, Apodaca, Santa Catarina, García y toda el área metropolitana. Reduce hasta 10 % tu consumo de gas natural eliminando el sarro en los tubos de transferencia de calor.',
        'wa_msg': 'Hola%2C%20me%20interesa%20cotizar%20agua%20desmineralizada%20para%20mi%20caldera%20industrial',
        'sections': [
            {
                'title': 'El costo oculto del agua mal especificada en tu caldera',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Cada milímetro de incrustación de calcio y magnesio en los tubos de tu caldera reduce hasta un <strong>10 % la transferencia de calor</strong>. Eso significa que estás quemando un 10 % más de gas natural cada mes para producir la misma cantidad de vapor — y en una caldera de 100 HP funcionando 16 horas al día, eso son miles de pesos mensuales de combustible literalmente convertidos en sarro.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">El problema no termina ahí. El agua dura también acelera la corrosión interna por carbónico libre, debilita la presión nominal de operación y, en casos críticos, puede ocasionar rupturas catastróficas en tubos de fuego o de agua. El costo de un paro no programado por daño en caldera supera fácilmente lo que cuesta surtir agua tratada correctamente durante años.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;">En INDUAGUA suministramos agua desmineralizada con especificación controlada para alimentación de calderas en toda el área metropolitana de Monterrey. Análisis certificado por lote, conductividad y dureza verificadas antes de salir de planta.</p>'''
            },
            {
                'title': 'Especificación recomendada según presión de operación',
                'bg': 'background:var(--gray-50);',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:24px;">La especificación de agua de alimentación depende de la presión de tu caldera. Esta es la guía técnica que aplicamos según ABMA/ASME para calderas industriales:</p>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;margin-bottom:16px;">
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <div style="font-size:.7rem;font-weight:700;color:var(--blue-600);text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;">Baja presión</div>
                        <div style="font-size:1.25rem;font-weight:800;color:var(--navy);margin-bottom:8px;">&lt; 300 psi</div>
                        <p style="color:var(--gray-600);font-size:.875rem;line-height:1.6;">Dureza &lt; 1 ppm como CaCO₃ · Conductividad &lt; 5,000 µS/cm · Sílice &lt; 150 ppm</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <div style="font-size:.7rem;font-weight:700;color:var(--blue-600);text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;">Media presión</div>
                        <div style="font-size:1.25rem;font-weight:800;color:var(--navy);margin-bottom:8px;">300-600 psi</div>
                        <p style="color:var(--gray-600);font-size:.875rem;line-height:1.6;">Dureza &lt; 0.3 ppm · Conductividad &lt; 1,500 µS/cm · Sílice &lt; 40 ppm</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <div style="font-size:.7rem;font-weight:700;color:var(--blue-600);text-transform:uppercase;letter-spacing:.1em;margin-bottom:10px;">Alta presión</div>
                        <div style="font-size:1.25rem;font-weight:800;color:var(--navy);margin-bottom:8px;">&gt; 600 psi</div>
                        <p style="color:var(--gray-600);font-size:.875rem;line-height:1.6;">Dureza &lt; 0.05 ppm · Conductividad &lt; 300 µS/cm · Sílice &lt; 10 ppm</p>
                    </div>
                </div>'''
            },
            {
                'title': 'Cómo te entregamos el suministro',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Olvídate de operar tu propia planta de tratamiento. INDUAGUA produce el agua, la certifica por lote y la entrega en tu planta con frecuencia recurrente programada según tu consumo:</p>
                <ul style="list-style:none;padding:0;color:var(--gray-700);font-size:1.0625rem;line-height:1.9;">
                    <li style="padding-left:28px;position:relative;margin-bottom:10px;"><span style="position:absolute;left:0;color:var(--blue-600);font-weight:800;">✓</span><strong>Entrega en tote IBC de 1,000 L</strong> a granel directo en tu planta</li>
                    <li style="padding-left:28px;position:relative;margin-bottom:10px;"><span style="position:absolute;left:0;color:var(--blue-600);font-weight:800;">✓</span><strong>Análisis certificado por lote</strong>: conductividad, dureza, pH, sílice</li>
                    <li style="padding-left:28px;position:relative;margin-bottom:10px;"><span style="position:absolute;left:0;color:var(--blue-600);font-weight:800;">✓</span><strong>Frecuencia programada</strong> según consumo (semanal, quincenal o mensual)</li>
                    <li style="padding-left:28px;position:relative;margin-bottom:10px;"><span style="position:absolute;left:0;color:var(--blue-600);font-weight:800;">✓</span><strong>Cero inversión</strong> en planta de tratamiento propia, operador ni consumibles</li>
                    <li style="padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:var(--blue-600);font-weight:800;">✓</span><strong>Cobertura</strong>: Monterrey, Apodaca, Santa Catarina, García, Escobedo, Guadalupe, San Nicolás, Pesquería</li>
                </ul>'''
            }
        ],
        'faqs': [
            ('¿Qué tipo de agua se usa para alimentar una caldera industrial?', 'La mayoría de calderas industriales de baja y media presión usan agua desmineralizada con dureza menor a 1 ppm como CaCO₃. Esto previene incrustaciones en los tubos de transferencia de calor, reduce la corrosión interna y mantiene la eficiencia térmica nominal. Para calderas de alta presión (>600 psi), la especificación es más estricta y se requiere agua con conductividad menor a 300 µS/cm.'),
            ('¿Cuánto combustible ahorro usando agua tratada correctamente?', 'Cada milímetro de incrustación de calcio reduce hasta un 10 % la transferencia de calor en los tubos. Una caldera con sarro acumulado puede estar consumiendo entre 8 % y 25 % más combustible que una caldera limpia. En operación industrial típica de 16 horas al día, este sobreconsumo representa decenas de miles de pesos mensuales en gas natural.'),
            ('¿Tengo que comprar una planta de tratamiento propia o pueden surtirme el agua?', 'No es necesario invertir en planta propia. INDUAGUA suministra agua desmineralizada con la especificación exacta para tu caldera, en frecuencia recurrente programada. Te ahorras la inversión inicial, el operador dedicado, los consumibles y el mantenimiento — y obtienes la misma especificación certificada en cada entrega.'),
            ('¿Con qué frecuencia entregan?', 'Según tu consumo. Para clientes con consumo continuo entregamos semanal o quincenal con calendario fijo. Para consumo variable, entregamos bajo demanda con confirmación en menos de 24 horas. Cobertura completa en el área metropolitana de Monterrey, Apodaca, Santa Catarina, García y municipios cercanos.'),
            ('¿Cómo confirmo que el agua cumple la especificación de mi caldera?', 'Cada lote entregado incluye un certificado de análisis con conductividad, dureza, pH y sílice medidos en nuestro laboratorio antes de salir de planta. Esto te permite documentar el cumplimiento ante auditorías ISO 9001, IATF 16949 o normativa interna de tu empresa.'),
        ]
    },
    {
        'slug': 'agua-para-torres-de-enfriamiento',
        'title': 'Agua Desmineralizada para Torres de Enfriamiento Industriales | INDUAGUA NL',
        'h1': 'Agua Desmineralizada para Torres de Enfriamiento Industriales',
        'meta': 'Agua de reposición para torres de enfriamiento industriales en Monterrey y Nuevo León. Controla incrustación en el relleno, corrosión del circuito y reduce purgas. Suministro recurrente con análisis certificado.',
        'keywords': 'agua para torres de enfriamiento, agua reposición torre enfriamiento Monterrey, agua desmineralizada torres industriales, tratamiento agua torres NL, proveedor agua make-up torre',
        'hero_image': 'app-torres.jpg',
        'hero_intro': 'Suministro de agua desmineralizada de reposición (make-up) para torres de enfriamiento industriales en Nuevo León. Controla la incrustación en el relleno, reduce las purgas necesarias y mantiene estable la eficiencia del intercambio térmico.',
        'wa_msg': 'Hola%2C%20me%20interesa%20cotizar%20agua%20desmineralizada%20para%20mi%20torre%20de%20enfriamiento',
        'sections': [
            {
                'title': 'Por qué tu torre evapora dinero todos los días',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Una torre de enfriamiento industrial evapora entre el <strong>1 % y 2 % del flujo recirculante por cada 5.5 °C de salto térmico</strong>. Cuando el agua que repones tiene minerales disueltos, esos minerales NO se evaporan — se concentran en el circuito. Cuanto más reciclas, más concentras, hasta que el sarro se deposita en el relleno, los intercambiadores y el condensador.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Para evitar esto, tu sistema necesita hacer <strong>purgas</strong> — tirar agua concentrada y reponer con agua fresca. Si repones con agua dura, vas a tener que purgar mucho más, lo que significa tirar también todo el químico de tratamiento que pagaste. Los ciclos de concentración bajos elevan tu factura de agua, química y tiempo perdido.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;">Con agua desmineralizada de reposición, tus ciclos de concentración pueden ir de los típicos 3-4 hasta 6-8 sin problemas — reduciendo a la mitad el consumo de agua y químicos.</p>'''
            },
            {
                'title': 'Lo que protege agua de reposición correctamente especificada',
                'bg': 'background:var(--gray-50);',
                'content': '''<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;">
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Relleno del torre</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">El sarro de calcio reduce el área de intercambio aire-agua. Cada milímetro depositado reduce la eficiencia de enfriamiento entre 5 % y 15 %.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Intercambiadores</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">El depósito mineral aísla térmicamente los tubos, obligando al sistema a trabajar a más presión y temperatura para lograr el mismo enfriamiento.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Condensadores</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">En sistemas de refrigeración industrial, las incrustaciones en el condensador suben la presión de descarga del compresor — más kWh por tonelada de refrigeración.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Purgas y química</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Menor concentración mineral inicial = ciclos más largos = menos purgas = menos químico desperdiciado.</p>
                    </div>
                </div>'''
            },
            {
                'title': 'Suministro a medida para tu volumen',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">El consumo de agua de reposición en torres industriales varía mucho según tonelaje y horas de operación. Un sistema de 200 toneladas puede consumir entre 30,000 y 50,000 litros mensuales solo en make-up. Adaptamos el plan de suministro a tu volumen real:</p>
                <ul style="list-style:none;padding:0;color:var(--gray-700);font-size:1.0625rem;line-height:1.9;">
                    <li style="padding-left:28px;position:relative;margin-bottom:10px;"><span style="position:absolute;left:0;color:var(--blue-600);font-weight:800;">→</span>Entregas programadas en tote IBC de 1,000 L</li>
                    <li style="padding-left:28px;position:relative;margin-bottom:10px;"><span style="position:absolute;left:0;color:var(--blue-600);font-weight:800;">→</span>Calendario fijo de reposición según tonelaje y horas de operación</li>
                    <li style="padding-left:28px;position:relative;margin-bottom:10px;"><span style="position:absolute;left:0;color:var(--blue-600);font-weight:800;">→</span>Análisis certificado por lote</li>
                    <li style="padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:var(--blue-600);font-weight:800;">→</span>Cobertura completa en NL: Monterrey, Apodaca, Santa Catarina, García, Escobedo, Guadalupe</li>
                </ul>'''
            }
        ],
        'faqs': [
            ('¿Qué agua se debe usar para reponer una torre de enfriamiento?', 'Se recomienda agua de reposición desmineralizada o suavizada con bajo contenido de calcio, magnesio y sílice. Esto reduce la velocidad de incrustación, permite ciclos de concentración más altos y disminuye las purgas necesarias. Para sistemas de refrigeración crítica o de alta eficiencia, se recomienda agua desmineralizada con conductividad menor a 100 µS/cm.'),
            ('¿Cuánta agua de reposición consume una torre típica?', 'Una torre de enfriamiento industrial consume aproximadamente entre 1 % y 2 % del flujo recirculante por evaporación por cada 5.5 °C de salto térmico. A esto se suma el agua perdida por arrastre (0.05–0.2 %) y la purga necesaria para controlar ciclos de concentración. Un sistema de 200 toneladas puede requerir entre 30,000 y 50,000 litros mensuales de make-up.'),
            ('¿Puedo subir mis ciclos de concentración con agua tratada?', 'Sí. Con agua desmineralizada de reposición, los ciclos de concentración pueden ir de los típicos 3-4 a entre 6 y 8, lo que reduce a la mitad el consumo de agua y químicos en el sistema. El ahorro acumulado paga el agua tratada en pocos meses.'),
            ('¿Entregan en mi parque industrial?', 'Sí. Cubrimos toda el área metropolitana de Monterrey incluyendo Apodaca, Santa Catarina, García, General Escobedo, Guadalupe, San Nicolás y Pesquería con entrega programada en tote IBC.'),
            ('¿El agua viene con certificado de análisis?', 'Sí. Cada entrega incluye certificado con conductividad, dureza, pH y sílice — documentación que puedes presentar en auditorías de calidad y procesos.'),
        ]
    },
    {
        'slug': 'agua-para-inyeccion-de-plastico',
        'title': 'Agua Desmineralizada para Chillers de Inyección de Plástico | INDUAGUA NL',
        'h1': 'Agua Desmineralizada para Chillers e Inyección de Plástico',
        'meta': 'Agua desmineralizada para chillers y líneas de enfriamiento de moldes en inyección de plástico en Monterrey y Apodaca. Evita el sarro que reduce la transferencia de calor y eleva el cycle time, sin la corrosión del agua ultrapura.',
        'keywords': 'agua para chiller inyección plástico, agua para moldes inyección, agua desmineralizada inyectoras plástico Monterrey, agua para cooling line plástico, proveedor agua plásticos Apodaca',
        'hero_image': 'app-inyeccion.jpg',
        'hero_intro': 'Suministro de agua desmineralizada para chillers y líneas de enfriamiento de moldes en plantas de inyección de plástico en Apodaca, Santa Catarina, García y todo Nuevo León. La especificación correcta evita el sarro sin la corrosión del agua ultrapura.',
        'wa_msg': 'Hola%2C%20me%20interesa%20cotizar%20agua%20desmineralizada%20para%20chiller%20de%20inyeccion',
        'sections': [
            {
                'title': 'El punto dulce que la mayoría de inyectoras no usan',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">La mayoría de las plantas de inyección de plástico cometen uno de dos errores con el agua de enfriamiento:</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:12px;"><strong>Error 1 — Agua de la red:</strong> El calcio y magnesio se depositan como sarro en los canales del molde y en los tubos del chiller. Una capa de 1 mm de sarro reduce hasta 30 % la transferencia de calor — lo que eleva el cycle time, genera defectos de contracción y dispara los rechazos de calidad.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:12px;"><strong>Error 2 — Agua desionizada pura:</strong> El agua ultrapura es agresiva — busca equilibrarse disolviendo iones. En un cooling loop con conectores de cobre, latón o bronce, esto significa disolución del metal, agua azulada por cobre disuelto, perforación de mangueras y daños en intercambiadores en cuestión de meses.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;"><strong>La solución correcta:</strong> agua desmineralizada con TDS bajo (10–50 ppm) pero con iones residuales suficientes para no atacar los metales del circuito. Cycle time estable, sin corrosión, sin sarro.</p>'''
            },
            {
                'title': 'Especificación recomendada para chillers de inyección',
                'bg': 'background:var(--gray-50);',
                'content': '''<div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:32px;max-width:560px;margin:0 auto;">
                    <h3 style="font-size:1.125rem;font-weight:700;color:var(--navy);margin-bottom:20px;">Agua desmineralizada para chiller — INDUAGUA</h3>
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px 24px;color:var(--gray-700);font-size:.9375rem;line-height:1.5;">
                        <div><strong>Conductividad:</strong></div><div>15–50 µS/cm</div>
                        <div><strong>TDS:</strong></div><div>10–50 ppm</div>
                        <div><strong>Dureza total:</strong></div><div>&lt; 5 ppm como CaCO₃</div>
                        <div><strong>Cloruros:</strong></div><div>&lt; 50 ppm</div>
                        <div><strong>Hierro:</strong></div><div>&lt; 0.3 ppm</div>
                        <div><strong>pH:</strong></div><div>7.0 – 8.0</div>
                    </div>
                </div>
                <p style="color:var(--gray-600);font-size:.95rem;line-height:1.7;margin-top:24px;text-align:center;">Esta especificación protege metales de cooling line, evita sarro en moldes y mantiene cycle time consistente.</p>'''
            },
            {
                'title': 'Para fabricantes de autopartes plásticas y envases',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Atendemos plantas de inyección en los corredores industriales de Nuevo León: Apodaca, Santa Catarina, García, Pesquería y Salinas Victoria. Producción de:</p>
                <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;color:var(--gray-700);font-size:.95rem;">
                    <div style="background:var(--gray-50);border-radius:8px;padding:16px;">Autopartes plásticas con/sin refuerzo</div>
                    <div style="background:var(--gray-50);border-radius:8px;padding:16px;">Envases industriales y de consumo</div>
                    <div style="background:var(--gray-50);border-radius:8px;padding:16px;">Componentes eléctricos y electrónicos</div>
                    <div style="background:var(--gray-50);border-radius:8px;padding:16px;">Mobiliario y artículos del hogar</div>
                    <div style="background:var(--gray-50);border-radius:8px;padding:16px;">Tapas, cierres y accesorios</div>
                    <div style="background:var(--gray-50);border-radius:8px;padding:16px;">Productos OEM Tier 1 / Tier 2</div>
                </div>'''
            }
        ],
        'faqs': [
            ('¿Qué tipo de agua se debe usar en un chiller de inyección de plástico?', 'Lo recomendado es agua desmineralizada con TDS bajo (10–50 ppm) y conductividad entre 15 y 50 µS/cm. El agua dura genera sarro que reduce hasta 30 % la transferencia de calor y eleva el cycle time. El agua desionizada ultrapura, en cambio, es agresiva y disuelve el cobre y latón del circuito de enfriamiento. El punto óptimo es desmineralizada — bajo TDS pero con iones residuales que no atacan los metales.'),
            ('¿Cuánto puede aumentar mi cycle time si tengo sarro en el molde?', 'Una capa de 1 mm de sarro en los canales del molde reduce hasta 30 % la transferencia de calor. Esto se traduce típicamente en cycle time 8–15 % más largo, lo que en una línea de producción de 24 horas representa miles de piezas menos por semana y mayor consumo energético por pieza.'),
            ('¿Es mejor agua de red, desmineralizada o desionizada para inyección de plástico?', 'Desmineralizada es la mejor opción para chillers de inyección de plástico. Agua de red causa sarro y reduce transferencia de calor. Agua desionizada ultrapura disuelve cobre y latón del circuito. La desmineralizada da el balance correcto: TDS bajo para no formar sarro y suficientes iones para no ser agresiva con los metales.'),
            ('¿Puedo usar la misma agua del chiller para otros procesos?', 'Sí. La misma agua desmineralizada que usamos en chiller de inyección sirve para procesos de enjuague, preparación de mezclas y otros usos industriales con TDS bajo controlado.'),
            ('¿En cuánto tiempo entregan en Apodaca, Santa Catarina o García?', 'Para clientes con contrato de suministro recurrente, calendarizamos entregas semanales o quincenales. Para pedidos puntuales, confirmamos disponibilidad en el mismo día y entregamos en menos de 24 horas hábiles en toda el área metropolitana.'),
        ]
    },
    {
        'slug': 'agua-para-anticongelante-y-urea',
        'title': 'Agua Desmineralizada para Fabricantes de Anticongelante y Urea Automotriz | INDUAGUA',
        'h1': 'Agua Desmineralizada y Desionizada para Anticongelante, Urea y Refrigerantes',
        'meta': 'Suministro de agua desmineralizada y desionizada como ingrediente base para fabricantes de anticongelante, urea automotriz, refrigerantes y químicos de formulación en Monterrey y Nuevo León. Análisis certificado por lote.',
        'keywords': 'agua para anticongelante, agua desmineralizada anticongelante Monterrey, agua para urea automotriz, agua DEF, agua AdBlue Nuevo León, agua refrigerante fabricación',
        'hero_image': 'app-detergentes.jpg',
        'hero_intro': 'Tu fórmula es tu marca. El agua es la nuestra. Suministramos agua desmineralizada y desionizada como ingrediente base para fabricantes de anticongelante, urea automotriz y refrigerantes en Nuevo León. Misma especificación en cada lote — porque tu cliente no perdona un producto inconsistente.',
        'wa_msg': 'Hola%2C%20me%20interesa%20cotizar%20agua%20para%20fabricar%20anticongelante%20o%20urea',
        'sections': [
            {
                'title': 'Cuando el agua ES tu producto',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">El anticongelante para motor diésel típico contiene <strong>entre 50 % y 70 % agua</strong>. La urea automotriz grado AUS 32 contiene <strong>67.5 % agua</strong>. El refrigerante automotriz puede ser <strong>50 % agua o más</strong>. En estos productos, el agua no es un insumo — es <strong>el ingrediente principal de tu fórmula</strong>.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Eso significa que la especificación de tu agua de entrada define la especificación de tu producto final. Si tu lote llega con conductividad fuera de rango, el producto terminado también lo está. Si llega con minerales fuera de spec, tu producto puede fallar las pruebas de cliente o auditoría. Si la entrega es inconsistente entre lotes, tu producción es inconsistente.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;">INDUAGUA entrega agua desmineralizada y desionizada con la misma especificación lote tras lote, con análisis certificado, para que tu fórmula sea consistente y tu cliente no tenga sorpresas.</p>'''
            },
            {
                'title': 'Especificación crítica según norma de cada producto',
                'bg': 'background:var(--gray-50);',
                'content': '''<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;">
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:8px;">Urea automotriz</h3>
                        <p style="color:var(--blue-600);font-weight:600;font-size:.875rem;margin-bottom:12px;">Norma ISO 22241 / AUS 32</p>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Conductividad &lt; 5 µS/cm · Sin metales pesados · Sin aldehídos · Trazabilidad por lote requerida por OEM.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:8px;">Anticongelantes (OAT/HOAT/IAT)</h3>
                        <p style="color:var(--blue-600);font-weight:600;font-size:.875rem;margin-bottom:12px;">ASTM D3306, D4985, D6210</p>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Conductividad &lt; 10 µS/cm · Cloruros &lt; 25 ppm · Sulfatos &lt; 25 ppm · Sílice controlado según formulación.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:8px;">Refrigerantes industriales</h3>
                        <p style="color:var(--blue-600);font-weight:600;font-size:.875rem;margin-bottom:12px;">Especificación por OEM</p>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Agua desmineralizada con TDS controlado y sin iones que comprometan la formulación inhibidora.</p>
                    </div>
                </div>'''
            },
            {
                'title': 'Por qué los fabricantes serios escogen suministro recurrente',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Si tu producción mensual es 50,000 L o 200,000 L de fórmula final, tu consumo de agua puede ser entre 30,000 L y 150,000 L mensuales. Operar tu propia planta de tratamiento para ese volumen implica:</p>
                <ul style="list-style:none;padding:0;color:var(--gray-700);font-size:1.0625rem;line-height:1.9;margin-bottom:24px;">
                    <li style="padding-left:28px;position:relative;margin-bottom:8px;"><span style="position:absolute;left:0;color:var(--gray-400);">•</span>CAPEX de equipo (RO + resinas + tanques)</li>
                    <li style="padding-left:28px;position:relative;margin-bottom:8px;"><span style="position:absolute;left:0;color:var(--gray-400);">•</span>Operador dedicado con capacitación</li>
                    <li style="padding-left:28px;position:relative;margin-bottom:8px;"><span style="position:absolute;left:0;color:var(--gray-400);">•</span>Consumibles, refacciones y mantenimiento</li>
                    <li style="padding-left:28px;position:relative;"><span style="position:absolute;left:0;color:var(--gray-400);">•</span>Si el equipo falla, se para tu producción</li>
                </ul>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;">Con suministro recurrente INDUAGUA, recibes el agua con la especificación exacta de tu producto, sin invertir, sin operar y con análisis por lote para auditorías. Si fabricas urea automotriz, anticongelante o refrigerantes en Monterrey, Apodaca, García, Salinas Victoria o Santa Catarina, podemos confirmar disponibilidad para tu volumen mensual.</p>'''
            }
        ],
        'faqs': [
            ('¿Qué agua se usa para fabricar anticongelante?', 'El anticongelante para motor diésel contiene entre 50 % y 70 % agua, por lo que la especificación del agua de entrada define la especificación del producto final. Las normas ASTM D3306, D4985 y D6210 piden agua desmineralizada con conductividad menor a 10 µS/cm, cloruros menores a 25 ppm y sulfatos menores a 25 ppm para fórmulas OAT, HOAT e IAT.'),
            ('¿Qué especificación de agua pide la norma de urea automotriz (AUS 32)?', 'La norma ISO 22241 para urea automotriz grado AUS 32 (DEF / AdBlue / SCR) exige agua desionizada con conductividad menor a 5 µS/cm, sin metales pesados (Cu, Zn, Ni, Cr, Pb), sin aldehídos y con trazabilidad por lote. INDUAGUA produce agua desionizada para esta aplicación con análisis certificado por lote.'),
            ('¿Pueden entregar volúmenes industriales de 50,000 a 200,000 L al mes?', 'Sí. Manejamos suministro recurrente programado para fabricantes con consumo industrial. Entregamos en tote IBC de 1,000 L con calendario fijo (semanal o quincenal) y cobertura completa en Nuevo León: Monterrey, Apodaca, Santa Catarina, García, Pesquería, Salinas Victoria.'),
            ('¿El agua viene con certificado para auditorías ISO/IATF?', 'Sí. Cada entrega incluye certificado de análisis con conductividad, dureza, TDS, pH y los parámetros adicionales que requiera tu norma de producto. Esto te permite presentar trazabilidad ante auditorías ISO 9001, IATF 16949 y cualquier auditoría de cliente OEM.'),
            ('¿Cuál es la diferencia entre desmineralizada y desionizada para mi formulación?', 'Desmineralizada (single-pass RO) tiene TDS de 10–50 ppm y conductividad de 15–50 µS/cm. Desionizada (RO + resinas) tiene TDS menor a 1 ppm y conductividad menor a 1 µS/cm. Para anticongelante y refrigerantes la desmineralizada generalmente es suficiente. Para urea AUS 32 se requiere desionizada por norma.'),
        ]
    },
    {
        'slug': 'agua-para-metalmecanica-y-acabados',
        'title': 'Agua para Metalmecánica, Acabados y Tratamiento Térmico | INDUAGUA NL',
        'h1': 'Agua Desmineralizada y Desionizada para Metalmecánica y Acabados Industriales',
        'meta': 'Agua desmineralizada y desionizada para enjuagues en cromado, niquelado, anodizado, pretratamiento de pintura y procesos de templado en talleres metalmecánicos de Nuevo León. Evita manchas, defectos de acabado y fallas de adherencia.',
        'keywords': 'agua para cromado, agua para anodizado Monterrey, agua para pretratamiento pintura industrial, agua desionizada metalmecanica NL, agua para templado, agua acabados metalicos Apodaca',
        'hero_image': 'app-metalmecanica.jpg',
        'hero_intro': 'Suministro de agua desmineralizada y desionizada para procesos críticos en metalmecánica: enjuagues finales en cromado, niquelado y anodizado, pretratamiento de pintura industrial, y aplicaciones de templado y enfriamiento controlado. Cobertura en toda el área metropolitana de Monterrey.',
        'wa_msg': 'Hola%2C%20me%20interesa%20cotizar%20agua%20para%20metalmecanica%20y%20acabados',
        'sections': [
            {
                'title': 'Cómo el agua define la calidad de tu acabado',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">En metalmecánica, el agua no entra al producto final — pero <strong>define si tu acabado pasa o no pasa control de calidad</strong>. Tres ejemplos:</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:12px;"><strong>En cromado y niquelado:</strong> El enjuague final tras el baño electrolítico es donde se decide la presencia de manchas y water spots. Si el agua de enjuague tiene minerales, se quedan en la pieza al secar — manchas blancas visibles, lote rechazado.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:12px;"><strong>En anodizado de aluminio:</strong> Las etapas de enjuague entre baños (decapado, oxidación anódica, sellado) requieren agua desionizada para no contaminar el siguiente baño con iones del anterior. Sin DI, los baños se contaminan rápido y la calidad del óxido cae.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;"><strong>En pretratamiento de pintura:</strong> El enjuague final tras el fosfatado requiere agua desmineralizada para evitar defectos de adherencia y "cráteres" en la película de pintura. Las líneas automotrices de mayor calidad exigen agua con conductividad menor a 20 µS/cm en el enjuague final.</p>'''
            },
            {
                'title': 'Aplicaciones en talleres y plantas metalmecánicas',
                'bg': 'background:var(--gray-50);',
                'content': '''<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;">
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Galvanoplastia</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Enjuague final en cromado, niquelado, zincado y cobreado. Evita water spots, manchas blancas y rechazos visuales.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Anodizado de aluminio</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Etapas de enjuague entre baños (decapado, ánodo, sellado). DI obligatoria para no contaminar baños sucesivos.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Pretratamiento de pintura</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Enjuague final post-fosfatado en líneas automotrices y electrodomésticos. Conductividad &lt; 20 µS/cm.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Templado y tratamiento térmico</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Agua desmineralizada para baños de enfriamiento controlado en tratamientos térmicos especializados de aceros y aleaciones.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Lavado de piezas críticas</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Enjuague final de piezas mecanizadas para industria automotriz, aeroespacial y dispositivos médicos donde no se aceptan residuos.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Electroerosión (Wire EDM)</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Agua desionizada como medio dieléctrico en talleres de matricería y troquelado de precisión.</p>
                    </div>
                </div>'''
            },
            {
                'title': 'Mercado fuerte en Nuevo León',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Nuevo León concentra una de las industrias metalmecánicas más grandes de México: talleres de cromado y niquelado para autopartes, líneas de pintura automotriz Tier 1 y Tier 2, anodizado de aluminio para componentes arquitectónicos y partes automotrices, talleres de fundición y forja. Surtimos a procesos en:</p>
                <div style="display:flex;flex-wrap:wrap;gap:8px;">
                    <span style="background:var(--blue-50);color:var(--blue-700);padding:6px 14px;border-radius:100px;font-size:.875rem;font-weight:600;">Apodaca</span>
                    <span style="background:var(--blue-50);color:var(--blue-700);padding:6px 14px;border-radius:100px;font-size:.875rem;font-weight:600;">Santa Catarina</span>
                    <span style="background:var(--blue-50);color:var(--blue-700);padding:6px 14px;border-radius:100px;font-size:.875rem;font-weight:600;">García</span>
                    <span style="background:var(--blue-50);color:var(--blue-700);padding:6px 14px;border-radius:100px;font-size:.875rem;font-weight:600;">General Escobedo</span>
                    <span style="background:var(--blue-50);color:var(--blue-700);padding:6px 14px;border-radius:100px;font-size:.875rem;font-weight:600;">San Nicolás</span>
                    <span style="background:var(--blue-50);color:var(--blue-700);padding:6px 14px;border-radius:100px;font-size:.875rem;font-weight:600;">Guadalupe</span>
                    <span style="background:var(--blue-50);color:var(--blue-700);padding:6px 14px;border-radius:100px;font-size:.875rem;font-weight:600;">Monterrey</span>
                </div>'''
            }
        ],
        'faqs': [
            ('¿Qué agua se usa en cromado y niquelado para evitar manchas?', 'El enjuague final tras el baño electrolítico requiere agua desionizada o desmineralizada de baja conductividad. Si el agua tiene minerales, estos se quedan en la pieza al secar generando water spots y manchas blancas — defectos visibles que llevan al rechazo de lote. Se recomienda conductividad menor a 50 µS/cm para enjuague de calidad y menor a 5 µS/cm para acabados premium.'),
            ('¿Qué agua se debe usar en pretratamiento de pintura automotriz?', 'El enjuague final tras el fosfatado requiere agua desmineralizada con conductividad menor a 20 µS/cm. Si el agua tiene minerales residuales, estos generan defectos de adherencia y "cráteres" en la película de pintura. Las líneas automotrices Tier 1 y OEM exigen esta especificación.'),
            ('¿Necesito agua desionizada para anodizado de aluminio?', 'Sí. Las etapas de enjuague entre baños del proceso de anodizado (decapado alcalino, baño anódico, sellado) requieren agua desionizada para no contaminar el siguiente baño con iones del anterior. Sin DI, los baños químicos se contaminan rápidamente, lo que reduce la calidad del óxido y eleva los costos de reposición de químicos.'),
            ('¿Atienden Wire EDM y electroerosión?', 'Sí. El Wire EDM y la electroerosión requieren agua desionizada como medio dieléctrico. Suministramos a talleres de matricería y troquelado de precisión en NL con consumo continuo de DI grado eléctrico.'),
            ('¿Cómo me confirman que el agua cumple la especificación de mi proceso?', 'Cada entrega incluye certificado de análisis con conductividad, dureza, TDS y pH. Para procesos críticos (anodizado, urea, electrónica) podemos agregar análisis específicos como sílice, cloruros y metales traza. Esta trazabilidad documenta cumplimiento ante auditorías de cliente y normas internas.'),
        ]
    },
    {
        'slug': 'agua-para-detergentes-quimicos',
        'title': 'Agua Desmineralizada para Fabricantes de Detergentes y Químicos | INDUAGUA NL',
        'h1': 'Agua Desmineralizada y Desionizada para Fabricantes de Detergentes, Jabones y Químicos Industriales',
        'meta': 'Agua desmineralizada y desionizada como ingrediente base para fabricantes de detergentes, jabones, químicos de formulación, pinturas y resinas en Monterrey y Nuevo León. Misma especificación en cada lote, análisis certificado.',
        'keywords': 'agua para detergentes, agua para fabricar jabón industrial, agua desmineralizada quimicos NL, agua para pinturas, agua para resinas Monterrey, proveedor agua quimica formulacion',
        'hero_image': 'app-detergentes.jpg',
        'hero_intro': 'Suministro de agua desmineralizada y desionizada como ingrediente base para fabricantes de detergentes, jabones, químicos de formulación, pinturas y resinas en Nuevo León. Si el agua representa más del 50 % de tu fórmula, su especificación define la calidad de tu producto final.',
        'wa_msg': 'Hola%2C%20me%20interesa%20cotizar%20agua%20para%20fabricar%20detergentes%20o%20quimicos',
        'sections': [
            {
                'title': 'El ingrediente principal de tu producto',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">En la mayoría de las fórmulas químicas de consumo industrial, el agua es <strong>el ingrediente con mayor proporción</strong>. Un detergente líquido típico contiene 60–80 % agua. Un limpiador industrial: 70–85 %. Una pintura base agua: 30–60 %. Una resina diluida: 40–70 %. En todos estos casos, la especificación del agua define directamente la calidad del producto terminado.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Si tu agua de entrada llega con conductividad inconsistente entre lotes, tu producción será inconsistente. Si tiene calcio o magnesio, puede inactivar parte de tus tensoactivos. Si tiene hierro, puede oxidar componentes y manchar el producto. Si tiene cloro residual, puede degradar fragancias y colorantes.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;">INDUAGUA entrega agua desmineralizada y desionizada con la misma especificación lote tras lote — para que tu producción sea consistente, tu producto pase las pruebas de cliente y tu marca conserve su reputación.</p>'''
            },
            {
                'title': 'Para qué procesos y productos surtimos',
                'bg': 'background:var(--gray-50);',
                'content': '''<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;">
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Detergentes líquidos</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Detergentes industriales, lavado de ropa, lavavajillas comercial, limpiadores multiusos. Agua sin dureza para mantener activos los tensoactivos.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Jabones y limpiadores</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Jabones líquidos para manos, geles antibacteriales, productos de aseo profesional para hoteles, hospitales e industria.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Pinturas base agua</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Pinturas vinílicas, esmaltes al agua, recubrimientos de látex. Agua desmineralizada para mantener estable la emulsión polimérica.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Resinas sintéticas</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Resinas acrílicas, vinílicas, alquídicas en dispersión. Polimerización controlada requiere agua de baja conductividad.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Químicos básicos</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Soluciones acuosas de inorgánicos y orgánicos, reactivos comerciales, mezclas dilutivas para procesos industriales.</p>
                    </div>
                    <div style="background:white;border:1px solid var(--gray-200);border-radius:12px;padding:24px;">
                        <h3 style="font-size:1.0625rem;font-weight:700;color:var(--navy);margin-bottom:10px;">Lubricantes y aditivos</h3>
                        <p style="color:var(--gray-600);font-size:.9375rem;line-height:1.7;">Emulsiones para corte metálico, aditivos de proceso, fluidos hidráulicos base agua para industria.</p>
                    </div>
                </div>'''
            },
            {
                'title': 'Volumen industrial con suministro consistente',
                'content': '''<p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Para fabricantes con producción entre 20,000 L y 200,000 L mensuales de producto final, el consumo de agua va de 15,000 L a 150,000 L mensuales. Manejamos este volumen con suministro recurrente programado en tote IBC de 1,000 L y entregas calendarizadas a tu planta.</p>
                <p style="color:var(--gray-600);font-size:1.0625rem;line-height:1.8;margin-bottom:16px;">Cobertura: Monterrey, Apodaca, Santa Catarina, García, General Escobedo, San Nicolás, Guadalupe, Pesquería, Salinas Victoria — donde se concentran las plantas de químicos, detergentes, pinturas y resinas en Nuevo León.</p>'''
            }
        ],
        'faqs': [
            ('¿Por qué necesito agua desmineralizada para fabricar detergente?', 'El agua representa entre 60 % y 80 % de la fórmula de un detergente líquido. Si tu agua tiene dureza (calcio/magnesio), estos minerales reaccionan con los tensoactivos aniónicos y los inactivan parcialmente — lo que reduce el poder limpiador del producto final. Si tiene hierro, puede oxidar y manchar. Agua desmineralizada con baja conductividad mantiene los activos al 100 % y asegura consistencia entre lotes.'),
            ('¿Qué especificación de agua piden las pinturas y resinas base agua?', 'Para pinturas vinílicas, esmaltes al agua y resinas en emulsión, se recomienda agua desmineralizada con conductividad menor a 20 µS/cm. Los iones disueltos pueden desestabilizar la emulsión polimérica, generar separación de fases, manchas en la película seca y reducción de la durabilidad del recubrimiento.'),
            ('¿Pueden surtir volúmenes industriales de químicos?', 'Sí. Manejamos suministro recurrente desde 10,000 hasta 200,000+ litros mensuales con calendario programado, entrega en tote IBC de 1,000 L y cobertura completa en Nuevo León. Para fabricantes con producción continua ofrecemos contratos de suministro con precio fijo y frecuencia garantizada.'),
            ('¿El agua cumple para auditorías ISO 9001 y registros sanitarios?', 'Sí. Cada lote entregado incluye certificado de análisis con conductividad, dureza, TDS y pH. Para productos con registro sanitario (COFEPRIS) o auditorías ISO/IATF, podemos agregar análisis específicos según tu protocolo de calidad y normativa aplicable.'),
            ('¿Es lo mismo agua desmineralizada que desionizada para mi formulación?', 'No son lo mismo. Desmineralizada (single-pass RO) tiene TDS 10–50 ppm y conductividad 15–50 µS/cm — suficiente para la mayoría de detergentes, jabones, pinturas y químicos generales. Desionizada (RO + resinas) tiene TDS <1 ppm — necesaria solo para productos altamente sensibles como cosméticos premium, farmacéutica o electrónica. Te ayudamos a determinar cuál te conviene según tu fórmula.'),
        ]
    },
]


# =========================================================================
# GENERAR ARCHIVOS
# =========================================================================
import os
for page in PAGES:
    html = build_page(
        slug=page['slug'],
        title=page['title'],
        h1=page['h1'],
        meta_desc=page['meta'],
        keywords=page['keywords'],
        hero_image=page['hero_image'],
        hero_intro=page['hero_intro'],
        sections=page['sections'],
        faqs=page['faqs'],
        wa_msg=page['wa_msg']
    )
    out = page['slug'] + '.html'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'OK {out} ({len(html)//1024} KB)')

print(f'\nTotal: {len(PAGES)} landing pages generadas')
