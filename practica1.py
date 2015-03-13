#!/usr/bin/python

"""
 contentApp class
 Simple web application for managing content

 Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles 2009-2015
 jgb, grex @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2015
"""

import webapp
import urllib


class practica1 (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content
    content = {}
    contentInverso = {}
    num_sec = 0

    def parse(self, request):
        """Return the resource name (including /)"""
        metodo = request.split(' ', 2)[0]
        recurso = request.split(' ', 2)[1]

        if metodo == "GET":
            cuerpo = request.split(' ',2)[1][1:]
            print "Recibido GET con cuerpo " + cuerpo + " y recurso " + recurso
        elif metodo == "POST":
            cuerpo = request.split("\r\n\r\n")[-1]
            cuerpo = cuerpo.split("url=",2)[-1]
            cuerpo = cuerpo.split("http%3A%2F%2F",2)[-1]
            cuerpo = "http://" + cuerpo
            print "Recibido POST con cuerpo " + cuerpo + " y recurso" + recurso

        return (metodo, recurso, cuerpo)

    def process(self, resourceName):
        """Process the relevant elements of the request.

        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """
        (metodo, recurso, cuerpo) = resourceName

        httpCode = "HTTP/1.1 200 OK\r\n\r\n"
        httpBody = "<html><body><h1>Ooops! Algo salio mal :(</h1></body></html>"
        
        if metodo == "GET":
            if cuerpo in self.contentInverso.keys():
                httpCode = "300 Redirect"
                htmlBody = "<html><head><meta http-equiv='refresh' content='0;url=" \
						   + str(self.contentInverso[cuerpo]) + "'></head></html>"
            elif cuerpo == "":
                httpCode = "200 OK"
                htmlBody = "<html><body><h1>" + str(self.content) + "</h2>" + \
						   "<h2>Introduzca la url que quiera acortar</h2><form method=post action=http://localhost:1234>" + \
				   		   "URL:<input type = name name = url original></body>"
                return (httpCode, htmlBody)
            else:
                httpCode = "400 ERROR"
                htmlBody = "<html><body><h1>La url acortada introducida no existe," + \
                           " asegurese de meterla correctamente</h1>" + \
                           "<a href='http://localhost:1234'>Pulse aqui para volver al diccionario</a>" + \
                           "<body><html>"
        elif metodo == "POST":
            if cuerpo in self.content.keys():
                httpCode = "200 OK"
                htmlBody = "<html><head></head><h1><a href='" + str(cuerpo) + "'>" \
					       + "http://localhost:1234/" + str(self.content[cuerpo]) + "-->" \
                           + str(cuerpo) + "</a></h1></body></html>"
                return (httpCode, htmlBody)
            else:
                try:
					pag = urllib.urlopen(cuerpo)
                except IOError:
                    httpCode = "400 ERROR"
                    httpBody = "<html><head><h1>La pagina que intenta guardar no existe</h1>" + \
                               "<a href='http://localhost:1234'>Pulse aqui para volver al diccionario</a>" + \
                               "</head></html>"
                    return(httpCode, httpBody)

                self.content[cuerpo] = self.num_sec
                self.contentInverso[str(self.num_sec)] = cuerpo
                self.num_sec += 1
                
                httpCode = "200 OK"
                htmlBody = "<html><body><h1>La pagina: " + str(cuerpo) + \
                           " ha sido acortada. Su url es: " + str(self.content[cuerpo]) + "</h1>"\
                           " <a href='http://localhost:1234'>Pulse aqui para volver al diccionario</a>" + \
                           " <a href='" + str(cuerpo) + "'>Pulse aqui para ir a la url original</a>" + \
                           " </body></html>"
      
        return (httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = practica1("localhost", 1234)
