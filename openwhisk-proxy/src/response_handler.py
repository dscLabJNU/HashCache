import utils


class ResponseHandler:
    @classmethod
    def route_request(cls, flow):
        reqeust_path = flow.request.path
        request_url = flow.request.url
        if "s3" in request_url:
            return cls.handle_s3_response(flow=flow)

    @staticmethod
    def handle_s3_response(flow):
        response_content = flow.response.content
        saved_file_name = flow.request.headers['hash_url']

        # TODO 异步请求
        if flow.request.headers['file_exsited'] == "False" and flow.request.method == 'GET':
            utils.save_files(saved_file_name, response_content)
        return None