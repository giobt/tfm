FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN wget https://www.antlr.org/download/antlr-4.8-complete.jar \
    && java -jar "antlr-4.8-complete.jar" -Dlanguage=Python3 ./pattern_grammar/STIXPattern.g4 -o ./compiled_grammar

CMD [ "python", "./producer.py" ]