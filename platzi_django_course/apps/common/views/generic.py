from django.http import HttpResponseNotAllowed


class MethodOverrideMixin:
    allowed_methods = ['put', 'delete', 'patch']
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            overriden_method = request.POST.get('_method', '').lower()
            if overriden_method in self.allowed_methods:
                request.method = overriden_method.upper()
        
        if self.request.method.lower() not in self.http_method_names:
            return HttpResponseNotAllowed(self.http_method_names)
        
        return super().dispatch(request, *args, **kwargs)
