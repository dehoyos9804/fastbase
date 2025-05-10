# -*- coding: utf-8 -*-
# Define un diccionario llamado CSP_FOR_SECWEB que contiene la configuración de la Content Security Policy (CSP).
# Esta configuración será utilizada por la librería SecWeb para establecer las cabeceras CSP en las respuestas HTTP.
CSP_FOR_SECWEB = {
    # 'default-src': Especifica la política de carga por defecto para la mayoría de los tipos de recursos.
    "default-src": [
        "'self'", # Permite cargar recursos únicamente desde el mismo origen
    ],
    # 'script-src': Define las fuentes permitidas para la ejecución de JavaScript.
    "script-src": [
        "'self'", # Permite scripts que provienen del mismo origen que la página.
        "https://cdn.jsdelivr.net",  # Permite scripts cargados desde el CDN de jsdelivr.net.
        "'sha256-eV3QMumkWxytVHa/LDvu+mnW+PcSAEI4SfFu0iIlbDc='"
    ],
    # 'style-src': Define las fuentes permitidas para las hojas de estilo (CSS).
    "style-src": [
        "'self'", # Permite hojas de estilo que provienen del mismo origen.
        "https://cdn.jsdelivr.net", # Permite hojas de estilo cargadas desde el CDN de jsdelivr.net.
        "https://fonts.googleapis.com", # Permite hojas de estilo de Google Fonts (usadas para cargar las fuentes).
        "'unsafe-inline'" # Permite el uso de estilos inline (ej. <style>...</style> o style="...").
    ],
    # 'img-src': Define las fuentes permitidas para las imágenes.
    "img-src": [
        "'self'", # Permite imágenes que provienen del mismo origen.
        "data:", # Permite imágenes embebidas como data URIs (ej. data:image/png;base64,...).
        "https://fastapi.tiangolo.com",
        "https://cdn.redoc.ly"
    ],
    # 'font-src': Define las fuentes permitidas para las fuentes web (utilizadas con @font-face).
    "font-src": [
        "'self'", # Permite fuentes que provienen del mismo origen.
        "https://fonts.gstatic.com"
    ],
    # 'connect-src': Restringe las URL a las que se puede conectar usando interfaces como fetch,
    # XMLHttpRequest, WebSocket, y EventSource.
    "connect-src": [
        "'self'" # Permite conexiones (XHR, WebSockets, etc.) únicamente al mismo origen.
    ],
    # 'object-src': Define las fuentes permitidas para los elementos <object>, <embed>, y <applet>.
    "object-src": [
        "'none'" # Bloquea la carga de este tipo de plugins o contenido embebido.
    ],
    # 'base-uri': Restringe las URL que pueden ser usadas en el elemento <base> de un documento HTML.
    "base-uri": [
        "'self'" # Permite que la URI base del documento sea únicamente el propio origen.
    ],
    # 'form-action': Especifica las URL válidas a las que se pueden enviar formularios (<form action="...">).
    "form-action": [
        "'self'" # Permite que los formularios se envíen únicamente al mismo origen.
    ],
    # 'frame-ancestors': Especifica qué orígenes pueden embeber
    # la página actual usando <frame>, <iframe>, <object>, <embed>, o <applet>.
    "frame-ancestors": [
        "'none'" # Impide que la página sea embebida en cualquier otro sitio
    ],
    "worker-src": [
        "blob:"
    ]
}
