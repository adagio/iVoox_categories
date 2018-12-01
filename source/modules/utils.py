import requests

class Utils:

    def __init__(self):
        pass
        #self.logger = logger

    def get_url_content(self, url):
        """
            Extrae el contenido de unas URL específicas
        """

        #self.logger.info('Get content: Start')

        res = requests.get(url)
        # Levanta el error solo si algo fue mal (errores 400)
        try:
            res.raise_for_status()
        except Exception as exc:
            print('Problem! %s' % (exc))

        text = res.text

        #self.logger.info('Get content: Completed')

        return text