docker build -t webdrop .
docker run -dp 80:80 -v D:\Desktop\WebDrop:/code/app/drop webdrop