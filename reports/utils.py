def ordering(queryset,request):
    filter_date = 'publication_date'
    filter_cvss = '-cvss'

    date = request.GET.get('date','')
    cvss = request.GET.get('cvss','')
        
    if cvss == 'asc':
        filter_cvss = 'cvss'
    
    if date == 'desc':
        filter_date = '-publication_date'
    
    reports = queryset.order_by(filter_date,filter_cvss)

    return reports


def queryset_filter(entry,request):
    severity_states = {
        "critico":"Crítico",
        "alto":"Alto",
        "medio":"Médio",
        "baixo": "Baixo"

    }

    severity_type = request.GET.get('severity','')
    fixed_type = request.GET.get('fixed','')
    valid_fixed_type = (fixed_type == "corrigida") or (fixed_type == "nao-corrigida")


    if severity_type in severity_states.keys() and valid_fixed_type:
        return entry.objects.filter(severity=severity_states[severity_type],fixed=(fixed_type == "corrigida"))

    if valid_fixed_type:
        return entry.objects.filter(fixed=(fixed_type == "corrigida"))

    if severity_type in severity_states.keys():
        return entry.objects.filter(severity=severity_states[severity_type])


    return entry.objects.all()