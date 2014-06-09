sudo easy_install pip
sudo pip install markdown2
sudo pip install pygments

sudo cp ./base.css /Library/WebServer/Documents/base.css
sudo chmod a+x md2html
sudo chmod a+x md2pdf
sudo cp md2pdf /usr/bin
sudo cp md2html /usr/bin
sudo cp -r wkhtmltox /usr/local/Cellar
