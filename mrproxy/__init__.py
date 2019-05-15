#!/usr/bin/env python

import sys

if sys.version_info[0] < 3:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from urllib import addinfourl
    from urllib2 import (
        HTTPRedirectHandler, build_opener, install_opener, urlopen,
        URLError, HTTPError,
        Request,
    )
else:
    from http.server import BaseHTTPRequestHandler
    from urllib.response import addinfourl
    from urllib.request import HTTPRedirectHandler, build_opener, install_opener, urlopen, Request
    from urllib.error import URLError, HTTPError


class NoRedirectHandler(HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302


opener = build_opener(NoRedirectHandler())
install_opener(opener)


class UserProxyHandler(BaseHTTPRequestHandler):

    @property
    def dest_url(self):
        return "http://localhost:%s%s" % (self.server.args.backend_port, self.path)

    def finish_request(self, code, headers, output):
        self.send_response(code)
        for key, value in headers:
            self.send_header(key, value)
        self.end_headers()
        self.wfile.writelines(output)

    def updated_headers(self):
        headers = dict(self.headers)
        for header in self.server.args.header:
            key, value = header.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers

    def do_request(self, request):
        try:
            url = urlopen(request)
            data = url.readlines()
        except HTTPError as err:
            return self.finish_request(err.getcode(), {}, err.readlines())
        except URLError as err:
            msg = ["503 Service Unavailable: {}\n".format(err).encode('utf-8')]
            return self.finish_request(503, {}, msg)

        return self.finish_request(url.getcode(), url.info().items(), data)

    def do_GET(self, method="GET"):
        headers = self.updated_headers()
        request = Request(self.dest_url, headers=headers)
        request.get_method = lambda: method
        self.do_request(request)

    def do_POST(self, method="POST"):
        content_len = int(self.headers['Content-Length'])
        data = self.rfile.read(content_len)
        headers = self.updated_headers()
        request = Request(self.dest_url, headers=headers, data=data)
        request.get_method = lambda: method
        self.do_request(request)

    def do_PUT(self):
        self.do_POST("PUT")

    def do_DELETE(self):
        self.do_GET("DELETE")

    def do_PATCH(self):
        self.do_POST("PATCH")

    def do_OPTIONS(self):
        self.do_GET("OPTIONS")
