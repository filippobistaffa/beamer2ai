from render import generate_video

if __name__ == "__main__":

    generate_video(
        input_pdf_path="beamer.pdf",
        dpi=600,
        scripts=[
            {
                "text": 'Benvinguts a la presentació del nostre treball enfocat a recomanar rutes verdes als vianants ' +
                        'per reduir l’exposició als contaminants de l’aire a Barcelona. Aquest és un treball conjunt entre ' +
                        'l’Institut de Recerca en Intel·ligència Artificial i la Universitat Pompeu Fabra de Barcelona.',
                "pdf_page_number": 1,
            },
            {
                "text": 'El principal problema que abordem en aquest treball és com recomanar rutes verdes als vianants ' +
                        'que minimitzin l’exposició als contaminants de l’aire en una ciutat. Els vianants són els individus més vulnerables ' +
                        'quan es tracta de contaminació de l’aire, ja que poden patir problemes de salut molt greus.',
                "pdf_page_number": 2,
            },
            {
                "text": 'En aquesta línia, respondre aquesta pregunta d’investigació podria ser de gran interès per als ciutadans ' +
                        'que es pregunten si hi ha alternatives més verdes per als seus trajectes, fins i tot si implica caminar una mica més.',
                "pdf_page_number": 3,
            },
            {
                "text": 'De manera similar, les administracions públiques preocupades per la salut dels seus ciutadans podrien estar interessades ' +
                        'en una eina capaç de proporcionar alternatives més verdes a les rutes calculades per Gugol Maps, ' +
                        'que no considera l’exposició als contaminants de l’aire.',
                "pdf_page_number": 4,
            },
            {
                "text": 'En aquest treball proporcionem una solució a aquestes preguntes d’investigació amb el nostre prototip ' +
                        'de rutes verdes, mostrant-lo per a la ciutat de Barcelona. Específicament, podem calcular ' +
                        'rutes que minimitzin l’exposició als contaminants de l’aire, en lloc de minimitzar ' +
                        'la distància total com es fa habitualment en els problemes normals d’encaminament.',
                "pdf_page_number": 5,
            },
            {
                "text": 'L’exposició als contaminants es calcula considerant dades històriques de qualitat de l’aire ' +
                        'proporcionades per l’ajuntament de Barcelona. Aquesta font de dades es caracteritza per una resolució ' +
                        'espacial molt alta, ja que proporciona una mesura de qualitat de l’aire per a cada carrer del mapa. ' +
                        'D’altra banda, es caracteritza per una baixa resolució temporal, ja que es publica un cop a l’any.',
                "pdf_page_number": 6,
            },
            {
                "text": 'El nostre prototip també pot incorporar les dades proporcionades per set sensors de qualitat de l’aire ' +
                        'en temps real a Barcelona. Atès que hi ha tan pocs sensors, aquesta font de dades ' +
                        'té una resolució espacial molt baixa en comparació amb l’històrica.',
                "pdf_page_number": 7,
            },
            {
                "text": 'Per tenir en compte aquesta heterogeneïtat, el nostre prototip incorpora la tècnica que hem proposat recentment ' +
                        'basada en una Xarxa Neuronal Gràfica entrenada amb les dades històriques d’alta resolució. Aquest aspecte és fonamental, ' +
                        'ja que les dades en temps real poden diferir significativament de les històriques en una ubicació donada. ' +
                        'Per tant, considerar les dades en temps real ens permet recomanar rutes verdes amb una exposició més precisa, ' +
                        'i per tant més baixa, per a l’usuari.',
                "pdf_page_number": 8,
            },
            {
                "text": 'Aquesta és l’arquitectura del nostre prototip, que mostra com interactuen els diferents components. ' +
                        'Cada component està implementat en Paiton, utilitzant llibreries d’última generació per executar tasques com ' +
                        'obtenir dades d’Open Strit Map, calcular rutes i mostrar els resultats a l’usuari.',
                "pdf_page_number": 9,
            },
        ],
        model_path="voices/ca_ES-upc_ona-medium.onnx",
        output_video_path="ca_chunk_1.mp4",
        resolution=(3840, 2160),
        skip=True
    )

    generate_video(
        input_pdf_path="screenshots.pdf",
        dpi=100,
        scripts=[
            {
                "text": 'En aquesta demostració, mostrem com calcular la ruta verda des de la Plaça de Catalunya fins a la Sagrada Família. ' +
                        'En aquest cas, el prototip mostra estadístiques bàsiques com la longitud de la ruta verda en comparació ' +
                        'amb la més curta, i la reducció en termes d’exposició al N O dos.',
                "pdf_page_number": 1,
            },
            {
                "text": 'El prototip després mostra la ruta verda i la més curta en el mapa, a través de l’API d’Open Strit Map.',
                "pdf_page_number": 2,
            },
            {
                "text": 'De manera similar, podem calcular rutes verdes que també tenen en compte les dades dels sensors ' +
                        'de qualitat de l’aire en temps real. En aquest cas, el nostre algorisme basat en una xarxa neuronal gràfica ' +
                        'primer interpola les dades de baixa resolució dels sensors i després calcula la ruta verda resultant.',
                "pdf_page_number": 3,
            },
            {
                "text": 'Com s’ha esmentat abans, els resultats poden variar significativament en considerar ' +
                        'dades en temps real, especialment quan la ruta està a prop d’un sensor les mesures del qual ' +
                        'són molt diferents de les dades històriques, com en aquest exemple.',
                "pdf_page_number": 4,
            },
        ],
        model_path="voices/ca_ES-upc_ona-medium.onnx",
        output_video_path="ca_chunk_2.mp4",
        resolution=(3840, 2160),
        skip=True
    )

    generate_video(
        input_pdf_path="beamer.pdf",
        dpi=600,
        scripts=[
            {
                "text": 'En general, les nostres proves realitzades en punts d’inici i destinació populars a Barcelona mostren ' +
                        'una reducció de l’exposició al N O dos de menys 7 per cent. Aquests resultats corroboren la indicació que ' +
                        'les rutes verdes són molt beneficioses tant per als individus com per a les administracions públiques. ' +
                        'S’han obtingut resultats similars en altres ciutats importants, demostrant que les rutes verdes ' +
                        'poden ser una solució simple, però molt efectiva, per millorar la salut dels ciutadans.',
                "pdf_page_number": 10,
            },
        ],
        model_path="voices/ca_ES-upc_ona-medium.onnx",
        output_video_path="ca_chunk_3.mp4",
        resolution=(3840, 2160),
        skip=False
    )
