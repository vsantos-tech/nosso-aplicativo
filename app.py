<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    
    <!-- Título que vai aparecer no iPhone -->
    <title>Nosso Aplicativo 💗</title>

    <!-- Configurações para o iOS abrir em TELA CHEIA total sem barras -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="mobile-web-app-capable" content="yes">

    <!-- Ícone em formato .jpg ajustado -->
    <link rel="apple-touch-icon" href="icone.jpg">

    <style>
        /* Zera margens, paddings e remove barras brancas */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #FFD1DC; /* Cor de fundo suave durante o carregamento */
        }

        /* Faz o Streamlit expandir 100% na tela do iPhone */
        iframe {
            width: 100vw;
            height: 100vh;
            border: none;
            display: block;
        }
    </style>
</head>
<body>

    <!-- Carrega o app Streamlit dentro do envelope -->
    <iframe src="https://ra-larissa.streamlit.app/?embed=true"></iframe>

</body>
</html>
