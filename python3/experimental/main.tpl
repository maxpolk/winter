<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8"/>
        <title>Experimental wiki</title>
    </head>
    <body>
        <h1>Experimental wiki</h1>

        <h2>Request</h2>
        <pre>
        %for line in result:
    {{line}}
        %end
        </pre>

        <h2>Request Headers</h2>
        <ul>
            %for header in headers.keys():
            <li>{{header}}: {{headers[header]}}</li>
            %end
        </ul>

        <h2>Runtime Environment</h2>
        <ul>
            %for key in environ.keys():
            <li>{{key}}: {{environ[key]}}</li>
            %end
        </ul>
    </body>
</html>
