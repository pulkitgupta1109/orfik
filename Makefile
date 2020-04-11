release: heroku netlify
heroku:
	cp .heroku.runtime.txt runtime.txt
	git add runtime.txt
	git commit -m 'heroku deploy'
	git push origin master
netlify:
	cp .netlify.runtime.txt runtime.txt
	git add runtime.txt  || echo 'nothing to add'
	git commit -m 'netlify deploy'  || echo 'nothing to commit'
	git push origin master
