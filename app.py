import os
import tornado.ioloop
import tornado.web
from tornado.escape import json_encode


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, LendingFront!")


class ValidateLoan(tornado.web.RequestHandler):

    def make_response(self, data):
        """
        Prepare the correct response for JSONP.
        :param data: Dict with the data to send.
        :return: The data with the correct format.
        """
        callback = self.get_argument('callback')
        jsonp = "{jsfunc}({json});".format(jsfunc=callback,
            json=json_encode(data))
        return jsonp

    def post(self):
        try:
            data = self.request.arguments
            if 'amount' in data:
                amount = float(data['amount'][0])
                if 50000 == amount:
                    msg = 'Undecided'
                else:
                    msg = 'Declined' if amount > 50000 else 'Approved'
                status = 200
            else:
                msg = 'Amount not given.'
                status = 401

            res = {'data': msg, 'status': status}
            self.write(self.make_response(res))

        except Exception as e:
            res = {'data': e.message, 'status': 500}
            self.write(self.make_response(res))
    get = post


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/validate_loan", ValidateLoan),
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(int(os.environ.get('PORT', '5000')))
    tornado.ioloop.IOLoop.current().start()
