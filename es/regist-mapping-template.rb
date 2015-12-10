#!/usr/bin/env ruby

require 'json'
require 'net/http'
require 'uri'

def http_request(uri, body)
  uri  = URI.parse(uri)
  http = Net::HTTP.new(uri.host, uri.port)
  if uri.scheme == "https"
    http.use_ssl = true
  end
  req  = Net::HTTP::Post.new(uri.request_uri)
  req["Content-Type"] = "application/json"
  req.body = body
  http.request(req)
end

def create_mapping_template(es_host, template_name)
  uri  = "#{es_host}" + "/_template/" + "#{template_name}" 
  mapping = <<EOS
{
  "template": "s3_access_log-*",
  "mappings" : {
    "s3_access_log" : {
      "properties" : {
        "bucket_name" : {
          "type" : "string"
        },
        "bucket" : {
          "type" : "string"
        },
        "ip" : {
          "type" : "string"
        },
        "requestor_id" : {
          "type" : "string"
        },
        "request_id" : {
          "type" : "string"
        },
        "operation" : {
          "type" : "string"
        },
        "key" : {
          "type" : "string"
        },
        "http_method_uri_proto" : {
          "type" : "string"
        },
        "http_status" : {
          "type" : "string"
        },
        "s3_error" : {
          "type" : "string"
        },
        "bytes_sent" : {
          "type" : "string"
        },
        "object_size" : {
          "type" : "string"
        },
        "total_time" : {
          "type" : "string"
        },
        "turn_around_time" : {
          "type" : "string"
        },
        "referer" : {
          "type" : "string"
        },
        "user_agent" : {
          "type" : "string"
        },
        "datetime" : {
          "type" : "date",
          "format" : "dateOptionalTime"
        }
      }
    }
  }
}
EOS
  res = http_request(uri, mapping)
  puts "code: #{res.code}"
  puts "msg: #{res.message}"
  puts "body: #{res.body}"
end

create_mapping_template(ENV["ES_ENDPOINT"], ENV["ES_TEMPLATE_NAME"])
