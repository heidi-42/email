import asyncio
import smtplib
from concurrent.futures import ThreadPoolExecutor


def get_template_variables(template, env):
    template_source = env.loader.get_source(env, template)[0]
    parsed_content = env.parse(template_source)

    variables = {}
    for record in parsed_content.body:
        if hasattr(record, 'node') and hasattr(record, 'target'):
            variables[record.target.name] = record.node.value
    return variables


class Mail:

    def __init__(self, host, credentials, jinja):
        self.host = host
        self.credentials = credentials
        self.jinja = jinja
        self.executor = ThreadPoolExecutor(max_workers=32)

    def send_template_sync(self, recipients, template, data, sender=None):
        server = smtplib.SMTP_SSL(self.host)
        server.login(*self.credentials)

        if sender is None:
            variables = get_template_variables(template, self.jinja)
            sender = variables['sender']

        template = self.jinja.get_template(template)
        server.sendmail(sender, recipients,
                        template.render(data).encode('utf8'))
        server.quit()

    async def send_template(self, recipients, template, data, sender=None):
        loop = asyncio.get_event_loop()
        loop.run_in_executor(
            self.executor,
            self.send_template_sync,
            recipients, template, data, sender
        )
