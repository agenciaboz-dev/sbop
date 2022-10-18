def recoverPasswordTemplate(nome, link):
    return f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redefinição de senha - SBOP</title>
    <style>
        @font-face {{
            font-family: Montserrats;
            src: url("/static/fonts/Montserrat-Regular.otf");
        }}

        @font-face {{
            font-family: Montserrats;
            src: url("/static/fonts/Montserrat-Bold.otf");
            font-weight: bold;
        }}

        * {{
            box-sizing: border-box;
            font-family: Montserrats;
            width: 100%;
        }}

        .main-container {{
            height: min-content;
            width: 90%;
            background-color: white;
            border-radius: 2vw;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            margin: 7.5vh;
            padding: 2vh 2vw 3vh;
            outline: #0C6397 solid 0.4vw;
        }}

        img {{
            height: 30vh;
            width: auto;
            position: absolute;
            right: 75px;
            top: 25px;
        }}

        h1 {{
            color: #6B6B6B;
            margin: 2vh 0;
        }}

        h2 {{
            color: #8D8D8D;
        }}

        a {{
            color: #0C6397;
        }}
    </style>
</head>

<body>
    <div class="main-container">
        <div>
            <h1>Redefinição de senha - SBOP</h1>
            <h2>Nome de usuário: {nome}</h2>
        </div>
        <img src="https://sbop.com.br/wp-content/uploads/2020/08/SBOP-LOGO-AZUL-1x1-PNG.png" alt="">
        <p>Clique no link para redefinir sua senha: <a
                href="{link}">{link}</a>
        </p>
    </div>
</body>

</html>
"""
