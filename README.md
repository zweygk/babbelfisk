# Babbelfisk

Input a sentence, receive a pronunciation

```bash
cd babbelfisk
sudo docker build --tag bf .
sudo docker run -v "$(pwd)"/app.py:/app/app.py -p 5002:5002 bf
```

Example input

> Hey now, brown cow!!

Example curl

```bash
curl -X POST http://127.0.0.1:5002 -H 'Content-Type: application/json' -d '{"sentence":"Hey now, brown cow!!"}'
```

Example output

> {"lex":{"BROWN":["B","R","AW","N"],"COW":["K","AW"],"HEY":["HH","EY"],"NOW":["N","AW"]}}
