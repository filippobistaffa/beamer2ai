from render import generate_video


if __name__ == "__main__":

    # Bark voice presets
    # https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c

    generate_video(
        input_pdf_path="main.pdf",
        scripts=[
            {
                "text": 'Welcome to the presentation of our work entitled "Recommending Green Routes for Pedestrians ' +
                        'to Reduce the Exposure to Air Pollutants in Barcelona". This is joint work between the ' +
                        'Artificial Intelligence Research Institute and the UPF University in Barcelona.',
                "pdf_page_number": 1,
            },
            {
                "text": 'The main issue we tackle in this work is how to recommend green routes to pedestrians ' +
                        'that minimize the exposure to air pollutants in a city. Now, pedestrians are the most vulnerable ' +
                        'individuals when it comes to air pollution, which can lead to serious health problems.',
                "pdf_page_number": 2,
            },
            {
                "text": 'Along these lines, answering this research question could be of great interest for citizens ' +
                        'that wonder if there are greener alternatives for their commute, even if it implies walking a little longer.',
                "pdf_page_number": 3,
            },
            {
                "text": 'Similarly, public administrations concerned with their citizens\'s health could be interested ' +
                        'in a tool capable of providing greener alternatives to the routes computed by Google Maps, ' +
                        'which disregards the exposure to air pollutants.',
                "pdf_page_number": 4,
            },
            {
                "text": 'In this work we provide a solution to these research questions with our green route prototype, showcasing it ' +
                        'for the city of Barcelona. Specifically, we can compute routes that minimize the exposure to air pollutants, ' +
                        'rather than minimizing the total distance as usually done in normal routing problems.',
                "pdf_page_number": 5,
            },
            {
                "text": 'The exposure to pollutants is computed by considering historical air quality data provided by the Barcelona\' city council. ' +
                        'This data source is characterized by very high spatial resolution, since it provides an air quality measurement for ' +
                        'each road in the map. On the other hand, it is characterized by low temporal resolution, since it is published once per year.',
                "pdf_page_number": 6,
            },
            {
                "text": 'Our prototype can also incorporate the data provided by seven real-time air quality sensors in Barcelona. ' +
                        'Since there are few data points, this data source has very low spatial resolution, compared to the historical one.',
                "pdf_page_number": 7,
            },
            {
                "text": 'To account for this heterogeneity, our prototype incorporates the technique we recently proposed ' +
                        'based on a Graph Neural Network trained on the high-resolution historical data. ' +
                        'This aspect is fundamental as real-time data can differ significantly from historical data in a certain location. ' +
                        'Therefore, accounting for real-time data allows us to recommend green routes with more accurate, ' +
                        'hence lower, exposure to the user.',
                "pdf_page_number": 8,
            },
            {
                "text": 'This is the architecture of our prototype, showing how the different components interact. ' +
                        'Each component is implemented in Python, using state of the art libraries for features such as ' +
                        'fetching data from OpenStreetMap, routing and showing the results to the user.',
                "pdf_page_number": 9,
            },
        ],
        voice_preset="v2/en_speaker_8",
        output_video_path="output.mp4",
        resolution=(3840, 2160)
    )
