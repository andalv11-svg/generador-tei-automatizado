from groq import Groq

# Divide el texto en fragmentos seguros para evitar superar el límite de tokens
def dividir_texto(texto, max_chars=6000):
    partes = []
    while len(texto) > max_chars:
        corte = texto.rfind(" ", 0, max_chars)
        if corte == -1:
            corte = max_chars
        partes.append(texto[:corte])
        texto = texto[corte:]
    partes.append(texto)
    return partes

def generar_tei(texto_plano, api_key):
    try:
        if not api_key.startswith("gsk_"):
            return "❌ Error: La API key de Groq debe empezar por 'gsk_'."

        if not texto_plano.strip():
            return "❌ Error: No hay texto para procesar."

        client = Groq(api_key=api_key)

        # Dividir el texto en partes para evitar el error 413
        partes = dividir_texto(texto_plano, max_chars=6000)
        contenido_tei = ""

        for i, parte in enumerate(partes, start=1):
            prompt = f"""
            Marca el siguiente fragmento en formato TEI siguiendo las directrices TEI P5.
            No inventes contenido. Respeta la estructura original.
            NO incluyas cabecera TEI, solo el contenido del cuerpo.
            Fragmento {i}/{len(partes)}:
            {parte}
            """

            respuesta = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": "Eres un experto en marcado TEI."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_completion_tokens=4096
            )

            contenido_tei += respuesta.choices[0].message.content.strip() + "\n"

        # Envolver todo en un único TEI válido
        tei_envuelto = f"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Texto marcado en TEI</title>
      </titleStmt>
      <publicationStmt>
        <p>Generado automáticamente</p>
      </publicationStmt>
      <sourceDesc>
        <p>Fuente original proporcionada por el usuario</p>
      </sourceDesc>
    </fileDesc>
  </teiHeader>
  <text>
    <body>
{contenido_tei}
    </body>
  </text>
</TEI>"""

        return tei_envuelto

    except Exception as e:
        return f"❌ Error al generar TEI: {str(e)}"
