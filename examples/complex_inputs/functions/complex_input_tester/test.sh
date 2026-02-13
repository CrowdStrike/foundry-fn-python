curl -X POST --location "http://localhost:8081" \
    -H "Content-Type: multipart/form-data" \
    -F meta='{
          "url": "/complex-test",
          "method": "POST"
      }' \
    -F body='{
           "name": "Sam",
           "age": 35
       }' \
    -F file1='@lorem-ipsum-1.txt;filename=lorem-ipsum-1.txt' \
    -F file2='@lorem-ipsum-2.txt;filename=lorem-ipsum-2.txt' \
    -F file3='@lorem-ipsum-3.txt;filename=lorem-ipsum-3.txt'