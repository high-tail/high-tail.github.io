FROM ruby:latest

RUN gem install jekyll -v 4.3.4

WORKDIR /srv/jekyll

COPY . .

RUN bundle install & bundle update

EXPOSE 4000

CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0"]