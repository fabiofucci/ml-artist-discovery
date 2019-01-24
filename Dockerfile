FROM python

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN groupadd -g 999 appuser && \
    useradd -r -u 999 -g appuser appuser

USER appuser

# expose port 8080
EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["app.py"]