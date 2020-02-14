Orfik
=====

- Infrastructure
    - Site is served in two parts.
    - Main pages are served statically. I like netlify for this due to auto builds etc.
    - Leaderboard needs to be dynamic so we serve that dynamically using pythonanywhere/heroku etc.
    - Combo of those two should be cheap as hell. I already own compsoc.club so we can use that to host if you want.
- Session management
    - Each user-pwd combo is hashed and stored in the browser as a cookie.
    - Any action that requires identifying the user has to send this hash.
    - Ultimately the winner has to produce the winning hash (aka user-pwd combo) to claim the prize.
- Question structure
    - We add questions and their answers to the codebase. Codebase remains private for the duration of the contest.
    - Each question's url is the hash of the previous question's answer. This ensures that people can't proceed unless they have the right answer for the current question.
    - We can also have multiple answers for the same question because of this scheme.
- Leaderboard
    - The static site fetches data from the dynamic site to display the current leaderboard.
    - Everytime someone lands on a question page, javascript on that page sends an ajax request to our dynamic server with `{'url': window.location.href, 'hsh': "user-pwd hash"}`.
    - We can now calculate every person's path through the question set and assign a score.
    - Leaderboard can now be visualized like a time graph
        - Let x axis be time. Let y axis be question number.
        - We can now plot multiple lines denoting player positions in the contest throughout time for the leaderboard.
        - By default we can show the latest rankings.
        - End of the contest we have a nice video which shows how the contest progressed.



```
python -m orfik build
```
