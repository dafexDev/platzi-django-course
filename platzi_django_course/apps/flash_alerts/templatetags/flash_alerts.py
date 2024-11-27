from django.template.library import Library
from django.contrib import messages
from django.template.loader import render_to_string


register = Library()


@register.simple_tag(takes_context=True)
def show_flash_alerts(context, template='html'):
    request = context['request']
    
    flash_alerts = []
    for message in messages.get_messages(request):
        message_type = ''
        if message.level == messages.SUCCESS:
            message_type = 'success'
        elif message.level == messages.WARNING:
            message_type = 'warning'
        elif message.level == messages.ERROR:
            message_type = 'error'
        elif message.level == messages.INFO:
            message_type = 'info'
        elif message.level == messages.DEBUG:
            message_type = 'debug'
        
        flash_alerts.append({
            'message': message.message,
            'type': message_type
        })
        
    template_context = {
        'flash_alerts': flash_alerts
    }
    
    if template == 'html':
        return render_to_string('flash_alerts/alerts.html', template_context)
    elif template == 'bootstrap':
        return render_to_string('flash_alerts/bootstrap_alerts.html', template_context)
    else:
        raise ValueError(f"Template '{template}' is not a valid option. Use 'html' or 'bootstrap'.")
