from django.template import loader, TemplateSyntaxError
try:
    loader.get_template('base.html')
    print('Template compiled')
except TemplateSyntaxError as e:
    print('TS error:', e)
    import traceback; traceback.print_exc()