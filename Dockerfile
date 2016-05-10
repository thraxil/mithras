FROM ccnmtl/django.base
ADD wheelhouse /wheelhouse
RUN /ve/bin/pip install --no-index -f /wheelhouse -r /wheelhouse/requirements.txt \
&& rm -rf /wheelhouse
WORKDIR /app
COPY . /app/
RUN /ve/bin/python manage.py test \
&& npm set progress=false \
&& npm install \
&& ./node_modules/.bin/webpack --config webpack.prod.config.js
EXPOSE 8000
ADD docker-run.sh /run.sh
ENV APP mithras
ENTRYPOINT ["/run.sh"]
CMD ["run"]
