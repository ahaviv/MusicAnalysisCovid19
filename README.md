# MusicAnalysisCovid19

Our collection contains:
1.	Spotify charts:
a.	spotify_charts_songs – contains the most played songs in spotify. The data was extracted from spotify charts, for each week between 2019-03-08 and 2021-03-03. Each song contains the following information: name, artist, genre, audio features*, and a list of weeks in which it was played the most.
b.	spotify_charts_weeks_to_lockdown – contains dates representing weeks for which we extracted the most played songs. For each week there is a number of lockdown on which it occurred (0 if there was no lockdown at that time, and ,1,2,3 respectively to the first, second, and the third lockdowns). In addition, each date has a binary value that indicates whether it occurred before or after corona outbreak.
c.	spotify_charts_weeks_data - contains dates representing weeks for which we found the most played songs. Each week contains the average of all audio features for the most played songs that week.
2.	Galgalats parades:
a.	galgalatz_songs – contains the songs parades extracted from galgalatz website, which were published each week from '2019-02-21' to '2021-02-25', and for each song it’s song name, song artist, genre, audio features*,  and a list of weeks in which the song was shown in the parade.
b.	galgalatz_weeks_to_lockdown – contains dates representing weeks for which we extracted the parades songs, and for each week the number of lockdown on which it occurred (0 if there was no lockdown on that date, 1 for the first lockdown, 2 for the second lockdown and 3 for the third lockdown). In addition for each date, there is a binary value that says whether the date was at the time of the corona or not.
c.	galgalatz_weeks_data - contains dates representing weeks for which we extracted the parades songs, and for each week the average number for each audio feature*.
*Audio features:
•	Danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
•	Acousticness: A measure from 0.0 to 1.0 of whether the track is acoustic.
•	Energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy.
•	Instrumentalness: Predicts whether a track contains no vocals. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content.
•	Liveness: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live.
•	Loudness: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track. Values typical range between -60 and 0 db.
•	Speechiness: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value.
•	Tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
•	Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
