from handlers import route


@route.post('/template_email')
async def post_template_email(request):
    payload = await request.json()
    await request.app['mail'].send_template(**payload)
