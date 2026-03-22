import json

# Cargar archivos
with open('productos_streamXM_pricing.json', 'r', encoding='utf-8') as f:
    productos_originales = json.load(f)

with open('Qwen_json_20260322_v62djf3rp.json', 'r', encoding='utf-8') as f:
    productos_pricing = json.load(f)

# Crear diccionario de productos de pricing por id_producto
pricing_dict = {prod['id_producto']: prod for prod in productos_pricing['productos']}

# Lista para productos fusionados
productos_fusionados = []

# Procesar cada producto original
for prod_orig in productos_originales['productos']:
    id_prod = prod_orig['id_producto']
    
    # Crear copia del producto original (manteniendo TODAS las llaves originales)
    prod_fusionado = prod_orig.copy()
    
    # Si existe pricing para este producto, agregar las llaves de pricing
    if id_prod in pricing_dict:
        prod_pricing = pricing_dict[id_prod]
        
        # Agregar solo las llaves NUEVAS de pricing (sin sobrescribir las originales)
        llaves_pricing = [
            'costo_soles',
            'precio_piso_usd',
            'precio_piso_soles',
            'precio_tramo_usd',
            'precio_tramo_soles',
            'precio_soles_fresia',
            'precio_soles_teleplus',
            'precio_soles_josevas',
            'tipo_cuenta_nuestra',
            'tipo_cuenta_competencia',
            'precio_soles_streamXM',
            'ganancia_soles',
            'ganancia_pct',
            'nota_estrategica',
            'categoria'
        ]
        
        for llave in llaves_pricing:
            if llave in prod_pricing:
                prod_fusionado[llave] = prod_pricing[llave]
    
    productos_fusionados.append(prod_fusionado)

# Crear estructura final manteniendo metadata original
resultado = {
    "total": productos_originales.get('total', 69),
    "fecha_scraping": productos_originales.get('fecha_scraping', '2026-03-21T00:15:47'),
    "tiempo_segundos": productos_originales.get('tiempo_segundos', 284),
    "productos": productos_fusionados
}

# Guardar archivo fusionado
with open('productos_streamXM_pricing_final.json', 'w', encoding='utf-8') as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print(f"✅ Archivo generado: productos_streamXM_pricing_final.json")
print(f"📦 Total de productos: {len(productos_fusionados)}")

# Verificar que se mantengan las llaves
prod_ejemplo = productos_fusionados[0]
print(f"\n📋 Llave del primer producto:")
for key in prod_ejemplo.keys():
    print(f"  - {key}")