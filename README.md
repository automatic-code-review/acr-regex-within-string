# acr-within-string

Arquivo config.json

- data
    - message
        - descrição da mensagem
    - inverted
        - se deve verificar o regex de forma invertida
    - language
        - linguagem do snipset
    - stringToIgnore
        - lista de regex para ignorar strings especificas
    - stringLineRegex
        - lista de regex para ignorar linhas inteiras
    - regexFile
        - lista de regex para verificar quais arquivos devem verificar
    - regex
        - lista de regex para verificar na string, respeitando o campo inverted

```json
{
  "data": [
    {
      "message": "${TEXT} - ${FILE_PATH} - ${LINE}",
      "inverted": true,
      "language": "java",
      "stringToIgnore": [
        ""
      ],
      "stringLineRegex": [
        ""
      ],
      "regexFile": [
      ],
      "regex": [
      ]
    }
  ]
}
```
