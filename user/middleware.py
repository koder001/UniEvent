from django.shortcuts import redirect

class RedirectToIndexMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Проверяем, является ли запрос пустым (только название сайта)
        if not request.path.strip('/'):
            # Проверяем, зарегистрирован ли пользователь
            if getattr(request, 'user', None) and request.user.is_authenticated:
                return redirect('user/dashboard')
            else:
                return redirect('user/login')  # Или используйте ваш URL для страницы регистрации

        if request.path.strip('/') == 'user':
            # Проверяем, зарегистрирован ли пользователь
            if getattr(request, 'user', None) and request.user.is_authenticated:
                return redirect('dashboard')
            else:
                return redirect('login')  # Или используйте ваш URL для страницы регистрации
        
        # Продолжаем выполнение обычного запроса        
        response = self.get_response(request)
        return response