from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = ['ADMINISTRATOR', 'AUTHORITY', 'VIEWER']
    
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.headers.get('Accept', ''):
                    return JsonResponse({'error': 'Authentication required'}, status=401)
                return redirect('accounts:login')
            
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            profile = getattr(request.user, 'profile', None)
            user_role = profile.role if profile else 'VIEWER'
            
            if user_role not in allowed_roles:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'json' in request.headers.get('Accept', ''):
                    return JsonResponse({'error': 'Permission denied. Insufficient role privileges.'}, status=403)
                messages.error(request, "Access Denied: Your account role does not have authorization for this action.")
                return redirect('dashboard:index')
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
