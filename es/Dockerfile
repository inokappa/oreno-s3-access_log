FROM ruby
MAINTAINER inokappa
RUN apt-get update
ADD regist-mapping-template.rb /app/regist-mapping-template.rb
RUN chmod 755 /app/*.rb

CMD ["/app/regist-mapping-template.rb"]
