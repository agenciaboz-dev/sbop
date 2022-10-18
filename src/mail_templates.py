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
        :root {{
            --primary-color: #0C6397;
            --input-background: #E4E4E4;
            --primary-text-color: #8D8D8D;
            --secondary-text-color: #6B6B6B;
            --line-color: #707070;
        }}

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

        body {{
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #E4E4E4;
        }}

        .main-container {{
            display: flex;
            flex-direction: column;
            height: min-content;
            width: 90%;
            background-color: white;
            border-radius: 2vw;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            margin: 7.5vh;
            padding: 2vh 2vw 3vh;
            outline: var(--primary-color) solid 0.4vw;
        }}

        /* .top-row {{
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            position: relative;
        }} */

        img {{
            height: 30vh;
            width: auto;
            position: absolute;
            right: 50px;
            top: 25px;
        }}

        /* .bottom-row {{
            display: flex;
            flex-direction: row;
            word-wrap: break-word;
        }} */

        h1 {{
            color: var(--secondary-text-color);
            margin: 2vh 0;
        }}

        h2 {{
            color: var(--primary-text-color);
        }}

        a {{
            color: var(--primary-color);
        }}
    </style>
</head>

<body>
    <div class="main-container">
        <!-- <div class="top-row"> -->
        <div>
            <h1>Redefinição de senha - SBOP</h1>
            <h2>Nome de usuário: {nome}</h2>
        </div>
        <img src="https://sbop.com.br/wp-content/uploads/2020/08/SBOP-LOGO-AZUL-1x1-PNG.png" alt="">
        <!-- </div> -->
        <!-- <div class="bottom-row"> -->
        <p>Clique no link para redefinir sua senha: <a
                href="{link}">{link}</a>
        </p>
        <!-- </div> -->
    </div>
</body>

</html>
"""
