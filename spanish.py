from render import generate_video

if __name__ == "__main__":

    # Bark voice presets
    # https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c

    generate_video(
        input_pdf_path="beamer.pdf",
        dpi=600,
        scripts=[
            {
                "text": 'Bienvenidos a la presentación de nuestro trabajo enfocado en recomendar rutas verdes para peatones ' +
                        'para reducir la exposición a contaminantes del aire en Barcelona. Este es un trabajo conjunto entre ' +
                        'el Instituto de Investigación en Inteligencia Artificial y la Universidad UPF en Barcelona.',
                "pdf_page_number": 1,
            },
            {
                "text": 'El principal problema que abordamos en este trabajo es cómo recomendar rutas verdes a los peatones ' +
                        'que minimicen la exposición a contaminantes del aire en una ciudad. Los peatones son los individuos más vulnerables ' +
                        'cuando se trata de la contaminación del aire, que puede ocasionar serios problemas de salud.',
                "pdf_page_number": 2,
            },
            {
                "text": 'En esta línea, responder a esta pregunta de investigación podría ser de gran interés para los ciudadanos ' +
                        'que se preguntan si hay alternativas más verdes para sus trayectos, incluso si implica caminar un poco más.',
                "pdf_page_number": 3,
            },
            {
                "text": 'De manera similar, las administraciones públicas preocupadas por la salud de sus ciudadanos podrían estar interesadas ' +
                        'en una herramienta capaz de proporcionar alternativas más verdes a las rutas calculadas por Google Maps, ' +
                        'que no considera la exposición a contaminantes del aire.',
                "pdf_page_number": 4,
            },
            {
                "text": 'En este trabajo proporcionamos una solución a estas preguntas de investigación con nuestro prototipo de rutas verdes, mostrándolo ' +
                        'para la ciudad de Barcelona. Específicamente, podemos calcular rutas que minimicen la exposición a contaminantes del aire, ' +
                        'en lugar de minimizar la distancia total como se hace usualmente en los problemas normales de enrutamiento.',
                "pdf_page_number": 5,
            },
            {
                "text": 'La exposición a contaminantes se calcula considerando datos históricos de calidad del aire proporcionados por el ayuntamiento de Barcelona. ' +
                        'Esta fuente de datos se caracteriza por una resolución espacial muy alta, ya que proporciona una medición de calidad del aire para ' +
                        'cada calle del mapa. Por otro lado, se caracteriza por una baja resolución temporal, ya que se publica una vez al año.',
                "pdf_page_number": 6,
            },
            {
                "text": 'Nuestro prototipo también puede incorporar los datos proporcionados por siete sensores de calidad del aire en tiempo real en Barcelona. ' +
                        'Dado que hay pocos puntos de datos, esta fuente de datos tiene una resolución espacial muy baja en comparación con la histórica.',
                "pdf_page_number": 7,
            },
            {
                "text": 'Para tener en cuenta esta heterogeneidad, nuestro prototipo incorpora la técnica que propusimos recientemente ' +
                        'basada en una Red Neuronal Gráfica entrenada con los datos históricos de alta resolución. ' +
                        'Este aspecto es fundamental, ya que los datos en tiempo real pueden diferir significativamente de los históricos en una ubicación específica. ' +
                        'Por lo tanto, considerar los datos en tiempo real nos permite recomendar rutas verdes con una exposición más precisa, ' +
                        'y por lo tanto más baja, para el usuario.',
                "pdf_page_number": 8,
            },
            {
                "text": 'Esta es la arquitectura de nuestro prototipo, que muestra cómo interactúan los diferentes componentes. ' +
                        'Cada componente está implementado en Python, utilizando bibliotecas de última generación para características como ' +
                        'obtener datos de OpenStreetMap, calcular rutas y mostrar los resultados al usuario.',
                "pdf_page_number": 9,
            },
        ],
        voice_preset="v2/es_speaker_0",
        output_video_path="es_chunk_1_{}.mp4",
        resolution=(3840, 2160),
        repeat=5,
        skip=False
    )

    generate_video(
        input_pdf_path="screenshots.pdf",
        dpi=100,
        scripts=[
            {
                "text": 'En esta demostración, mostramos cómo calcular la ruta verde desde Plaza de Catalunya hasta la Sagrada Familia. ' +
                        'El prototipo muestra estadísticas básicas como la longitud de la ruta verde en comparación con la más corta, ' +
                        'y la reducción en términos de exposición a contaminantes del aire, NO2 en este ejemplo.',
                "pdf_page_number": 1,
            },
            {
                "text": 'El prototipo luego muestra las rutas verde y más corta en el mapa, a través de la API de OpenStreetMap.',
                "pdf_page_number": 2,
            },
            {
                "text": 'De manera similar, podemos calcular rutas verdes que también tienen en cuenta los datos de los sensores de calidad del aire en tiempo real. ' +
                        'En este caso, nuestro algoritmo basado en una red neuronal gráfica primero interpola los datos de baja resolución de los sensores, ' +
                        'y luego calcula la ruta verde resultante.',
                "pdf_page_number": 3,
            },
            {
                "text": 'Como se mencionó antes, los resultados pueden variar significativamente al considerar datos en tiempo real, especialmente cuando la ruta ' +
                        'está en proximidad a un sensor cuyas mediciones son muy diferentes de los datos históricos, como en este ejemplo.',
                "pdf_page_number": 4,
            },
        ],
        voice_preset="v2/es_speaker_0",
        output_video_path="es_chunk_2_{}.mp4",
        resolution=(3840, 2160),
        repeat=5,
        skip=False
    )

    generate_video(
        input_pdf_path="beamer.pdf",
        dpi=600,
        scripts=[
            {
                "text": 'En general, nuestras pruebas realizadas en puntos de inicio y destino populares en Barcelona muestran ' +
                        'una reducción de la exposición al NO2 de −7.23%. Estos resultados corroboran la indicación de que ' +
                        'las rutas verdes son muy beneficiosas tanto para los individuos como para las administraciones públicas. ' +
                        'Se han obtenido resultados similares en otras ciudades importantes, demostrando que las rutas verdes ' +
                        'pueden ser una solución simple, pero muy efectiva, para mejorar la salud de los ciudadanos.',
                "pdf_page_number": 10,
            },
        ],
        voice_preset="v2/es_speaker_0",
        output_video_path="es_chunk_3_{}.mp4",
        resolution=(3840, 2160),
        repeat=5,
        skip=False
    )

