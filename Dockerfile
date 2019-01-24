FROM python

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser

USER appuser

EXPOSE 8080

# ENV FLASK_ENV=development
# ENV FLASK_DEBUG=1

ENTRYPOINT ["python"]
CMD ["app.py"]