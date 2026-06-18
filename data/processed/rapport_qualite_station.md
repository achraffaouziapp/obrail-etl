# Rapport qualite - Table STATION

- Gares brutes disponibles : 28784
- Gares utilisees par les routes : 129
- Gares associees (exact + prefixe) : 100
- Gares finales (apres dedoublonnage) : 100
- Taux de couverture : 77.5%
- Gares sans coordonnees GPS : 0

## Limite connue : matching par prefixe
Les routes utilisent des noms de villes generiques (ex: 'Wien'),
alors que stops.json contient des gares precises (ex: 'Wien Hbf').
Le matching par prefixe peut generer des faux positifs
(ex: 'Berlin' -> 'Berlingen'). Un referentiel UIC normalise
resoudrait ce probleme. Code UIC absent des donnees sources.

## Gares non associees (29)
- Burgas
- Cherkasy
- Chernihiv
- Chernivtsi
- Dnipro
- Dobrich
- Ivano-Frankivsk
- Kamianets-Podilskyi
- Kharkiv
- Kovel
- Kremenchuk
- Kryvyi Rih
- Kyiv
- Lozova
- Lviv
- Mukacheve
- Mykolaiv
- Odesa
- Rakhiv
- Silistra
- Sofia
- Solotvyno
- Sumy
- Truskavets
- Uzhhorod
- Varna
- Vorokhta
- Yasinia
- Zaporizhzhia