#ifndef SOCIAL_NETWORK_MICROSERVICES_SRC_MEDIASERVICE_MEDIAHANDLER_H_
#define SOCIAL_NETWORK_MICROSERVICES_SRC_MEDIASERVICE_MEDIAHANDLER_H_

#include <chrono>
#include <iostream>
#include <string>

#include "../../gen-cpp/MediaService.h"
#include "../logger.h"
#include "../tracing.h"

// 2018-01-01 00:00:00 UTC
#define CUSTOM_EPOCH 1514764800000

namespace social_network {

class MediaHandler : public MediaServiceIf {
 public:
  MediaHandler() = default;
  ~MediaHandler() override = default;

  void ComposeMedia(std::vector<Media> &_return, int64_t,
                    const std::vector<std::string> &,
                    const std::vector<int64_t> &,
                    const std::map<std::string, std::string> &) override;

 private:
};

template <typename T>
std::string vecToString(const std::vector<T>& vec) {
  std::ostringstream ss;
  for (size_t i = 0; i < vec.size(); ++i) {
    if (i != 0)
      ss << ",";
    ss << vec[i];
  }
  return ss.str();
}


void MediaHandler::ComposeMedia(
    std::vector<Media> &_return, int64_t req_id,
    const std::vector<std::string> &media_types,
    const std::vector<int64_t> &media_ids,
    const std::map<std::string, std::string> &carrier) {
  // Initialize a span
  auto start_time = std::chrono::high_resolution_clock::now();
  TextMapReader reader(carrier);
  std::map<std::string, std::string> writer_text_map;
  TextMapWriter writer(writer_text_map);
  auto parent_span = opentracing::Tracer::Global()->Extract(reader);
  auto span = opentracing::Tracer::Global()->StartSpan(
      "compose_media_server", {opentracing::ChildOf(parent_span->get())});
  opentracing::Tracer::Global()->Inject(span->context(), writer);

  if (media_types.size() != media_ids.size()) {
    ServiceException se;
    se.errorCode = ErrorCode::SE_THRIFT_HANDLER_ERROR;
    se.message =
        "The lengths of media_id list and media_type list are not equal";
    throw se;
  }

  for (int i = 0; i < media_ids.size(); ++i) {
    Media new_media;
    new_media.media_id = media_ids[i];
    new_media.media_type = media_types[i];
    _return.emplace_back(new_media);
  }
  // Record input-output
  auto end_time = std::chrono::high_resolution_clock::now();
  // 计算时间差，转换为毫秒
  std::chrono::duration<double> duration = end_time - start_time;
  std::stringstream input_ss;
  std::stringstream output_ss;
  size_t input_hash;
  size_t output_hash;
  std::string input_str;
  std::string output_str;
  std::hash<std::string> str_hash;

  // ComposeMedia
  input_ss << vecToString(media_types) << ',' << vecToString(media_ids);
  output_ss << vecToString(_return);
  input_str = input_ss.str();
  output_str = output_ss.str();
  input_hash = str_hash(input_str);
  output_hash = str_hash(output_str);
  std::cout << "[FunctionLog]: ComposeMedia," << input_hash << "," << output_hash << "," << duration.count() << std::endl;

  span->Finish();
}

}  // namespace social_network

#endif  // SOCIAL_NETWORK_MICROSERVICES_SRC_MEDIASERVICE_MEDIAHANDLER_H_
