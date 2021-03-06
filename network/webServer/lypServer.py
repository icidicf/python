#!/usr/bin/python
import web
import xml.etree.ElementTree as ET

tree = ET.parse('user_data.xml')
root = tree.getroot()

urls = (
    '/users', 'list_users',
    '/users/(.*)', 'get_user'
    )

class MyApplication(web.application):
    def run(self, port=8099, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = web.application(urls, globals())

class list_users:        
    def GET(self):
        output = 'users:[';
        for child in root:
            print 'child', child.tag, child.attrib
            output += str(child.attrib) + ','
            output += ']';
            return output

class get_user:
    def GET(self, user):
        for child in root:
            if child.attrib['id'] == user:
                return str(child.attrib)

if __name__ == "__main__":
    app = MyApplication(urls, globals())
    app.run()
