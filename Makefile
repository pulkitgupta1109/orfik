release:
	cp .heroku.runtime.txt runtime.txt
	git add runtime.txt
	git commit -m 'heroku deploy'
	cp .netlify.runtime.txt runtime.txt
	git add runtime.txt
	git commit -m 'netlify deploy'
