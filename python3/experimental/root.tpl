<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8"/>
        <title>Experimental wiki</title>
    </head>
    <body>
        <h1>Experimental wiki</h1>

        <h2>Some test pages</h2>
        <ul>
        %for link in links:
          <li><a href="{{link}}">{{link}}</a></li>
        %end
        </ul>
    </body>
</html>
